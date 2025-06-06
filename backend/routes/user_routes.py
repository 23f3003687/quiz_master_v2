# routes/user_routes.py
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db ,User, Score, Subject, Chapter, Quiz, Question, UserAnswer
from datetime import datetime
user_bp = Blueprint('user', __name__)

# backend/routes/user_routes.py

def calculate_performance(user_id):
    from models import Score
    scores = Score.query.filter_by(user_id=user_id).all()
    if not scores:
        return 0
    total_score = sum(score.total_score for score in scores)
    total_max = sum(score.correct_answers for score in scores)
    return round((total_score / total_max) * 100) if total_max > 0 else 0




@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_user_dashboard():
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Calculate performance
    performance = calculate_performance(user_id)

    # Quizzes completed
    completed_scores = Score.query.filter_by(user_id=user_id).order_by(Score.time_stamp_of_attempt.desc()).all()
    quizzes_completed = len(completed_scores)

    # Last login
    last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "N/A"

    # Activity log (latest 5)
    activity_log = []
    for score in completed_scores[:5]:
        quiz = Quiz.query.get(score.quiz_id)
        total_questions = score.correct_answers + score.wrong_answers
        accuracy = round((score.correct_answers / total_questions) * 100, 2) if total_questions else 0

        activity_log.append({
            "id": score.score_id,
            "quiz_name": quiz.name if quiz else "Unknown Quiz",
            "score": score.total_score,
            "accuracy": accuracy,
            "completion_date": score.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({
        "full_name": user.full_name,
        "email": user.email,
        "qualification": user.qualification,
        "performance": performance,
        "last_login": last_login,
        "quizzes_completed": quizzes_completed,
        "activity_log": activity_log
    })
    
@user_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_all_subjects():
    subjects = Subject.query.all()
    subject_list = [
        {
            "subject_id": subject.subject_id,
            "name": subject.name,
            "description": subject.description
        }
        for subject in subjects
    ]
    return jsonify({"subjects": subject_list}), 200

@user_bp.route('/subject/<int:subject_id>/quizzes', methods=['GET'])
@jwt_required()
def get_quizzes_by_subject(subject_id):
    try:
        # Find all chapters under the subject
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()

        all_quizzes = []
        for chapter in chapters:
            quizzes = Quiz.query.filter_by(chapter_id=chapter.chapter_id).all()
            for quiz in quizzes:
                quiz_data = {
                    'quiz_id': quiz.quiz_id,
                    'name': quiz.name,
                    'date_of_quiz': quiz.date_of_quiz.isoformat() if quiz.date_of_quiz else None,
                    'time_duration': quiz.time_duration,
                    'total_marks': quiz.total_marks,
                    'num_questions': quiz.num_questions,
                    'remarks': quiz.remarks,
                    'tags': quiz.tags,
                    'chapter': {
                        'chapter_id': chapter.chapter_id,
                        'name': chapter.name,
                        'description': chapter.description,
                        'difficulty_level': chapter.difficulty_level
                    }
                }
                all_quizzes.append(quiz_data)

        return jsonify(all_quizzes), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Something went wrong'}), 500
    
@user_bp.route("/quiz/<int:quiz_id>/attempt", methods=["GET", "OPTIONS"])
@cross_origin()
def get_quiz_attempt(quiz_id):
    if request.method == "OPTIONS":
        return '', 200

    from flask_jwt_extended import verify_jwt_in_request
    verify_jwt_in_request()

    quiz = Quiz.query.filter_by(quiz_id=quiz_id).first()
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    questions = Question.query.filter_by(quiz_id=quiz_id).all()

    quiz_data = {
        "quiz_id": quiz.quiz_id,
        "name": quiz.name,
        "time_duration": quiz.time_duration,
        "total_marks": quiz.total_marks,
    }

    questions_data = []
    for q in questions:
        questions_data.append({
            "question_id": q.question_id,
            "question_statement": q.question_statement,
            "option1": q.option1,
            "option2": q.option2,
            "option3": q.option3,
            "option4": q.option4,
        })

    return jsonify({
        "quiz": quiz_data,
        "questions": questions_data
    })

    
@user_bp.route('/submit-quiz/<int:quiz_id>', methods=['POST', 'OPTIONS'])
@cross_origin()
@jwt_required()
def submit_quiz(quiz_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    answers = data.get("answers", [])  # [{question_id: 1, selected_option: "option2"}, ...]

    total_score = 0
    correct_count = 0
    wrong_count = 0

    # Step 1: Create Score object
    score = Score(
        quiz_id=quiz_id,
        user_id=user_id,
        time_stamp_of_attempt=datetime.utcnow(),
        total_score=0,  # will be updated below
        correct_answers=0,
        wrong_answers=0,
        time_taken=data.get("time_taken", "00:00"),
        remarks=None,
        status=None
    )
    db.session.add(score)
    db.session.commit()

    for ans in answers:
        question = Question.query.get(ans["question_id"])
        if not question:
            continue

        selected_key = ans.get("selected_option")
        print(f"Question ID: {question.question_id}, Selected option key: {selected_key}")


        # Handle skipped or invalid answers
        if not selected_key:
            selected_value = "skipped"
            is_correct = False
        else:
            selected_key = str(selected_key)
            selected_value = getattr(question, selected_key, None)
            print(f"Selected value from question: {selected_value}")

            if selected_value is None:
                selected_value = "invalid"
                is_correct = False
            else:
                correct_value = getattr(question, question.correct_option, None)
                is_correct = selected_value == correct_value

        # Update score counts
        if is_correct:
            total_score += 1
            correct_count += 1
        else:
            wrong_count += 1

        user_answer = UserAnswer(
            score_id=score.score_id,
            question_id=question.question_id,
            selected_option=selected_value,
            is_correct=is_correct
        )
        db.session.add(user_answer)

    # Step 2: Update Score fields
    score.total_score = total_score
    score.correct_answers = correct_count
    score.wrong_answers = wrong_count
    score.status = "Passed" if correct_count >= len(answers) / 2 else "Failed"

    db.session.commit()

    return jsonify({
        "message": "Quiz submitted successfully",
        "score_id": score.score_id
    }), 200


@user_bp.route('/score/<int:score_id>', methods=['GET'])
@jwt_required()
def get_scorecard(score_id):
    score = Score.query.get_or_404(score_id)
    user_answers = UserAnswer.query.filter_by(score_id=score_id).all()

    questions = []
    for ans in user_answers:
        question = Question.query.get(ans.question_id)
        questions.append({
            "question_statement": question.question_statement,
            "selected_option": ans.selected_option,
            "correct_option": question.correct_option,
            "is_correct": ans.is_correct,
            "difficulty": question.difficulty,
            "explanation": question.explanation
        })

    return jsonify({
        "score_id": score.score_id,
        "quiz_id": score.quiz_id,
        "total_score": score.total_score,
        "correct_answers": score.correct_answers,
        "wrong_answers": score.wrong_answers,
        "time_stamp_of_attempt": score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M'),
        "status": score.status,
        "questions": questions
    }), 200

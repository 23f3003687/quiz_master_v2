# routes/user_routes.py
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db ,User, Score, Subject, Chapter, Quiz, Question, UserAnswer
from datetime import datetime, timedelta
import pytz
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

def generate_remarks(total_score, total_marks):
    percentage = total_score / total_marks if total_marks > 0 else 0

    if percentage == 1.0:
        return "Outstanding! You aced it!"
    elif percentage >= 0.75:
        return "Great job! Keep it up!"
    elif percentage >= 0.5:
        return "Good effort. Review and try again!"
    else:
        return "Needs improvement. Don’t give up!"





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
            "score": f"{score.total_score} / {quiz.total_marks if quiz else 'N/A'}",
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
                    'time_duration': quiz.time_duration,
                    'start_datetime': quiz.start_datetime.isoformat() if quiz.start_datetime else None,
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


     # Use IST timezone
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    # Localize start time if it's naive
    if quiz.start_datetime.tzinfo is None:
        start_time = ist.localize(quiz.start_datetime)
    else:
        start_time = quiz.start_datetime.astimezone(ist)

    end_time = start_time + timedelta(minutes=quiz.time_duration)


    if now < start_time:
        return jsonify({"error": "Quiz has not started yet. Please check the Quiz Datetime again."}), 403
    elif now > end_time:
        return jsonify({"error": "Quiz has expired."}), 403
   

    quiz_data = {
        "quiz_id": quiz.quiz_id,
        "name": quiz.name,
        "time_duration": quiz.time_duration,
        "total_marks": quiz.total_marks,
        "subject_id": quiz.chapter.subject.subject_id,
    }

    questions_data = [{
        "question_id": q.question_id,
        "question_statement": q.question_statement,
        "option1": q.option1,
        "option2": q.option2,
        "option3": q.option3,
        "option4": q.option4,
    } for q in quiz.questions]

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

    # Step 1: Create Score object
    score = Score(
        quiz_id=quiz_id,
        user_id=user_id,
        time_stamp_of_attempt=datetime.utcnow(),
        total_score=0,
        correct_answers=0,
        wrong_answers=0,
        time_taken=data.get("time_taken", "00:00"),
        remarks=None,
        status=None
    )
    db.session.add(score)
    db.session.commit()

    # Step 2: Get all questions for the quiz
    all_questions = Question.query.filter_by(quiz_id=quiz_id).all()
    answered_question_ids = set(ans["question_id"] for ans in answers)
    question_map = {q.question_id: q for q in all_questions}

    total_score = 0
    correct_count = 0
    wrong_count = 0

    # Step 3: Process submitted answers
    for ans in answers:
        question = question_map.get(ans["question_id"])
        if not question:
            continue

        selected_key = str(ans.get("selected_option"))
        if not selected_key:
            selected_value = "skipped"
            is_correct = False
        else:
            selected_value = getattr(question, selected_key, None)
            correct_value = getattr(question, question.correct_option, None)

            if selected_value is None:
                selected_value = "invalid"
                is_correct = False
            else:
                is_correct = selected_value == correct_value

        if is_correct:
            correct_count += 1
            total_score += 1
        elif selected_value not in ["skipped", "invalid"]:
            wrong_count += 1

        db.session.add(UserAnswer(
            score_id=score.score_id,
            question_id=question.question_id,
            selected_option=selected_value,
            is_correct=is_correct
        ))

    # Step 4: Handle skipped questions (not in answers at all)
    for q in all_questions:
        if q.question_id not in answered_question_ids:
            db.session.add(UserAnswer(
                score_id=score.score_id,
                question_id=q.question_id,
                selected_option="skipped",
                is_correct=False
            ))

    # Step 5: Finalize Score
    quiz = Quiz.query.get(quiz_id)
    total_marks = quiz.total_marks if quiz else len(all_questions)

    score.total_score = total_score
    score.correct_answers = correct_count
    score.wrong_answers = wrong_count
    score.status = "PASSED" if correct_count >= len(all_questions) / 2 else "FAILED"
    score.remarks = generate_remarks(total_score, total_marks)

    db.session.commit()

    return jsonify({
        "message": "Quiz submitted successfully",
        "score_id": score.score_id
    }), 200



@user_bp.route('/score/<int:score_id>', methods=['GET'])
@jwt_required()
def get_scorecard(score_id):
    score = Score.query.get_or_404(score_id)
    quiz = Quiz.query.get(score.quiz_id)
    user_answers = UserAnswer.query.filter_by(score_id=score_id).all()
    attempted = score.correct_answers + score.wrong_answers

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
        "quiz_total_marks": quiz.total_marks if quiz else 0,
        "correct_answers": score.correct_answers,
        "wrong_answers": score.wrong_answers,
        "attempted_questions": attempted,
        "total_questions": len(user_answers),
        "time_stamp_of_attempt": score.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M'),
        "time_taken": score.time_taken,
        "status": score.status,
        "remarks": score.remarks,
        "questions": questions
    }), 200
    
@user_bp.route('/score/history', methods=['GET'])
@jwt_required()
def get_score_history():
    user_id = get_jwt_identity()
    scores = Score.query.filter_by(user_id=user_id).order_by(Score.time_stamp_of_attempt.desc()).all()
    history = []
    for s in scores:
        quiz = Quiz.query.get(s.quiz_id)
        history.append({
            "score_id": s.score_id,
            "quiz_name": quiz.name if quiz else "Unknown Quiz",
            "score": f"{s.total_score}/{quiz.total_marks}" if quiz else s.total_score,
            "accuracy": f"{round((s.correct_answers / (s.correct_answers + s.wrong_answers)) * 100, 2)}%" if (s.correct_answers + s.wrong_answers) else "N/A",
            "status": s.status,
            "time_stamp_of_attempt": s.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M')
        })
    return jsonify(history), 200


@user_bp.route('/summary-report', methods=['GET'])
@jwt_required()
def summary_report():
    user_id = get_jwt_identity()
    scores = Score.query.filter_by(user_id=user_id).all()

    if not scores:
        return jsonify({"message": "No attempts yet", "summary": {}, "scores": []}), 200

    # Compose summary stats
    total_quizzes = len(scores)
    total_score = sum(score.total_score for score in scores)
    highest_score = max(score.total_score for score in scores)
    average_score = round(total_score / total_quizzes, 2)
    passed = sum(1 for s in scores if s.status == "PASSED")
    failed = total_quizzes - passed
    total_correct = sum(s.correct_answers for s in scores)
    total_questions = total_correct + sum(s.wrong_answers for s in scores)
    accuracy = round((total_correct / total_questions) * 100, 2) if total_questions else 0

    # Also prepare detailed score info for frontend charts
    detailed_scores = []
    for s in scores:
        detailed_scores.append({
            "quiz_name": s.quiz.name if s.quiz else "Unknown Quiz",
            "total_score": s.total_score,
            "quiz_total_marks": s.quiz.total_marks if s.quiz else 0,
            "status": s.status,
            "time_stamp_of_attempt": s.time_stamp_of_attempt.isoformat(),
        })

    return jsonify({
        "summary": {
            "total_quizzes": total_quizzes,
            "total_score": total_score,
            "highest_score": highest_score,
            "average_score": average_score,
            "passed": passed,
            "failed": failed,
            "accuracy": accuracy
        },
        "scores": detailed_scores
    }), 200

@user_bp.route("/search", methods=["GET"])
@cross_origin()
@jwt_required()
def user_search():
    query = request.args.get("query", "").strip().lower()
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    results = []

    # Subjects
    subjects = Subject.query.filter(
        (Subject.name.ilike(f"%{query}%")) |
        (Subject.description.ilike(f"%{query}%"))
    ).all()
    for s in subjects:
        results.append({
            "type": "subject",
            "subject_id": s.subject_id,
            "name": s.name,
            "description": s.description
        })

    # Quizzes
    quizzes = Quiz.query.join(Chapter).join(Subject).filter(
        (Quiz.name.ilike(f"%{query}%")) |
        (Chapter.name.ilike(f"%{query}%")) |
        (Subject.name.ilike(f"%{query}%"))
    ).all()
    for q in quizzes:
        results.append({
            "type": "quiz",
            "quiz_id": q.quiz_id,
            "name": q.name,
            "chapter_name": q.chapter.name,
            "subject_id": q.chapter.subject.subject_id,
            "subject_name": q.chapter.subject.name,
            "start_datetime": q.start_datetime.strftime("%Y-%m-%d %H:%M"),
            "total_marks": q.total_marks
        })

    return jsonify(results), 200

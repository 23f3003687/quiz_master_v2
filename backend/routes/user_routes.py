# routes/user_routes.py
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Score, Subject, Chapter, Quiz, Question
user_bp = Blueprint('user', __name__)

# backend/routes/user_routes.py

def calculate_performance(user_id):
    from models import Score
    scores = Score.query.filter_by(user_id=user_id).all()
    if not scores:
        return 0
    total_score = sum(score.marks_obtained for score in scores)
    total_max = sum(score.total_marks for score in scores)
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

    # Activity log: latest 5 attempts
    activity_log = [
        {
            "id": score.score_id,
            "timestamp": score.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M:%S"),
            "description": f"Attempted quiz ID {score.quiz_id} - Score: {score.total_score}"
        }
        for score in completed_scores[:5]
    ]

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
@cross_origin()  # this adds the correct CORS headers
def get_quiz_attempt(quiz_id):
    if request.method == "OPTIONS":
        return '', 200  # Respond to CORS preflight

    # Apply JWT only for actual GET requests
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
        options = [q.option1, q.option2, q.option3, q.option4]
        questions_data.append({
            "question_id": q.question_id,
            "question_statement": q.question_statement,
            "options": options
        })

    return jsonify({
        "quiz": quiz_data,
        "questions": questions_data
    })

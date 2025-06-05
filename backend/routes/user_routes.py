# routes/user_routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Score, Subject
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
    

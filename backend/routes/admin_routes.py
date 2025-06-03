# routes/admin_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db , Subject, Chapter, User, Quiz
from datetime import datetime
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects(): #show all the subjects on dashboard
    claims = get_jwt()
    is_admin = claims.get("is_admin", False)


    if not is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        subjects = Subject.query.all()
        subjects_list = [
            {
                "subject_id": subject.subject_id,
                "name": subject.name,
                "description": subject.description
            }
            for subject in subjects
        ]
        return jsonify(subjects_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/subjects', methods=['POST'])
@jwt_required()
def create_subject():
    claims = get_jwt()
    is_admin = claims.get("is_admin", False)

    if not is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name or not description:
        return jsonify({"error": "Name and description are required"}), 400

    try:
        new_subject = Subject(name=name, description=description)
        db.session.add(new_subject)
        db.session.commit()

        return jsonify({
           "subject_id": new_subject.subject_id,
           "name": new_subject.name,
           "description": new_subject.description
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@admin_bp.route('/subject/<int:subject_id>', methods=['GET']) #show subject details
@jwt_required()
def get_subject_details(subject_id):
    claims = get_jwt()
    is_admin = claims.get("is_admin", False)

    if not is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({"error": "Subject not found"}), 404

        chapters = subject.chapters  # Assuming you have a relationship between Subject and Chapter
        chapters_list = [
            {
                "chapter_id": chapter.chapter_id,
                "name": chapter.name,
                "description": chapter.description,
                "difficulty_level": chapter.difficulty_level,
            }
            for chapter in chapters
        ]

        return jsonify({"subject": {"subject_id": subject.subject_id,"name": subject.name, "description": subject.description}, "chapters": chapters_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/subject/<int:subject_id>', methods=['PUT'])
@jwt_required()
def update_subject(subject_id):
    claims = get_jwt()
    is_admin = claims.get("is_admin", False)

    if not is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if name:
        subject.name = name
    if description:
        subject.description = description

    try:
        db.session.commit()
        return jsonify({
            "subject_id": subject.subject_id,
            "name": subject.name,
            "description": subject.description
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/subject/<int:subject_id>', methods=['DELETE'])
@jwt_required()
def delete_subject(subject_id):
    claims = get_jwt()
    is_admin = claims.get("is_admin", False)

    if not is_admin:
        return jsonify({"error": "Unauthorized"}), 403
    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404

    db.session.delete(subject)
    db.session.commit()
    return jsonify({'message': 'Subject deleted successfully'}) , 200

@admin_bp.route('/chapters', methods=['POST'])
@jwt_required()
def create_chapter():
    data = request.get_json()
    subject_id = data.get('subject_id')
    name = data.get('name')
    description = data.get('description')
    difficulty_level = data.get('difficulty_level')

    if not subject_id or not name or not difficulty_level:
        return jsonify({'error': 'Missing required fields'}), 400

    new_chapter = Chapter(
        subject_id=subject_id,
        name=name,
        description=description,
        difficulty_level=difficulty_level
    )
    db.session.add(new_chapter)
    db.session.commit()

    return jsonify({
        'chapter_id': new_chapter.chapter_id,
        'name': new_chapter.name,
        'description': new_chapter.description,
        'difficulty_level': new_chapter.difficulty_level
    }), 201

@admin_bp.route('/chapters/<int:chapter_id>', methods=['PUT', 'OPTIONS'])
@jwt_required()
def update_chapter(chapter_id):
    if request.method == 'OPTIONS':
        return '', 200  # Respond to preflight request with 200 OK

    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({"error": "Chapter not found"}), 404

    data = request.get_json()

    # Update fields if provided
    chapter.name = data.get('name', chapter.name)
    chapter.description = data.get('description', chapter.description)
    chapter.difficulty_level = data.get('difficulty_level', chapter.difficulty_level)

    try:
        db.session.commit()
        return jsonify({
            "chapter_id": chapter.chapter_id,
            "name": chapter.name,
            "description": chapter.description,
            "difficulty_level": chapter.difficulty_level,
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update chapter"}), 500


@admin_bp.route('/chapters/<int:chapter_id>', methods=['DELETE'])
@jwt_required()
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        return jsonify({"error": "Chapter not found"}), 404

    try:
        db.session.delete(chapter)
        db.session.commit()
        return jsonify({"message": "Chapter deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete chapter"}), 500
    
@admin_bp.route('/chapters/<int:chapter_id>/quizzes', methods=['GET'])
@jwt_required()
def get_quizzes_by_chapter(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    quiz_list = []
    for q in quizzes:
        quiz_list.append({
            "quiz_id": q.quiz_id,
            "name": q.name,
            "date_of_quiz": q.date_of_quiz.isoformat(),  # date as string
            "time_duration": q.time_duration,
            "total_marks": q.total_marks,
            "remarks": q.remarks,
            "is_active": q.is_active,
            "num_questions": q.num_questions,
            "tags": q.tags,
        })
    return jsonify(quiz_list), 200

@admin_bp.route('/chapters/<int:chapter_id>/quizzes', methods=['POST'])
@jwt_required()
def create_quiz_for_chapter(chapter_id):
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'date_of_quiz', 'time_duration', 'total_marks', 'num_questions']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        new_quiz = Quiz(
            chapter_id=chapter_id,
            name=data['name'],
            date_of_quiz=datetime.strptime(data['date_of_quiz'], "%Y-%m-%d").date(),
            time_duration=data['time_duration'],
            total_marks=data['total_marks'],
            remarks=data.get('remarks', ''),
            num_questions=data['num_questions'],
            tags=data.get('tags', '')
        )
        db.session.add(new_quiz)
        db.session.commit()

        return jsonify({
            "quiz_id": new_quiz.quiz_id,
            "name": new_quiz.name,
            "date_of_quiz": new_quiz.date_of_quiz.isoformat(),
            "time_duration": new_quiz.time_duration,
            "total_marks": new_quiz.total_marks,
            "remarks": new_quiz.remarks,
            "is_active": new_quiz.is_active,
            "num_questions": new_quiz.num_questions,
            "tags": new_quiz.tags,
        }), 201

    except Exception as e:
        print("Error creating quiz:", e)
        return jsonify({"message": "Failed to create quiz"}), 500
    
@admin_bp.route('/quizzes/<int:quiz_id>', methods=['PUT'])
@jwt_required()
def update_quiz(quiz_id):
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    data = request.get_json()

    try:
        quiz.name = data.get('name', quiz.name)

        date_str = data.get('date_of_quiz')
        if date_str:
            quiz.date_of_quiz = datetime.strptime(date_str, "%Y-%m-%d").date()

        quiz.time_duration = data.get('time_duration', quiz.time_duration)
        quiz.total_marks = data.get('total_marks', quiz.total_marks)
        quiz.num_questions = data.get('num_questions', quiz.num_questions)
        quiz.remarks = data.get('remarks', quiz.remarks)
        quiz.tags = data.get('tags', quiz.tags)

        db.session.commit()
        return jsonify({"message": "Quiz updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@admin_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
@jwt_required()
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    try:
        db.session.delete(quiz)
        db.session.commit()
        return jsonify({"message": f"Quiz {quiz_id} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    user_list = [
        {
            "user_id": user.user_id,
            "email": user.email,
            "full_name": user.full_name,
            "qualification": user.qualification,
            "dob": user.dob.strftime('%Y-%m-%d'),
            "is_admin": user.is_admin,
            "last_login": user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else None,
            "registered_on": user.registered_on.strftime('%Y-%m-%d %H:%M:%S')
        }
        for user in users
    ]
    return jsonify(user_list), 200
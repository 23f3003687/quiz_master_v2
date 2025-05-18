# routes/admin_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db , Subject, Chapter, User
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
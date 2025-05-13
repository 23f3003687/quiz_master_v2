# routes/admin_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db , Subject
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects():
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

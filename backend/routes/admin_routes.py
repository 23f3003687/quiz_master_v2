# routes/admin_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Subject
admin_bp = Blueprint('admin', __name__)

from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

@admin_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects():
    claims = get_jwt()
    is_admin = claims.get("is_admin", False)

    print("JWT Claims:", claims)  # ✅ will show is_admin

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

# routes/admin_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects():
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"error": "Unauthorized"}), 403

    # Dummy response (replace with real DB logic later)
    return jsonify({"subjects": ["Math", "Science", "History"]}), 200

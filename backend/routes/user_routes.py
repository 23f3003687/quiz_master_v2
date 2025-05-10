# routes/user_routes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

@user_bp.route('/scores', methods=['GET'])
@jwt_required()
def get_scores():
    current_user = get_jwt_identity()
    if current_user.get("is_admin"):
        return jsonify({"error": "Admins cannot view user scores this way"}), 403

    # Dummy response (replace with DB fetch later)
    return jsonify({"scores": [80, 90, 85]}), 200

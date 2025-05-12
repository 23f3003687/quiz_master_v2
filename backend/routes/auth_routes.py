from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

# Admin credentials from environment
admin_email = os.getenv('ADMIN_EMAIL')
admin_password_hash = os.getenv('ADMIN_PASSWORD_HASH')

# Ensure Admin Exists
def ensure_admin_user():
    if not admin_email or not admin_password_hash:
        print("Admin email or password hash not found in .env")
        return

    existing_admin = User.query.filter_by(email=admin_email, is_admin=True).first()
    if not existing_admin:
        admin = User(
            email=admin_email,
            password=admin_password_hash,  # Already hashed in .env
            full_name="Quiz Master",
            qualification="Admin Certified",
            dob=datetime.strptime('1990-01-01', '%Y-%m-%d'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created.")
    else:
        print("ℹ️ Admin already exists.")
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        # Update last_login
        user.last_login = datetime.utcnow()
        db.session.commit()

        access_token = create_access_token(
            identity=str(user.user_id),
            additional_claims={"is_admin": user.is_admin}
        )
        return jsonify({"access_token": access_token, "is_admin": user.is_admin}), 200

    return jsonify({"msg": "Invalid credentials"}), 401



# User Registration
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    qualification = data.get('qualification')
    dob = data.get('dob')

    try:
        dob = datetime.strptime(dob, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered."}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, full_name=full_name, qualification=qualification, dob=dob, is_admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201

# Protected Route Example
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.get(current_user["user_id"])  # Fetch user by ID from JWT payload
    
    if user:
        return jsonify({
            "user_id": user.user_id,
            "email": user.email,
            "full_name": user.full_name,
            "qualification": user.qualification,
            "dob": user.dob,
            "is_admin": user.is_admin
        }), 200
    
    return jsonify({"error": "User not found"}), 404

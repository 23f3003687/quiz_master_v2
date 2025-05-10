from flask import Flask, jsonify, request
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from models import db, User
from dotenv import load_dotenv
from datetime import datetime
from routes.auth_routes import auth_bp
# from routes.admin_routes import admin_bp
# from routes.user_routes import user_bp
import os
from flask_cors import CORS
# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
CORS(app, resources={r"/*": {"origins": "http://localhost:5174"}}, supports_credentials=True)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')



# Initialize extensions
jwt = JWTManager(app)
db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# # Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
# app.register_blueprint(admin_bp, url_prefix='/admin')
# app.register_blueprint(user_bp, url_prefix='/user')

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

# ✅ Create admin user using pre-hashed password
def create_admin_user():
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password_hash = os.getenv('ADMIN_PASSWORD_HASH')  # Already hashed

    if not admin_email or not admin_password_hash:
        print("⚠️ ADMIN_EMAIL or ADMIN_PASSWORD_HASH missing in .env")
        return

    existing_admin = User.query.filter_by(email=admin_email, is_admin=True).first()
    if not existing_admin:
        admin = User(
            email=admin_email,
            password=admin_password_hash,
            full_name="Quiz Master",
            qualification="Admin Qualified",
            dob=datetime.strptime('1995-12-30', '%Y-%m-%d'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created.")
    else:
        print("ℹ️ Admin user already exists.")

# ✅ Ensure DB and admin are ready before serving requests
with app.app_context():
    db.create_all()
    create_admin_user()

# Root redirect
@app.route('/')
def index():
    return jsonify({"message": "Quiz Master API is running."})


# Run server
if __name__ == '__main__':
    app.run(debug=True)

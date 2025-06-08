from app import app,db
from models import *  # Import your models


with app.app_context():
    print("⚠️ Dropping all tables...")
    db.drop_all()
    print("✅ Tables dropped.")

    print("🔁 Creating all tables...")
    db.create_all()
    print("✅ Tables created.")

    # Optionally seed one admin user or test data here
    # Example:
    # from datetime import date
    # admin = User(email='admin@example.com', password='hashed_pw', full_name='Admin', dob=date(1990,1,1), is_admin=True)
    # db.session.add(admin)
    # db.session.commit()

    print("🎉 Database reset complete.")

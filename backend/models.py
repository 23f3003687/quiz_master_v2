from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    qualification = db.Column(db.String(120), nullable=True)
    dob = db.Column(db.Date, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    scores = db.relationship('Score', backref='user', lazy=True, cascade="all, delete-orphan")

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        role = "Admin" if self.is_admin else "User"
        return f"<{role} {self.email}>"

class Subject(db.Model):
    __tablename__ = 'subjects'

    subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)


    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subject {self.name}>"

class Chapter(db.Model):
    __tablename__ = 'chapters'

    chapter_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.subject_id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty_level = db.Column(db.String(50), nullable=True)  # e.g., Easy, Medium, Hard

    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Chapter {self.name}>"

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    quiz_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.chapter_id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.String(10), nullable=False)  # Format: HH:MM
    total_marks = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    num_questions = db.Column(db.Integer, nullable=False, default=0)
    tags = db.Column(db.String(255), nullable=True)

    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Quiz {self.name}>"

class Question(db.Model):
    __tablename__ = 'questions'

    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(10), nullable=False)  # e.g., "option2"
    difficulty = db.Column(db.String(50), nullable=True)  # Optional
    explanation = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Question ID: {self.question_id} | Quiz: {self.quiz_id}>"

class Score(db.Model):
    __tablename__ = 'scores'

    score_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    total_score = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=True)
    wrong_answers = db.Column(db.Integer, nullable=True)
    time_taken = db.Column(db.String(10), nullable=True)  # Format: MM:SS
    remarks = db.Column(db.String(255), nullable=True)
    ranking = db.Column(db.Integer, nullable=True)  # Optional
    status = db.Column(db.String(20), nullable=True)  # e.g., Passed, Failed

    def __repr__(self):
        return f"<Score {self.score_id} | User {self.user_id} | Quiz {self.quiz_id}>"

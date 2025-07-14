from extensions import cache
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import db , Subject, Chapter, User, Quiz, Question, Score
from datetime import datetime, timedelta
from tasks.daily_reminder import send_daily_quiz_reminders
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__)
@admin_bp.route('/trigger-daily-reminders', methods=['GET'])
@jwt_required
def trigger_reminders():
    current_user = get_jwt()
    if current_user['role'] != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    send_daily_quiz_reminders.delay()
    return jsonify({"message": "Reminders scheduled"}), 200


@admin_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects(): #show all the subjects on dashboard
    claims = get_jwt()
    if not claims or not claims.get("is_admin", False):
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
    if not claims or not claims.get("is_admin", False):
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
    if not claims or not claims.get("is_admin", False):
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
    if not claims or not claims.get("is_admin", False):
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
    if not claims or not claims.get("is_admin", False):
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
            "time_duration": q.time_duration,
            "start_datetime": q.start_datetime.isoformat() if q.start_datetime else None,
            "total_marks": q.total_marks,
            "remarks": q.remarks,
            "num_questions": q.num_questions,
            "tags": q.tags,
        })
    return jsonify(quiz_list), 200

@admin_bp.route('/chapters/<int:chapter_id>/quizzes', methods=['POST'])
@jwt_required()
def create_quiz_for_chapter(chapter_id):
    data = request.get_json()

    # Validate required fields
    required_fields = ['name','time_duration','start_datetime','total_marks', 'num_questions']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    try:
        new_quiz = Quiz(
            chapter_id=chapter_id,
            name=data['name'],
            time_duration=data['time_duration'],
            start_datetime=datetime.strptime(data['start_datetime'], "%Y-%m-%dT%H:%M"),
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
            "time_duration": new_quiz.time_duration,
            "start_datetime": new_quiz.start_datetime.isoformat(),
            "total_marks": new_quiz.total_marks,
            "remarks": new_quiz.remarks,
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
            
        start_dt = data.get('start_datetime')
        if start_dt:
            quiz.start_datetime = datetime.strptime(start_dt, "%Y-%m-%dT%H:%M")

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
    
@admin_bp.route('/quizzes/<int:quiz_id>/questions', methods=['POST'])
@jwt_required()
def create_question(quiz_id):
    data = request.get_json()

    required_fields = ['question_statement', 'option1', 'option2', 'option3', 'option4', 'correct_option']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    question = Question(
        quiz_id=quiz_id,
        question_statement=data['question_statement'],
        option1=data['option1'],
        option2=data['option2'],
        option3=data['option3'],
        option4=data['option4'],
        correct_option=data['correct_option'],
        difficulty=data.get('difficulty'),
        explanation=data.get('explanation')
    )

    db.session.add(question)
    db.session.commit()
     

    return jsonify({'message': 'Question created successfully'}), 201

@admin_bp.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])
def get_quiz_questions(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    questions_list = []
    for q in questions:
        questions_list.append({
            "question_id": q.question_id,
            "question_statement": q.question_statement,
            "option1": q.option1,
            "option2": q.option2,
            "option3": q.option3,
            "option4": q.option4,
            "correct_option": q.correct_option,
            "difficulty": q.difficulty,
            "explanation": q.explanation,
            # Add any other fields needed
        })
    return jsonify(questions_list)

@admin_bp.route('/questions/<int:question_id>', methods=['PUT'])
@jwt_required()

def update_question(question_id):
    data = request.get_json()

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    question.question_statement = data.get('question_statement', question.question_statement)
    question.option1 = data.get('option1', question.option1)
    question.option2 = data.get('option2', question.option2)
    question.option3 = data.get('option3', question.option3)
    question.option4 = data.get('option4', question.option4)
    question.correct_option = data.get('correct_option', question.correct_option)
    question.difficulty = data.get('difficulty', question.difficulty)
    question.explanation = data.get('explanation', question.explanation)

    try:
        db.session.commit()
        return jsonify({"message": "Question updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update question", "details": str(e)}), 500

@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully"})

    
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

@admin_bp.route('/search/admin', methods=['GET'])
@jwt_required()
def admin_search():
    claims = get_jwt()
    if not claims.get("is_admin", False):
        return jsonify({"error": "Unauthorized"}), 403

    query = request.args.get("query", "").strip().lower()
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    results = []

    # Handle keywords that fetch all items
    if query in ["users", "user"]:
        users = User.query.all()
        results = [
            {"type": "user", "user_id": u.user_id, "name": u.full_name, "email": u.email}
            for u in users
        ]

    elif query in ["chapters", "chapter"]:
        chapters = Chapter.query.all()
        results = [
            {"type": "chapter", "subject_id": c.subject_id, "name": c.name, "description": c.description}
            for c in chapters
        ]
        
    elif query in ["subjects", "subject"]:
        subjects = Subject.query.all()
        results = [
            {"type": "subject", "subject_id": s.subject_id, "name": s.name, "description": s.description,"created_on":s.created_on}
            for s in subjects
        ]

    elif query in ["quizzes", "quiz"]:
        quizzes = Quiz.query.all()
        results = [
            {
                "type": "quiz",
                "quiz_id": q.quiz_id,
                "name": q.name,
                "chapter_id": q.chapter_id,
                "subject_id": q.chapter.subject.subject_id,
                "subject_name": q.chapter.subject.name
            }
            for q in quizzes
        ]

    elif query in ["questions", "question"]:
        questions = Question.query.all()
        results = [
            {"type": "question", "question_id": q.question_id, "question": q.question_statement}
            for q in questions
        ]

    else:
        # Free-text full search across all entities
        # Users
        users = User.query.filter(
            (User.full_name.ilike(f"%{query}%")) | (User.email.ilike(f"%{query}%"))
        ).all()
        for u in users:
            results.append({
                "type": "user",
                "user_id": u.user_id,
                "name": u.full_name,
                "email": u.email
            })

        # Subjects
        subjects = Subject.query.filter(
            (Subject.name.ilike(f"%{query}%")) | (Subject.description.ilike(f"%{query}%"))
        ).all()
        for s in subjects:
            results.append({
                "type": "subject",
                "subject_id": s.subject_id,
                "name": s.name,
                "description": s.description,
                "created_on":s.created_on
            })
            
        
        # Chapters
        chapters = Chapter.query.filter(
            (Chapter.name.ilike(f"%{query}%")) | (Chapter.description.ilike(f"%{query}%"))
        ).all()
        for c in chapters:
            results.append({
                "type": "chapter",
                "chapter_id": c.chapter_id,
                "name": c.name,
                "description": c.description,
                "subject_id":c.subject_id
                
            })

        # Quizzes
        quizzes = Quiz.query.filter(
            Quiz.name.ilike(f"%{query}%")
        ).all()
        for q in quizzes:
            results.append({
                "type": "quiz",
                "quiz_id": q.quiz_id,
                "name": q.name,
                "chapter_id": q.chapter_id,
                "subject_id": q.chapter.subject.subject_id,
                "subject_name": q.chapter.subject.name
            })

        # Questions
        questions = Question.query.filter(
            Question.question_statement.ilike(f"%{query}%")
        ).all()
        for q in questions:
            results.append({
                "type": "question",
                "question_id": q.question_id,
                "question": q.question_statement
            })

    return jsonify(results), 200

@admin_bp.route("/summary-report", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def admin_summary():
    total_users = User.query.filter_by(is_admin=False).count()
    total_quizzes = Quiz.query.count()
    total_subjects = Subject.query.count()
    total_attempts = Score.query.count()

    # Compose summary object
    summary = {
        "total_users": total_users,
        "total_quizzes": total_quizzes,
        "total_subjects": total_subjects,
        "total_attempts": total_attempts
    }

    # Prepare pseudo-score list to be reused in pie/line/bar charts in Vue
    scores = []

    # Pie chart: Quiz attempts by subject
    attempts_by_subject = (
        db.session.query(Subject.name, func.count(Score.score_id))
        .join(Subject.chapters)
        .join(Quiz, Quiz.chapter_id == Chapter.chapter_id)
        .join(Score, Score.quiz_id == Quiz.quiz_id)
        .group_by(Subject.name)
        .all()
    )
    for subject, attempts in attempts_by_subject:
        scores.append({
            "type": "subject_attempts",
            "label": subject,
            "value": attempts
        })

    # Bar chart: Quizzes per subject
    quizzes_by_subject = (
        db.session.query(Subject.name, func.count(Quiz.quiz_id))
        .join(Subject.chapters)
        .join(Quiz, Quiz.chapter_id == Chapter.chapter_id)
        .group_by(Subject.name)
        .all()
    )
    for subject, count in quizzes_by_subject:
        scores.append({
            "type": "subject_quizzes",
            "label": subject,
            "value": count
        })

    # Line chart: Attempts per day (last 7 days)
    last_7_days = datetime.utcnow() - timedelta(days=6)
    daily_attempts = (
        db.session.query(func.date(Score.time_stamp_of_attempt), func.count(Score.score_id))
        .filter(Score.time_stamp_of_attempt >= last_7_days)
        .group_by(func.date(Score.time_stamp_of_attempt))
        .order_by(func.date(Score.time_stamp_of_attempt))
        .all()
    )
    for date, count in daily_attempts:
        scores.append({
            "type": "daily_attempts",
            "label": date.strftime("%Y-%m-%d"),
            "value": count
        })

    return jsonify({
        "summary": summary,
        "scores": scores
    }), 200

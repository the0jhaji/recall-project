"""
RecallX - AI Memory Recall Assistant for Exams & Interviews
A hackathon-winning application using spaced repetition, forgetting curves, and stress-based recall testing.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
import math
import random
import os
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'recall-secret-key-change-in-production')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ==================== DATABASE MODELS ====================

class User(db.Model, UserMixin):
    """User model for storing user information"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    topics = db.relationship('Topic', backref='user', lazy=True, cascade='all, delete-orphan')
    recall_history = db.relationship('RecallHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)


class Topic(db.Model):
    """Topic model for storing study topics"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    topic_name = db.Column(db.String(200), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)  # semester, competitive, interview
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_revised = db.Column(db.DateTime, default=datetime.utcnow)
    strength = db.Column(db.Float, default=1.0)  # Memory strength (0-100)
    
    # FTI (Forgettable Topic Index) Components
    topic_complexity = db.Column(db.Float, default=5.0)  # 0-10 scale (abstract=high)
    topic_length = db.Column(db.Float, default=5.0)  # 0-10 scale (long=high)
    past_failures = db.Column(db.Integer, default=0)  # Count of failed recalls
    exam_frequency = db.Column(db.Float, default=5.0)  # 0-10 scale (common in exams)
    fti_score = db.Column(db.Float, default=5.0)  # Overall FTI (0-10)
    fti_category = db.Column(db.String(20), default='moderate')  # high, moderate, safe
    
    internet_content = db.relationship('InternetFetchedContent', backref='topic', lazy=True, cascade='all, delete-orphan')
    pdf_content = db.relationship('PDFExtractedContent', backref='topic', lazy=True, cascade='all, delete-orphan')
    questions = db.relationship('GeneratedQuestion', backref='topic', lazy=True, cascade='all, delete-orphan')
    forgetting_predictions = db.relationship('ForgettingPrediction', backref='topic', lazy=True, cascade='all, delete-orphan')


class InternetFetchedContent(db.Model):
    """Store content fetched from internet search"""
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    search_query = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PDFExtractedContent(db.Model):
    """Store extracted content from PDFs"""
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    filename = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class GeneratedQuestion(db.Model):
    """AI-generated questions for studying"""
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # short-answer, viva, prompt
    difficulty = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    recall_history = db.relationship('RecallHistory', backref='question', lazy=True, cascade='all, delete-orphan')


class RecallHistory(db.Model):
    """Track user's recall performance"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('generated_question.id'), nullable=False)
    user_answer = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=False)
    response_time = db.Column(db.Float)  # in seconds
    stress_level = db.Column(db.Integer, default=0)  # 0-100
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
    confidence = db.Column(db.Integer, default=0)  # User confidence level 0-100


class ForgettingPrediction(db.Model):
    """Store forgetting curve predictions"""
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    days_ahead = db.Column(db.Integer)
    retention_percentage = db.Column(db.Float)  # 0-100
    forget_probability = db.Column(db.Float)  # 0-1
    optimal_revision_date = db.Column(db.DateTime)
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== HELPER FUNCTIONS ====================

def get_or_create_default_user():
    """Get or create a default user for demo purposes"""
    user = User.query.filter_by(username='demo_user').first()
    if not user:
        user = User(username='demo_user', email='demo@recallx.app')
        db.session.add(user)
        db.session.commit()
    return user


def calculate_ebbinghaus_forgetting_curve(days_since_learning, strength=1.0):
    """
    Calculate retention based on Ebbinghaus Forgetting Curve
    Retention = exp(-t / strength)
    
    Args:
        days_since_learning: Days since the topic was learned
        strength: Memory strength factor (higher = better retention)
    
    Returns:
        Retention percentage (0-100)
    """
    if days_since_learning < 0:
        return 100.0
    
    # Ebbinghaus formula: R = e^(-t/S)
    # t = days since learning, S = strength factor (default ~2.5 days for weak memory)
    retention = math.exp(-days_since_learning / (strength * 2.5))
    return max(0, min(100, retention * 100))


def generate_questions_for_topic(topic_name, exam_type, count=5):
    """
    Generate AI questions based on topic (mock implementation with templates)
    """
    question_templates = {
        'short-answer': [
            f"What are the key principles of {topic_name}?",
            f"Explain the main differences in {topic_name}.",
            f"What are the applications of {topic_name}?",
            f"Describe the process of {topic_name}.",
            f"What is the significance of {topic_name}?",
        ],
        'viva': [
            f"Why is {topic_name} important in {exam_type} exams?",
            f"Can you elaborate on {topic_name}?",
            f"What challenges arise when understanding {topic_name}?",
            f"How would you approach a problem related to {topic_name}?",
            f"What common misconceptions exist about {topic_name}?",
        ],
        'prompt': [
            f"Quick recall: Define {topic_name}",
            f"Recall the formula/method for {topic_name}",
            f"What is the first thing you remember about {topic_name}?",
            f"Apply {topic_name} to a real-world scenario",
            f"Compare {topic_name} with similar concepts",
        ]
    }
    
    answers = [
        "This is a fundamental concept that requires understanding core principles.",
        "Multiple aspects contribute to understanding this topic.",
        "Practical applications vary based on context and domain.",
        "This process involves several key steps and considerations.",
        "This is a critical component for mastering the subject.",
    ]
    
    questions = []
    question_types = list(question_templates.keys())
    
    for i in range(count):
        q_type = question_types[i % len(question_types)]
        question = question_templates[q_type][i % len(question_templates[q_type])]
        answer = answers[i % len(answers)]
        questions.append({
            'question': question,
            'answer': answer,
            'type': q_type,
            'difficulty': random.choice(['easy', 'medium', 'hard'])
        })
    
    return questions


def mock_internet_search(query):
    """
    Mock internet search function (simulates API like SerpAPI)
    In production, would use BeautifulSoup + Requests or actual API
    """
    mock_results = {
        'Stack Exchange': "Stack Exchange is a network of question-and-answer websites. Common questions include implementation details, best practices, and edge cases.",
        'Data Structures': "Data structures are specialized formats for organizing data. Key types: Arrays, Linked Lists, Trees, Graphs, Hash Tables. Important for algorithm efficiency.",
        'Machine Learning': "Machine learning involves algorithms learning from data without explicit programming. Types: Supervised, Unsupervised, Reinforcement. Common applications: classification, regression, clustering.",
        'Web Development': "Modern web development uses HTML for structure, CSS for styling, JavaScript for interactivity. Frameworks: React, Vue, Angular. Backend: Node.js, Python, Java.",
        'Database Design': "Relational databases use tables and relationships. Key concepts: normalization, ACID properties, indexing. SQL: SELECT, INSERT, UPDATE, DELETE operations.",
        'API Design': "RESTful APIs use HTTP methods (GET, POST, PUT, DELETE). Design principles: statelessness, resource-based URLs, proper status codes. Common formats: JSON, XML.",
    }
    
    # Simple keyword matching
    found_results = []
    for key, value in mock_results.items():
        if any(word.lower() in query.lower() for word in key.split()):
            found_results.append({
                'title': key,
                'snippet': value,
                'url': f'https://example.com/{key.replace(" ", "-").lower()}'
            })
    
    # Return at least one result
    if not found_results:
        found_results = [{
            'title': 'General Information',
            'snippet': f'Information about {query}: This is a comprehensive topic covering multiple aspects and applications.',
            'url': 'https://example.com/general'
        }]
    
    return found_results


def extract_text_from_pdf(file_path):
    """
    Extract text from PDF file
    In production, would use PyPDF2
    For demo, returns mock content
    """
    return """
    Chapter 1: Introduction
    - Core concepts and definitions
    - Historical background
    - Key terminologies
    
    Chapter 2: Main Topics
    - Fundamental principles
    - Practical applications
    - Common use cases
    
    Chapter 3: Advanced Concepts
    - Deep dives into theory
    - Complex scenarios
    """


def calculate_forgettable_topic_index(topic):
    """
    Calculate Forgettable Topic Index (FTI) for a topic
    
    FTI combines multiple signals:
    - Topic complexity (0-10): Abstract topics score higher
    - Topic length (0-10): Longer content scores higher
    - Time since last revision (0-10): Older revisions score higher
    - Past recall failures (0-10): More failures score higher
    - Stress-based performance drop (0-10): Larger drops score higher
    - Exam frequency (0-10): More common in exams score higher
    
    Returns:
        fti_score (0-10): Higher = more forgettable
        category: 'high' (>7), 'moderate' (4-7), 'safe' (<4)
    """
    
    # Component 1: Topic Complexity (already in DB)
    complexity_weight = topic.topic_complexity * 0.15  # 15% weight
    
    # Component 2: Topic Length (already in DB)
    length_weight = topic.topic_length * 0.15  # 15% weight
    
    # Component 3: Time since last revision (0-10 scale)
    days_since_revised = (datetime.utcnow() - topic.last_revised).days
    time_decay = min(10, days_since_revised / 3)  # Max 10 at 30 days
    time_weight = time_decay * 0.20  # 20% weight
    
    # Component 4: Past recall failures
    failed_recalls = topic.past_failures
    failure_weight = min(10, failed_recalls * 1.5) * 0.20  # 20% weight
    
    # Component 5: Stress-based performance drop
    # Calculate from recall history if available
    all_recalls = RecallHistory.query.filter(
        RecallHistory.question_id.in_(
            [q.id for q in topic.questions]
        )
    ).all()
    
    stress_drop = 0
    if all_recalls:
        high_stress_correct = sum(1 for r in all_recalls if r.stress_level > 70 and r.is_correct)
        high_stress_total = sum(1 for r in all_recalls if r.stress_level > 70)
        low_stress_correct = sum(1 for r in all_recalls if r.stress_level <= 70 and r.is_correct)
        low_stress_total = sum(1 for r in all_recalls if r.stress_level <= 70)
        
        if low_stress_total > 0 and high_stress_total > 0:
            low_stress_accuracy = low_stress_correct / low_stress_total
            high_stress_accuracy = high_stress_correct / high_stress_total
            stress_drop = (low_stress_accuracy - high_stress_accuracy) * 10
    
    stress_weight = max(0, min(10, stress_drop)) * 0.15  # 15% weight
    
    # Component 6: Exam frequency (already in DB)
    exam_weight = topic.exam_frequency * 0.15  # 15% weight
    
    # Calculate FTI Score
    fti_score = (complexity_weight + length_weight + time_weight + 
                 failure_weight + stress_weight + exam_weight)
    
    fti_score = max(0, min(10, fti_score))  # Clamp to 0-10
    
    # Categorize
    if fti_score >= 7:
        category = 'high'
    elif fti_score >= 4:
        category = 'moderate'
    else:
        category = 'safe'
    
    return fti_score, category


def update_topic_fti(topic):
    """Update a topic's FTI score and category"""
    fti_score, category = calculate_forgettable_topic_index(topic)
    topic.fti_score = fti_score
    topic.fti_category = category
    db.session.commit()
    return fti_score, category


# ==================== FLASK-LOGIN SETUP ====================

@login_manager.user_loader
def load_user(user_id):
    """Load user from database"""
    return User.query.get(int(user_id))


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=bool(remember))
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard showing topics ranked by Forgettable Topic Index"""
    user = current_user
    topics = Topic.query.filter_by(user_id=user.id).all()
    
    # Update FTI scores for all topics
    for topic in topics:
        update_topic_fti(topic)
    
    # Sort by FTI (most forgettable first)
    topics_by_fti = sorted(topics, key=lambda t: t.fti_score, reverse=True)
    
    # Create alerts for high-FTI topics
    alerts = []
    for topic in topics_by_fti:
        if topic.fti_category == 'high':
            alerts.append({
                'topic': topic.topic_name,
                'message': f'⚠️ {topic.topic_name} has HIGH forgettability! Focus on stress training.',
                'severity': 'high',
                'fti_score': topic.fti_score
            })
        elif topic.fti_category == 'moderate':
            # Add one sample moderate alert
            if len([a for a in alerts if a['severity'] == 'medium']) == 0:
                alerts.append({
                    'topic': topic.topic_name,
                    'message': f'📌 {topic.topic_name} has MODERATE forgettability. Regular practice needed.',
                    'severity': 'medium',
                    'fti_score': topic.fti_score
                })
    
    return render_template('dashboard.html', topics=topics_by_fti, alerts=alerts)


@app.route('/add-topic')
@login_required
def add_topic_page():
    """Add topic page"""
    return render_template('add_topic.html')


@app.route('/upload')
@login_required
def upload_page():
    """PDF upload page"""
    return render_template('upload.html')


@app.route('/forgetting-curve/<int:topic_id>')
@login_required
def forgetting_curve_page(topic_id):
    """Forgetting curve visualization page"""
    topic = Topic.query.get(topic_id)
    if not topic or topic.user_id != current_user.id:
        return "Unauthorized", 403
    return render_template('forgetting_curve.html', topic=topic)


@app.route('/stress-test/<int:topic_id>')
@login_required
def stress_test_page(topic_id):
    """Stress recall test page"""
    topic = Topic.query.get(topic_id)
    if not topic or topic.user_id != current_user.id:
        return "Unauthorized", 403
    return render_template('stress_test.html', topic=topic)


@app.route('/report')
@login_required
def report_page():
    """Performance report page"""
    return render_template('report.html')


# ==================== API ENDPOINTS ====================

@app.route('/api/add-topic', methods=['POST'])
@login_required
def api_add_topic():
    """API: Add a new topic"""
    try:
        user = current_user
        data = request.json
        
        topic = Topic(
            user_id=user.id,
            subject=data.get('subject'),
            topic_name=data.get('topic_name'),
            exam_type=data.get('exam_type'),
            description=data.get('description', ''),
            strength=1.0
        )
        
        db.session.add(topic)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Topic added successfully',
            'topic_id': topic.id,
            'topic_name': topic.topic_name
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/search-topic', methods=['POST'])
@login_required
def api_search_topic():
    """API: Search for topic information on the internet"""
    try:
        user = current_user
        data = request.json
        topic_id = data.get('topic_id')
        search_query = data.get('search_query', data.get('topic_name', ''))
        
        topic = Topic.query.get(topic_id)
        if not topic or topic.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Topic not found'}), 404
        
        # Mock internet search
        search_results = mock_internet_search(search_query)
        
        # Store search results
        for result in search_results:
            internet_content = InternetFetchedContent(
                topic_id=topic_id,
                search_query=search_query,
                content=result['snippet'],
                source_url=result['url']
            )
            db.session.add(internet_content)
        
        # Generate questions based on search
        questions = generate_questions_for_topic(topic.topic_name, topic.exam_type)
        for q in questions:
            generated_q = GeneratedQuestion(
                topic_id=topic_id,
                question=q['question'],
                answer=q['answer'],
                question_type=q['type'],
                difficulty=q['difficulty']
            )
            db.session.add(generated_q)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Topic researched and questions generated',
            'search_results': search_results,
            'questions_generated': len(questions)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/upload-pdf', methods=['POST'])
@login_required
def api_upload_pdf():
    """API: Upload and parse PDF"""
    try:
        user = get_or_create_default_user()
        topic_id = request.form.get('topic_id')
        
        topic = Topic.query.get(topic_id)
        if not topic:
            return jsonify({'success': False, 'error': 'Topic not found'}), 404
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Mock PDF extraction
        extracted_text = extract_text_from_pdf(file.filename)
        
        pdf_content = PDFExtractedContent(
            topic_id=topic_id,
            filename=file.filename,
            content=extracted_text
        )
        
        db.session.add(pdf_content)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'PDF processed successfully',
            'extracted_text_preview': extracted_text[:200] + '...'
        }), 201
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/generate-questions/<int:topic_id>', methods=['GET'])
@login_required
def api_generate_questions(topic_id):
    """API: Generate questions for a topic"""
    try:
        topic = Topic.query.get(topic_id)
        if not topic or topic.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Topic not found'}), 404
        
        # Get existing or generate new questions
        questions = GeneratedQuestion.query.filter_by(topic_id=topic_id).all()
        
        if not questions:
            # Generate if none exist
            q_data = generate_questions_for_topic(topic.topic_name, topic.exam_type, count=10)
            for q in q_data:
                generated_q = GeneratedQuestion(
                    topic_id=topic_id,
                    question=q['question'],
                    answer=q['answer'],
                    question_type=q['type'],
                    difficulty=q['difficulty']
                )
                db.session.add(generated_q)
            db.session.commit()
            questions = GeneratedQuestion.query.filter_by(topic_id=topic_id).all()
        
        questions_data = [{
            'id': q.id,
            'question': q.question,
            'answer': q.answer,
            'type': q.question_type,
            'difficulty': q.difficulty
        } for q in questions]
        
        return jsonify({
            'success': True,
            'questions': questions_data,
            'count': len(questions_data)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/forgetting-curve/<int:topic_id>', methods=['GET'])
@login_required
def api_forgetting_curve(topic_id):
    """API: Get forgetting curve data for visualization"""
    try:
        topic = Topic.query.get(topic_id)
        if not topic or topic.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Topic not found'}), 404
        
        # Generate curve data for next 30 days
        curve_data = []
        for day in range(0, 31):
            retention = calculate_ebbinghaus_forgetting_curve(day, topic.strength)
            curve_data.append({
                'day': day,
                'retention': round(retention, 2),
                'forget_probability': round(100 - retention, 2)
            })
        
        # Find optimal revision dates
        optimal_dates = []
        for day in [1, 3, 7, 14, 30]:
            optimal_dates.append({
                'day': day,
                'date': (datetime.utcnow() + timedelta(days=day)).strftime('%Y-%m-%d'),
                'retention': round(calculate_ebbinghaus_forgetting_curve(day, topic.strength), 2)
            })
        
        return jsonify({
            'success': True,
            'topic_name': topic.topic_name,
            'topic_strength': topic.strength,
            'curve_data': curve_data,
            'optimal_dates': optimal_dates
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/stress-test', methods=['POST'])
@login_required
def api_stress_test():
    """API: Submit stress test results"""
    try:
        user = current_user
        data = request.json
        
        question_id = data.get('question_id')
        user_answer = data.get('user_answer')
        response_time = data.get('response_time')
        stress_level = data.get('stress_level', 0)
        confidence = data.get('confidence', 0)
        correct_answer = data.get('correct_answer', '')
        
        # Simple answer checking (keyword matching)
        is_correct = any(word in user_answer.lower() for word in correct_answer.lower().split())
        
        recall = RecallHistory(
            user_id=user.id,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=is_correct,
            response_time=response_time,
            stress_level=stress_level,
            confidence=confidence
        )
        
        db.session.add(recall)
        db.session.commit()
        
        # Update topic strength based on performance
        question = GeneratedQuestion.query.get(question_id)
        if question:
            topic = question.topic
            # Boost strength if correct, reduce if wrong
            factor = 0.95 if is_correct else 1.05
            topic.strength = min(5.0, max(0.5, topic.strength * factor))
            topic.last_revised = datetime.utcnow()
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Response recorded',
            'is_correct': is_correct,
            'accuracy_feedback': f'{"Correct!" if is_correct else "Incorrect. "} Response time: {response_time:.1f}s'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/report', methods=['GET'])
@login_required
def api_report():
    """API: Get comprehensive performance report"""
    try:
        user = get_or_create_default_user()
        topics = Topic.query.filter_by(user_id=user.id).all()
        
        report_data = {
            'total_topics': len(topics),
            'total_strength': 0,
            'average_accuracy': 0,
            'topics': [],
            'alerts': []
        }
        
        total_correct = 0
        total_attempts = 0
        
        for topic in topics:
            days_since = (datetime.utcnow() - topic.last_revised).days
            retention = calculate_ebbinghaus_forgetting_curve(days_since, topic.strength)
            
            # Get performance for this topic
            recalls = RecallHistory.query.filter(
                RecallHistory.question_id.in_(
                    db.session.query(GeneratedQuestion.id).filter_by(topic_id=topic.id)
                )
            ).all()
            
            correct = sum(1 for r in recalls if r.is_correct)
            total_correct += correct
            total_attempts += len(recalls)
            
            topic_data = {
                'topic_name': topic.topic_name,
                'subject': topic.subject,
                'exam_type': topic.exam_type,
                'strength': round(topic.strength, 2),
                'retention': round(retention, 2),
                'accuracy': round(correct / len(recalls) * 100, 1) if recalls else 0,
                'attempts': len(recalls),
                'last_revised': topic.last_revised.strftime('%Y-%m-%d %H:%M')
            }
            report_data['topics'].append(topic_data)
            
            # Add to alerts if weak
            if retention < 50:
                report_data['alerts'].append({
                    'topic': topic.topic_name,
                    'message': f'Weak recall strength: {retention:.0f}% retention',
                    'action': 'Schedule revision immediately'
                })
        
        report_data['total_strength'] = round(sum(t['strength'] for t in report_data['topics']) / len(topics) if topics else 0, 2)
        report_data['average_accuracy'] = round(total_correct / total_attempts * 100, 1) if total_attempts > 0 else 0
        
        # Calculate readiness score
        readiness_score = min(100, report_data['average_accuracy'] * report_data['total_strength'])
        report_data['readiness_score'] = round(readiness_score, 1)
        report_data['readiness_status'] = 'Ready!' if readiness_score >= 75 else 'Needs Practice' if readiness_score >= 50 else 'Not Ready'
        
        return jsonify({
            'success': True,
            'report': report_data
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/topics', methods=['GET'])
@login_required
def api_get_topics():
    """API: Get all topics for current user"""
    try:
        user = get_or_create_default_user()
        topics = Topic.query.filter_by(user_id=user.id).all()
        
        topics_data = [{
            'id': t.id,
            'subject': t.subject,
            'topic_name': t.topic_name,
            'exam_type': t.exam_type,
            'strength': t.strength,
            'created_at': t.created_at.strftime('%Y-%m-%d')
        } for t in topics]
        
        return jsonify({
            'success': True,
            'topics': topics_data,
            'count': len(topics_data)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/forgettable-topics', methods=['GET'])
@login_required
def api_get_forgettable_topics():
    """API: Get topics ranked by Forgettable Topic Index (FTI)"""
    try:
        user = get_or_create_default_user()
        topics = Topic.query.filter_by(user_id=user.id).all()
        
        # Update FTI scores for all topics
        for topic in topics:
            update_topic_fti(topic)
        
        # Sort by FTI score (descending)
        sorted_topics = sorted(topics, key=lambda t: t.fti_score, reverse=True)
        
        topics_data = [{
            'id': t.id,
            'topic_name': t.topic_name,
            'subject': t.subject,
            'exam_type': t.exam_type,
            'fti_score': round(t.fti_score, 2),
            'fti_category': t.fti_category,
            'complexity': round(t.topic_complexity, 2),
            'length': round(t.topic_length, 2),
            'exam_frequency': round(t.exam_frequency, 2),
            'past_failures': t.past_failures,
            'days_since_revised': (datetime.utcnow() - t.last_revised).days,
            'created_at': t.created_at.strftime('%Y-%m-%d')
        } for t in sorted_topics]
        
        # Count by category
        high_count = sum(1 for t in sorted_topics if t.fti_category == 'high')
        moderate_count = sum(1 for t in sorted_topics if t.fti_category == 'moderate')
        safe_count = sum(1 for t in sorted_topics if t.fti_category == 'safe')
        
        return jsonify({
            'success': True,
            'topics': topics_data,
            'statistics': {
                'high_forgettable': high_count,
                'moderately_forgettable': moderate_count,
                'safe_topics': safe_count,
                'total': len(sorted_topics)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ==================== DATABASE INITIALIZATION ====================

def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if sample data exists
        user = User.query.filter_by(username='demo_user').first()
        if not user:
            # Create demo user with password
            user = User(username='demo_user', email='demo@recallx.app')
            user.set_password('demo_password_123')  # Hash the password
            db.session.add(user)
            db.session.commit()
            
            # Create sample topics with FTI characteristics
            sample_topics = [
                {
                    'subject': 'Data Structures',
                    'topic_name': 'Binary Trees',
                    'exam_type': 'competitive',
                    'description': 'Understanding tree traversal and binary search trees',
                    'complexity': 8.5,  # Very abstract
                    'length': 7.0,  # Medium-long
                    'exam_frequency': 9.0,  # Very common in exams
                    'past_failures': 3
                },
                {
                    'subject': 'Machine Learning',
                    'topic_name': 'Neural Networks',
                    'exam_type': 'interview',
                    'description': 'Deep learning fundamentals and backpropagation',
                    'complexity': 9.0,  # Highly abstract
                    'length': 8.5,  # Very long
                    'exam_frequency': 8.5,  # Common in interviews
                    'past_failures': 2
                },
                {
                    'subject': 'Web Development',
                    'topic_name': 'REST APIs',
                    'exam_type': 'interview',
                    'description': 'RESTful architecture and API design principles',
                    'complexity': 5.0,  # Moderate abstraction
                    'length': 5.5,  # Medium
                    'exam_frequency': 7.0,  # Common
                    'past_failures': 0
                }
            ]
            
            for topic_data in sample_topics:
                topic = Topic(
                    user_id=user.id,
                    subject=topic_data['subject'],
                    topic_name=topic_data['topic_name'],
                    exam_type=topic_data['exam_type'],
                    description=topic_data['description'],
                    strength=random.uniform(1.0, 3.0),
                    topic_complexity=topic_data['complexity'],
                    topic_length=topic_data['length'],
                    exam_frequency=topic_data['exam_frequency'],
                    past_failures=topic_data['past_failures']
                )
                db.session.add(topic)
                db.session.commit()
                
                # Calculate and store FTI
                fti_score, fti_category = calculate_forgettable_topic_index(topic)
                topic.fti_score = fti_score
                topic.fti_category = fti_category
                db.session.commit()
                
                # Generate sample questions
                questions = generate_questions_for_topic(topic.topic_name, topic.exam_type, count=8)
                for q in questions:
                    generated_q = GeneratedQuestion(
                        topic_id=topic.id,
                        question=q['question'],
                        answer=q['answer'],
                        question_type=q['type'],
                        difficulty=q['difficulty']
                    )
                    db.session.add(generated_q)
                
                db.session.commit()


if __name__ == '__main__':
    init_database()
    app.run(debug=True, port=5000)

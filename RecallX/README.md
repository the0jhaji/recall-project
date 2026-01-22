# RecallX – AI Memory Recall Assistant for Exams & Interviews

> **🔥 v2 UPDATE:** RecallX now features **Forgettable Topic Index (FTI)** - an intelligent system that identifies which topics you'll actually forget. See [FTI_UPGRADE.md](FTI_UPGRADE.md) for details!

![RecallX Banner](static/images/banner.png)

## 🎯 The Problem

Students spend countless hours studying but forget critical information during exams and interviews due to:
- Poor recall timing
- Lack of stress-based training
- No feedback on weak areas
- **Inability to identify genuinely-forgettable topics**

## ✨ The Solution

**RecallX** uses AI-powered spaced repetition, Ebbinghaus forgetting curve prediction, stress-based recall simulation, AND **Forgettable Topic Index (FTI)** to help students master information under pressure.

## 🚀 Key Features

### 1. **Smart Topic Input with AI Search**
- Add topics with subject, exam type, and description
- AI automatically searches the internet for exam-relevant questions
- Extracts important subtopics and commonly asked concepts

### 2. **PDF Upload & Content Extraction**
- Upload syllabi or notes in PDF format
- System extracts key concepts automatically
- Merges PDF content with AI research for comprehensive coverage

### 3. **AI-Generated Question Bank**
- Auto-generates short-answer, viva, and interview questions
- Questions are exam-oriented and stress-test friendly
- Questions stored per topic for organized study

### 4. **Ebbinghaus Forgetting Curve Prediction**
- Implements the scientifically-proven forgetting curve formula
- Predicts forget probability and optimal revision times
- Visualizes retention over 30 days with Chart.js
- Highlights danger zones in red for immediate action

### 5. **Stress Recall Mode** (The Game-Changer)
- Full-screen, distraction-free testing environment
- Dark theme to simulate pressure
- Countdown timer with increasing stress
- Random questions with time pressure
- Measures: accuracy, response time, stress level, confidence
- Real-time stress indicator showing cognitive load

### 6. **Smart Memory Alerts**
- Context-aware reminders like "You will forget 70% of Binary Trees by tomorrow"
- Triggered when retention drops below threshold
- Helps users plan revision proactively

### 7. **Comprehensive Performance Report**
- Topic-wise recall strength analysis
- Accuracy metrics under stress
- Weak vs strong areas identification
- Overall exam/interview readiness score
- Actionable recommendations

## 🏗️ Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Charts**: Chart.js 3.9
- **PDF Parsing**: PyPDF2
- **Web Requests**: Requests + BeautifulSoup4
- **ORM**: SQLAlchemy

## 📋 Project Structure

```
RecallX/
├── app.py                      # Flask application with all routes and APIs
├── database.db                 # SQLite database (auto-created)
├── requirements.txt            # Python dependencies
├── templates/
│   ├── index.html             # Landing page
│   ├── dashboard.html         # Topic overview & alerts
│   ├── add_topic.html         # Create new topic with AI search
│   ├── upload.html            # PDF upload & extraction
│   ├── forgetting_curve.html  # Memory retention visualization
│   ├── stress_test.html       # High-pressure recall test
│   └── report.html            # Performance analytics & readiness
├── static/
│   ├── css/style.css          # Complete responsive styling
│   └── js/
│       ├── dashboard.js       # Dashboard interactions
│       ├── search.js          # Topic creation & AI search
│       ├── stress.js          # Stress test logic
│       └── chart.js           # Forgetting curve visualization
```

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to project directory**
   ```bash
   cd RecallX
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access in browser**
   ```
   http://localhost:5000
   ```

## 🎬 Demo Walkthrough (2 Minutes)

### Step 1: View Landing Page
- Open http://localhost:5000
- See the problem-solution framework
- Click "Start Now" or "Go to Dashboard"

### Step 2: Explore Dashboard with Sample Data
- Dashboard loads with 3 pre-created topics:
  - Binary Trees (Data Structures, Competitive Exam)
  - Neural Networks (ML, Interview)
  - REST APIs (Web Dev, Interview)
- See memory alerts for each topic
- Each topic shows strength meter

### Step 3: View Forgetting Curve
- Click "📊 Forgetting Curve" on any topic
- Interactive Chart.js visualization shows:
  - Memory retention over 30 days
  - Optimal revision schedule
  - Your topic strength factor
- Learn why spaced repetition matters

### Step 4: Take Stress Test
- Click "🧠 Stress Test" on any topic
- Experience:
  - 5-minute countdown timer
  - Increasing stress level indicator
  - 10 random questions from topic
  - Confidence selection (Low/Medium/High/Very Sure)
  - Dark theme simulating pressure
  - Real-time accuracy feedback
- Results show: accuracy %, response time, confidence level

### Step 5: Create New Topic
- Click "+ Add Topic"
- Fill form:
  - Subject: "Artificial Intelligence"
  - Topic: "Neural Networks"
  - Exam Type: "Competitive"
- System automatically:
  - Searches internet for exam questions
  - Generates practice questions
  - Shows research results
- See success message with question count

### Step 6: View Performance Report
- Click "Report" in navigation
- See comprehensive metrics:
  - Exam readiness score (0-100)
  - Topic-wise performance table
  - Weak areas needing attention
  - Personalized recommendations
  - Readiness status: Ready / Needs Practice / Not Ready

### Step 7: Optional - Upload PDF
- Click "Upload PDF"
- Select a topic
- Upload any PDF (mock extraction for demo)
- Content automatically extracted and merged

## 📊 Database Schema

### Users
- `id`, `username`, `email`, `created_at`

### Topics
- `id`, `user_id`, `subject`, `topic_name`, `exam_type`
- `description`, `created_at`, `last_revised`
- `strength` (0-5, memory strength factor)

### InternetFetchedContent
- `id`, `topic_id`, `search_query`, `content`, `source_url`, `created_at`

### PDFExtractedContent
- `id`, `topic_id`, `filename`, `content`, `uploaded_at`

### GeneratedQuestions
- `id`, `topic_id`, `question`, `answer`
- `question_type` (short-answer/viva/prompt)
- `difficulty` (easy/medium/hard)
- `created_at`

### RecallHistory
- `id`, `user_id`, `question_id`, `user_answer`
- `is_correct`, `response_time`, `stress_level`
- `attempted_at`, `confidence`

### ForgettingPredictions
- `id`, `topic_id`, `days_ahead`, `retention_percentage`
- `forget_probability`, `optimal_revision_date`, `calculated_at`

## 🔬 The Science Behind RecallX

### Ebbinghaus Forgetting Curve
The app implements the scientifically-proven Ebbinghaus formula:

$$R(t) = e^{-t/S}$$

Where:
- R(t) = Retention percentage at time t
- t = Days since learning
- S = Strength factor (higher = better retention)

### Spaced Repetition Strategy
RecallX recommends revision at optimal intervals:
- Day 1: Initial recall (consolidation)
- Day 3: Before 70% is forgotten
- Day 7: Counter exponential decay
- Day 14: Long-term memory transfer
- Day 30: Final reinforcement

### Stress-Based Recall Testing
Research shows recall under pressure improves long-term retention:
- Countdown timer increases cognitive load
- Sudden questions simulate exam conditions
- Confidence levels correlate with retention

## 🎨 UI/UX Highlights

### Landing Page
- Problem-Solution framework clearly explained
- Feature cards with icons
- Step-by-step how-it-works guide
- Strong CTA buttons

### Dashboard
- Light, clean theme for calm study environment
- Visual alerts for weak topics
- Topic cards with strength meters
- Quick access to forgetting curve and stress test

### Stress Test Mode
- Dark theme to simulate exam pressure
- Large timer display with urgency
- Real-time stress level indicator
- Full-screen distraction-free interface
- Immediate feedback on answers

### Performance Report
- Color-coded retention status
- Comprehensive statistics
- Actionable recommendations
- Professional analytics layout

## 🚀 Performance Optimizations

- Lightweight vanilla JavaScript (no frameworks)
- Efficient SQLite queries with proper indexing
- Chart.js for fast rendering
- Responsive CSS Grid layout
- Minimal external dependencies

## 🔐 Security

- SQLite local database (no cloud)
- No sensitive data transmission
- CSRF protection ready
- Input validation on forms

## 🛠️ API Endpoints

All APIs are RESTful and return JSON:

```
POST   /api/add-topic           # Create new topic
POST   /api/search-topic        # Search internet & generate questions
POST   /api/upload-pdf          # Upload and extract PDF
GET    /api/generate-questions/<topic_id>
GET    /api/forgetting-curve/<topic_id>
POST   /api/stress-test         # Submit test response
GET    /api/report              # Get performance metrics
GET    /api/topics              # List all topics
```

## 💡 Hackathon Demo Highlights

✅ **Complete solution** - All 7 required pages fully functional
✅ **Working backend** - All APIs implemented with mock data
✅ **Beautiful UI** - Professional dark/light themes
✅ **Real algorithms** - Ebbinghaus forgetting curve
✅ **Sample data** - 3 pre-populated topics for instant demo
✅ **Stress simulation** - Dark mode + timer + pressure
✅ **No external APIs** - Mock internet search included
✅ **Responsive design** - Works on mobile and desktop
✅ **Under 2 minute demo** - Quick walkthrough possible
✅ **Clean code** - Well-commented, maintainable

## 🎯 Future Enhancements

- [ ] Real internet search with SerpAPI
- [ ] Actual PDF parsing with OCR
- [ ] User authentication & multi-user support
- [ ] Mobile app (React Native)
- [ ] Email reminders for optimal revision
- [ ] Collaborative study groups
- [ ] Integration with learning platforms (Coursera, Udemy)
- [ ] AI-powered answer evaluation
- [ ] Spaced repetition algorithm optimization
- [ ] Analytics dashboard for educators

## 📞 Support

For questions or issues:
1. Check the README.md
2. Review app.py comments
3. Check browser console for JavaScript errors
4. Ensure Python 3.8+ and dependencies installed

## 📄 License

This project is built for educational purposes and hackathon demonstration.

---

**RecallX - Master Information Under Pressure** 🧠💪

Built with ❤️ for hackers who want to solve real problems in education.

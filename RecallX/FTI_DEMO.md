# 🎬 RecallX v2 FTI Demo Script (2 Minutes)

**Target Audience:** Hackathon Judges  
**Setup Time:** 10 seconds (server already running)  
**Demo Time:** ~2 minutes  
**Goal:** Show intelligent forgettability prediction system  

---

## Pre-Demo Setup

✅ Flask server running on `http://localhost:5000`  
✅ Database initialized with 3 sample topics (with FTI values)  
✅ Dashboard loaded and ready  

---

## Demo Flow

### [0:00-0:10] LANDING PAGE

**Action:** Open http://localhost:5000  
**What They See:** Beautiful problem-solution framework

**Talking Points:**
- "Students forget critical topics under exam pressure"
- "RecallX identifies which topics are most forgettable using AI"
- "We don't just predict time-based forgetting—we predict actual forgettability"

---

### [0:10-0:35] DASHBOARD - THE MAGIC ✨

**Action:** Click "Go to Dashboard" button

**What They See:**
- 3-tier categorized view (RED/YELLOW/GREEN)
- FTI scores on each card (8.1/10, 8.6/10, 5.8/10)
- Visual component breakdown (complexity, length, exam frequency)
- Smart alerts for HIGH-FTI topics

**Talking Points:**

"This is our Forgettable Topic Index dashboard. Notice something different?

**[Point to RED section]** These are HIGH forgettability topics. Binary Trees (8.1/10) and Neural Networks (8.6/10).

Why are they so high?
- **Binary Trees:** Very abstract concept, medium-long content, extremely common in exams
- **Neural Networks:** Even MORE abstract, very long to learn, critical for interviews

Our algorithm weighs 6 factors:
1. **Complexity** - How abstract? (Trees = very abstract)
2. **Length** - How much content? (ML = tons of theory)
3. **Time** - How long since you studied it?
4. **Failures** - Did you fail recalls on this? (3 failures = high FTI)
5. **Stress** - Does pressure kill your accuracy?
6. **Exam Frequency** - How often in exams? (Binary Trees = every time)

**[Point to YELLOW section]** REST APIs is moderate. It's practical, so it's easier to recall even under stress.

**[Point to alerts]** These smart alerts only trigger for HIGH-FTI topics. We don't bombard students—we guide them."

---

### [0:35-0:55] OPEN A HIGH-FTI TOPIC

**Action:** Click on "Binary Trees" card → Click "Stress Test" button

**What They See:**
- Full-screen dark interface (high-pressure environment)
- Timer: "5:00" countdown
- Stress indicator bar
- Question randomized from high-FTI questions
- Confidence selector (Low/Medium/High/Very High)

**Talking Points:**

"Now here's where it gets serious. When you have a HIGH-FTI topic, you don't just review—you practice under PRESSURE.

- **Dark interface**: Simulates exam room pressure
- **Countdown timer**: Creates real time anxiety
- **Stress indicator**: Shows your panic level
- **Questions prioritized**: The system gives you MORE questions on high-FTI topics
- **Confidence tracking**: We measure if pressure affects your accuracy

This is where most students freeze. Our system forces you to practice that freezing, so you're ready."

---

### [0:55-1:15] SHOW STRESS TEST IN ACTION

**Action:** Answer 2-3 questions, select confidence level, submit

**What They See:**
- Question appears
- You type answer
- Select confidence
- Submit → Gets feedback (correct/incorrect)
- Stress level updates
- Next question appears

**Talking Points:**

"See the stress level climbing? That's realistic exam pressure.

Our algorithm tracks:
- **Accuracy under stress**: Do you perform worse?
- **Response time**: Are you slower when stressed?
- **Confidence calibration**: Do you know which answers are right?

This data feeds back into the FTI calculation. If Neural Networks tank your accuracy under pressure, next time it gets an EVEN HIGHER FTI score. The system learns what genuinely breaks your recall."

---

### [1:15-1:30] PERFORMANCE REPORT

**Action:** Finish test → View results → Go back to dashboard

**Talking Points:**

"After stress testing, your performance is tracked. Let me show you the report page..."

**[Navigate to /report if available, or explain]**

"Your report shows:
- **Readiness score**: Overall exam preparation (0-100)
- **Performance by topic**: Which ones did you nail, which ones tanked
- **Forgettability analysis**: How well you handled high-FTI topics
- **Weak areas identified**: Which combinations of (difficulty + stress) break you
- **Recommendations**: 'Practice more on Binary Trees under time pressure'"

---

### [1:30-1:50] THE INTELLIGENCE LAYER

**Action:** Go back to Dashboard, show how dashboard updates (or explain the cycle)

**Talking Points:**

"Here's the beautiful part: **The system learns from your performance.**

Every time you:
1. Take a stress test
2. Get questions wrong
3. Show stress-based performance drop
4. Practice a topic

...the FTI score gets recalculated. It learns:
- 'Ah, Binary Trees doesn't just theoretically break you—it actually DOES break you under pressure'
- 'Neural Networks is getting easier, lower FTI next time'
- 'REST APIs you're solid on, maintain it'

This is **personalized forgettability prediction**. Not generic. Not one-size-fits-all. Adaptive and intelligent."

---

### [1:50-2:00] CLOSING PITCH

**Talking Points:**

"So why is this different?

**Old way:** 'You learned this 5 days ago, time to revise'  
**RecallX way:** 'Binary Trees is abstract, long, commonly tested, AND you fail under pressure—URGENT STRESS TRAINING NEEDED'

We don't just predict memory decay. We predict **actual exam failure risk**.

Students don't need more study time. They need smarter study direction. And that's what RecallX provides—an intelligent system that says:

**'Study these (RED), maintain these (GREEN), and practice these under pressure (YELLOW)'**

That's personalized, actionable, and scientifically-grounded. And it's wrapped in a beautiful, student-friendly interface.

Thank you!"

---

## Judge Questions You Might Get

### Q: "This seems just like categorizing difficulty?"
**A:** "No, it's different. Difficulty is static. FTI is dynamic. We calculate based on YOUR past failures, YOUR stress-performance correlation, plus topic complexity. Student A might find Neural Networks manageable (FTI 6), but Student B might find it horrifying (FTI 9). It's personalized."

### Q: "How do you actually measure 'abstractness' of a topic?"
**A:** "In the demo, the user or admin inputs it (0-10 scale). In production, we'd use NLP to analyze content—if a topic uses lots of formal definitions and lacks concrete examples, it's abstract. We're keeping it simple for the hackathon."

### Q: "What about the 'stress impact' calculation?"
**A:** "We compare accuracy when stress_level < 50 vs stress_level > 70. If accuracy drops 40%, that's a huge multiplier on FTI. It means the student genuinely fails under pressure on that topic."

### Q: "This could be valuable for educators too?"
**A:** "Absolutely! A teacher could upload a syllabus, and RecallX would identify which concepts their students typically struggle with under pressure. Then focus teaching on those areas with more interactive, pressure-building exercises."

### Q: "What's the real-world impact?"
**A:** "In a 3-month exam prep: Student A wastes 30% of time on safe topics. Student B uses RecallX, focuses on high-FTI topics with targeted stress training, gets 15% better exam score. That's real impact for millions of students."

---

## Tech Stack (Mention If Asked)

- **Backend:** Python Flask (lightweight, fast)
- **Frontend:** Vanilla JS, HTML5, CSS3 (no bloat)
- **Database:** SQLite (local, no dependencies)
- **Visualization:** Chart.js (forgetting curve + FTI breakdown)
- **Algorithm:** Multi-factor weighted scoring (transparent, interpretable)

---

## Closing Note

**"RecallX v2 isn't about MORE features. It's about SMARTER features. We identified a real problem (students don't know what to prioritize) and built an intelligent solution that's backed by learning science, personalized to each student, and easy to understand. That's hackathon gold."**

---

**Demo time complete! You nailed it! 🏆**

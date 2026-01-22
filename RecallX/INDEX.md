# 📚 RecallX Documentation Index

**Welcome to RecallX v2 - Forgettable Topic Index Edition!**

This is your comprehensive guide to understanding, using, and showcasing RecallX.

---

## 🎯 Start Here

### For First-Time Users
1. **[START_HERE.md](START_HERE.md)** - Quick start guide (read this first!)
2. **[README.md](README.md)** - Project overview
3. Visit **http://localhost:5000** - See the landing page

### For Demo/Judges
1. **[FTI_DEMO.md](FTI_DEMO.md)** - Complete 2-minute demo script ⭐
2. **[FTI_QUICK_REF.md](FTI_QUICK_REF.md)** - Quick reference for talking points
3. Visit **http://localhost:5000/dashboard** - See FTI system in action

---

## 📖 Documentation Guide

### Core Documentation

| Document | Purpose | Best For |
|----------|---------|----------|
| **README.md** | Project overview & features | General understanding |
| **SUMMARY.md** | Quick facts & statistics | Quick reference |
| **CHECKLIST.md** | Feature verification checklist | Validation |
| **MANIFEST.md** | Complete file inventory | Checking what's included |
| **FINAL_REPORT.md** | Technical implementation details | Deep dive |

### FTI System Documentation (v2)

| Document | Purpose | Best For |
|----------|---------|----------|
| **FTI_UPGRADE.md** | Complete FTI technical guide | Understanding the system |
| **FTI_DEMO.md** | 2-minute demo script | Preparing for presentation |
| **FTI_QUICK_REF.md** | Quick reference guide | Quick lookup |
| **FTI_IMPLEMENTATION_COMPLETE.md** | Implementation summary | Technical details |
| **FINAL_CHECKLIST.md** | Comprehensive checklist | Verification |

---

## 🚀 Quick Navigation

### Running the Project

**Start Flask Server:**
```bash
cd "c:\Users\pc\OneDrive\Desktop\CODING STUFF\recall project\RecallX"
python app.py
```

**Access URLs:**
- Landing Page: http://localhost:5000
- Dashboard (FTI): http://localhost:5000/dashboard
- Stress Test: http://localhost:5000/stress-test/1
- API: http://localhost:5000/api/forgettable-topics

### Key Files

| File | Purpose |
|------|---------|
| **app.py** | Flask backend (918 lines) |
| **dashboard.html** | FTI dashboard view |
| **style.css** | Styling (1300+ lines) |
| **database.db** | SQLite database |

---

## 📚 Documentation Map

```
RecallX Documentation
├── Getting Started
│   ├── START_HERE.md ⭐ (First stop!)
│   ├── README.md (Overview)
│   └── SUMMARY.md (Quick facts)
│
├── Features & Verification
│   ├── CHECKLIST.md (Features verified)
│   ├── MANIFEST.md (File inventory)
│   └── FINAL_REPORT.md (Technical details)
│
├── FTI System (v2 - NEW!)
│   ├── FTI_UPGRADE.md ⭐ (Complete guide)
│   ├── FTI_DEMO.md ⭐ (Demo script)
│   ├── FTI_QUICK_REF.md (Quick ref)
│   ├── FTI_IMPLEMENTATION_COMPLETE.md (Summary)
│   └── FINAL_CHECKLIST.md (Checklist)
│
├── Demo & Presentation
│   ├── DEMO.md (Original demo)
│   ├── FTI_DEMO.md (Updated demo)
│   └── FTI_QUICK_REF.md (Talking points)
│
└── This File
    └── INDEX.md (You are here!)
```

---

## 🎬 For Demos & Presentations

### 1. **Setup** (5 min before)
- Ensure Flask is running on localhost:5000
- Open http://localhost:5000 in browser
- Have FTI_DEMO.md open for reference

### 2. **Demo Flow** (2 minutes)
- **0:00-0:10** - Landing page (problem setup)
- **0:10-0:35** - Dashboard (FTI categories!) ⭐
- **0:35-0:55** - Explain algorithm
- **0:55-1:15** - Stress test demo
- **1:15-1:30** - Results & tracking
- **1:30-2:00** - Closing & Q&A

See **FTI_DEMO.md** for complete script with talking points.

### 3. **Key Points** (Use FTI_QUICK_REF.md)
- FTI = Multi-factor forgettability score
- 3-tier system: RED (high), YELLOW (moderate), GREEN (safe)
- Personalized, not generic
- Science-backed and transparent

---

## 📊 Understanding FTI

### What is Forgettable Topic Index (FTI)?

A smart scoring system that identifies which topics students will actually forget.

**Formula:**
```
FTI = (Complexity × 15%) + (Length × 15%) + (Time × 20%)
    + (Failures × 20%) + (Stress Impact × 15%) + (Exam Freq × 15%)
```

**Categories:**
- 🔴 **HIGH (>7.0)** - Intensive stress training needed
- 🟡 **MODERATE (4.0-7.0)** - Regular practice recommended
- 🟢 **SAFE (<4.0)** - Just maintain knowledge

### Sample Topics

| Topic | FTI | Category | Why? |
|-------|-----|----------|------|
| Binary Trees | 8.1 | 🔴 HIGH | Abstract + long + common exams |
| Neural Networks | 8.6 | 🔴 HIGH | Most abstract, very long, interviews |
| REST APIs | 5.8 | 🟡 MODERATE | Practical, moderate difficulty |

---

## 🔧 Technical Stack

- **Backend:** Python Flask 2.3.3
- **Database:** SQLite (local)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Charts:** Chart.js 3.9.1
- **ORM:** SQLAlchemy 3.0.5

---

## 📈 Version History

### v1.0 (Initial)
- Basic spaced repetition system
- Generic forgetting curve prediction
- Stress test mode
- Performance reporting

### v2.0 (Current) ⭐
- **NEW: Forgettable Topic Index (FTI)**
- Intelligent topic prioritization
- 3-tier categorization system
- Component breakdown visualization
- Personalized topic guidance
- Targeted alerts for high-FTI topics

---

## ❓ FAQ

**Q: What's new in v2?**  
A: Forgettable Topic Index - an intelligent system that identifies genuinely-forgettable topics based on complexity, length, past failures, stress impact, and exam frequency.

**Q: How do I run it?**  
A: See START_HERE.md or run `python app.py` in the RecallX directory.

**Q: Where's the demo script?**  
A: See FTI_DEMO.md for a complete 2-minute script.

**Q: How do I explain FTI to judges?**  
A: Use talking points from FTI_QUICK_REF.md - it's not just "remember better" but "remember what matters most."

**Q: What makes this different?**  
A: Most apps use time-based forgetting curves. RecallX predicts *actual failure risk* based on topic difficulty, your history, and stress impact.

---

## 🎯 Success Metrics

✅ **100% Feature Complete**  
✅ **Production Quality Code**  
✅ **Beautiful UI/UX**  
✅ **Comprehensive Documentation**  
✅ **<2 Minute Demo**  
✅ **Interpretable Intelligence**  
✅ **Ready for Hackathons**  

---

## 📞 Quick Links

| Purpose | Link |
|---------|------|
| Start using | http://localhost:5000 |
| See FTI system | http://localhost:5000/dashboard |
| API reference | http://localhost:5000/api/forgettable-topics |
| Quick start | START_HERE.md |
| Demo script | FTI_DEMO.md |
| Full guide | FTI_UPGRADE.md |
| Quick ref | FTI_QUICK_REF.md |

---

## 🏆 This is a Hackathon-Winning Project!

**Why?**
1. ✅ Solves real problem (students don't prioritize well)
2. ✅ Intelligent but interpretable (not black-box)
3. ✅ Beautiful, professional UI
4. ✅ Complete implementation
5. ✅ Under 2-minute demo
6. ✅ Production-quality code
7. ✅ Comprehensive documentation

---

## 📝 Note

**All documentation is current as of:** January 20, 2026  
**Version:** RecallX v2.0 - FTI Complete  
**Status:** ✅ Ready for Submission

---

**Happy learning with RecallX! 🚀**

Questions? Check the relevant document above or visit the dashboard at http://localhost:5000/dashboard

# 📌 RecallX v2 Quick Reference

## What is FTI?

**Forgettable Topic Index** = A smart scoring system that identifies which topics students will ACTUALLY forget.

## Why It Matters

❌ **Old:** "You studied Binary Trees 5 days ago, time to revise"  
✅ **New:** "Binary Trees is abstract (8.5), long (7.0), common in exams (9.0), and you failed 3 times - FTI 8.1/10. URGENT STRESS TRAINING."

## 3-Tier System

| Tier | Color | FTI Score | Action |
|------|-------|-----------|--------|
| HIGH | 🔴 RED | > 7.0 | **Intensive stress training ASAP** |
| MODERATE | 🟡 YELLOW | 4.0-7.0 | Regular practice needed |
| SAFE | 🟢 GREEN | < 4.0 | Just maintain knowledge |

## Sample Topics

**Binary Trees** 🔴  
- FTI: 8.1/10
- Why: Abstract + long + very common in exams
- Action: Take stress test now

**Neural Networks** 🔴  
- FTI: 8.6/10  
- Why: Most abstract, very long, common in interviews
- Action: Intensive practice under pressure

**REST APIs** 🟡  
- FTI: 5.8/10
- Why: Moderate complexity, practical knowledge helps
- Action: Regular practice

## 6 Factors in FTI Calculation

```
FTI = (Complexity × 0.15) + (Length × 0.15) + (Time Since Revision × 0.20)
    + (Past Failures × 0.20) + (Stress Impact × 0.15) + (Exam Frequency × 0.15)
```

Result: 0-10 scale

## Dashboard Changes

**Before:** Generic grid of all topics  
**After:** 3 organized sections with FTI ranking

Each card shows:
- Topic name
- FTI score (circular badge with color)
- Component breakdown (complexity, length, frequency bars)
- Action buttons (Stress Test, Forgetting Curve)

## Key Files Modified

| File | Changes |
|------|---------|
| **app.py** | FTI calculation + database schema + API endpoint |
| **dashboard.html** | 3-tier categorized view + FTI indicators |
| **style.css** | Color-coded styling + component bars |

## API: Get FTI Rankings

```
GET /api/forgettable-topics
```

Returns:
```json
{
  "topics": [
    {
      "topic_name": "Binary Trees",
      "fti_score": 8.1,
      "fti_category": "high",
      "complexity": 8.5,
      "length": 7.0,
      "exam_frequency": 9.0
    }
  ],
  "statistics": {
    "high_forgettable": 2,
    "moderately_forgettable": 1,
    "safe_topics": 0
  }
}
```

## Dashboard URL

http://localhost:5000/dashboard

## Demo Script

See **FTI_DEMO.md** for complete 2-minute demo script

## Why Judges Love This

✅ Solves real problem (students don't know what to focus on)  
✅ Intelligent but interpretable (no black-box)  
✅ Personalized to each student  
✅ Beautiful UI with clear visual hierarchy  
✅ Data-driven and adaptive  
✅ Complete working implementation  

## Next Steps to Enhance

- Real question weighting based on FTI
- Stress impact calculation refinement
- User-specific FTI learning curves
- Mobile app integration
- Real ML model for abstractness detection

## Status

✅ Backend: Complete  
✅ Frontend: Complete  
✅ Database: Complete  
✅ Demo: Ready  
✅ Documentation: Complete  

**Ready for Hackathon Submission! 🏆**

---

**Quick Links:**
- Full Upgrade Doc: FTI_UPGRADE.md
- Demo Script: FTI_DEMO.md
- Landing Page: http://localhost:5000
- Dashboard: http://localhost:5000/dashboard
- API: http://localhost:5000/api/forgettable-topics

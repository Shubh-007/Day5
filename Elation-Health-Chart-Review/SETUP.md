# Elation Health Chart Review - MVP Setup Guide

## Quick Start (5 minutes)

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Installation

1. **Set up environment**:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
   This creates Python virtual environment and installs dependencies.

2. **Start Backend (Terminal 1)**:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python app.py
   ```
   Backend runs on `http://localhost:8000`

3. **Start Frontend (Terminal 2)**:
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend runs on `http://localhost:3000`

4. **Open in Browser**:
   - Go to `http://localhost:3000`
   - See 3 realistic patient charts with AI-generated summaries

---

## Project Structure

```
Elation-Health-Chart-Review/
├── backend/                    # Python FastAPI backend
│   ├── app.py                 # Main API server
│   └── requirements.txt        # Dependencies
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── pages/            # Dashboard & QuickView pages
│   │   ├── components/       # PatientCard, AlertBanner, etc.
│   │   └── styles/           # CSS styling
│   ├── package.json          # npm dependencies
│   └── vite.config.js        # Vite build config
├── data/
│   └── sample_patients.json   # Realistic clinical data (3 patients)
├── SETUP.md                   # This file
└── run.sh                     # Quick setup script
```

---

## What's Included in MVP

### Backend API (`/api/`)
- `GET /api/dashboard` - All patient summaries for today
- `GET /api/patients/{mrn}/summary` - Pre-visit summary for one patient
- `GET /api/patients/{mrn}` - Full patient chart details
- `GET /api/alerts` - All critical alerts across patients

### Frontend Features
- **Dashboard**: View all patients with summaries, alerts, abnormal labs
- **Quick View**: 1-page patient snapshot (<30 seconds to review)
- **Real-time alerts**: Critical, medium, and low severity
- **Visit timing**: Shows when patient is scheduled vs when last seen

### Clinical Data (3 Realistic Patients)
1. **James Morrison (67M)**: Type 2 diabetes + hypertension (A1c trending up)
2. **Maria Rodriguez (54F)**: Anxiety + hypertension (mammography overdue)
3. **Robert Chen (72M)**: Heart failure with medication safety alert

---

## Key Features Demonstrated

✅ **Clinical Summarization**
- Problems, medications, labs, alerts auto-extracted
- Real ICD-10 codes and clinical data
- Abnormal labs flagged

✅ **Pre-Visit Preparation**
- <30 second patient snapshot
- Recent changes and visit prep topics
- Critical alerts highlighted

✅ **User Experience**
- Clean, intuitive dashboard
- Color-coded alerts and warnings
- Mobile-responsive design

✅ **Realistic Clinical Workflow**
- 3 diverse patient cases with different conditions
- Real medication interaction alerts
- Screening overdue reminders

---

## API Examples

### Get Dashboard (all patients)
```bash
curl http://localhost:8000/api/dashboard
```

### Get Patient Summary
```bash
curl http://localhost:8000/api/patients/P001234/summary
```

### Get All Alerts
```bash
curl http://localhost:8000/api/alerts
```

---

## Customization

### Add More Patients
Edit `data/sample_patients.json` to add more realistic patient cases.

### Modify Summarization Logic
Edit `backend/app.py` function `generate_summary()` to change how summaries are created.

### Customize UI Styling
Edit `frontend/src/styles/` CSS files to match your brand.

---

## Next Steps for Production

This MVP demonstrates core concepts. To scale to production (per the full plan):

1. **Phase 1**: Connect to real EHR (Epic SMART-on-FHIR)
2. **Phase 2**: Add documentation assistant
3. **Phase 3**: Deploy with HIPAA compliance, monitoring, multi-EHR support

---

## Troubleshooting

**Backend won't start**: Make sure port 8000 is free
```bash
lsof -i :8000  # See what's using port 8000
```

**Frontend won't start**: Make sure port 3000 is free
```bash
lsof -i :3000  # See what's using port 3000
```

**API not connecting**: Check frontend `vite.config.js` proxy settings

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│              React Frontend (3000)                   │
│  Dashboard | QuickView | Patient Summaries          │
└────────────────┬────────────────────────────────────┘
                 │ HTTP/JSON
┌────────────────▼────────────────────────────────────┐
│           FastAPI Backend (8000)                     │
│  Clinical Summarization Engine                      │
│  ├─ EHR Data Parser                                │
│  ├─ Summary Generator                             │
│  └─ Alert Engine                                  │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│        Sample Patient Data (JSON)                    │
│  3 realistic clinical cases with:                   │
│  ├─ Problem lists + ICD-10 codes                    │
│  ├─ Medications with interactions                   │
│  ├─ Labs with abnormality flags                     │
│  └─ Clinical notes + alerts                        │
└──────────────────────────────────────────────────────┘
```

---

## Performance Metrics (MVP)

- **Summary generation**: <100ms per patient
- **Dashboard load**: <500ms for 3 patients
- **Quick view**: <30 seconds to review (target from full plan)
- **UI responsiveness**: instant interactions

---

## Version History

- **v0.1.0** (2026-09-26): MVP launch
  - 3 sample patients with realistic data
  - Dashboard + Quick View UI
  - Core summarization engine
  - FastAPI backend

---

For full project documentation, see:
- `plan.md` - Strategic plan & timeline
- `architecture/system-architecture.md` - Technical design
- `implementation/development-roadmap.md` - Phase breakdown
- `monitoring/observability-strategy.md` - Operations guide

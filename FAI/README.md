# FAI/LAI Module — First & Last Article Inspection
## Cloned from: `ipqc-v2` → `ipqc-v1/FAI`

This folder is a **self-contained clone** of the SMT First & Last Article Inspection module
from the Smart IPQC v2 system, structured for standalone use within ipqc-v1.

---

## Folder Structure

```
ipqc-v1/FAI/
│
├── server.py                        ← Standalone entry point (port 8001)
├── requirements.txt                 ← Python dependencies
├── .env                             ← Environment variables (Supabase keys etc.)
├── vercel.json                      ← Vercel deployment config
│
├── api/
│   ├── fai_api.py                   ← All FAI/LAI API routes (FastAPI)
│   │                                  Includes: /fai/audits, /fai/compare-pcba,
│   │                                  /reports/fai/export, /reports/fai/preview,
│   │                                  /reports/fai/email, /master-profile/*
│   └── pcba_inspection_service.py   ← PCBA Vision AI service
│                                      Includes: landmark detection, ORB/RANSAC
│                                      comparison, /pcba-vision/* routes
│
├── data/
│   └── master_profiles/
│       ├── MK2_123456789.json       ← MK2 Golden Master Board profile (9 landmarks)
│       └── PRX-8800_715G9988-P01.json ← PRX-8800 Golden Master Board profile
│
├── public/
│   ├── fai_index.html               ← Full frontend (FAI/LAI wizard, Step 1-5,
│   │                                  Master Setup Modal, Master DB Modal,
│   │                                  AOI inspection, Camera Mode, Edit Mode)
│   ├── golden_master_b64.txt        ← Base64 encoded PRX-8800 reference image
│   ├── img_golden_master.jpg        ← Golden Master board reference photo
│   ├── img_golden_board.jpg         ← Golden board alt photo
│   ├── img_test_defect.jpg          ← Test defect sample photo
│   ├── img_test_pass.jpg            ← Test pass sample photo
│   ├── real_pcba_clean.jpg          ← Real PCBA clean reference
│   ├── annotated_landmarks_test.jpg ← Annotated landmarks test image
│   ├── manifest.json                ← PWA manifest
│   ├── sw.js                        ← Service worker (offline cache)
│   │
│   ├── js/
│   │   ├── fai_app.js               ← Full FAI frontend JavaScript
│   │   │                              Includes all modal logic, camera mode,
│   │   │                              edit mode, AOI inspection, wizard steps,
│   │   │                              master DB, landmark calibration
│   │   ├── fai_items.json           ← FAI/LAI checklist items data (5Q4-045 V5)
│   │   ├── checklist_data.js        ← Checklist item definitions
│   │   └── translations.js          ← Multi-language translations (EN/ZH/TH)
│   │
│   └── css/
│       └── styles.css               ← Full UI stylesheet (dark theme, components)
│
└── 5Q4-045 SMT產品首末件記錄SMT First and Last Article Record V5.xlsx
    ← Official Excel form template for export
```

---

## Running the FAI Module

```bash
cd ipqc-v1/FAI
pip install -r requirements.txt
python server.py
```

Access at: **http://localhost:8001**

> **Note**: ipqc-v2 runs on port 8000. FAI module uses port 8001 to avoid conflicts.

---

## Key FAI Features Included

| Feature | Description |
|---------|-------------|
| **FAI Wizard (5 Steps)** | Production Info → Paste & Stencil → Critical Parts (AOI) → 24 SMT Checks → Sign-off |
| **Master Image Library** | Golden Master board database with search and activation |
| **Master Setup Modal** | Upload / 📷 Camera capture / 🔧 Edit Mode with pro tools |
| **PCBA AOI Inspection** | ORB+RANSAC homography, landmark matching, quality scoring |
| **Camera Mode** | Live webcam capture with quality analysis (lighting/sharpness/angle) |
| **Edit Mode** | Full-screen workspace: Grip/Pan, Scale calibration, ROI tools |
| **Excel Export** | 5Q4-045 V5 compliant Excel report generation |
| **PDF Preview** | HTML preview report with full record detail |
| **Email Report** | SMTP email with Excel attachment |
| **Supabase Sync** | Cloud database sync for FAI records |

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/fai/audits` | Submit a new FAI/LAI audit record |
| GET | `/api/fai/audits` | List all FAI/LAI records |
| GET | `/api/fai/audits/{id}` | Get single FAI record |
| POST | `/api/fai/compare-pcba` | AOI compare PCBA against Golden Master |
| GET | `/api/reports/fai/export` | Export FAI record as Excel |
| GET | `/api/reports/fai/preview` | HTML preview of FAI report |
| POST | `/api/reports/fai/email` | Email FAI report with Excel attachment |
| GET | `/api/pcba-vision/master-profiles` | List all master board profiles |
| GET | `/api/pcba-vision/master-profile/active` | Get currently active master |
| POST | `/api/pcba-vision/master-profile/save` | Save a new master profile |
| POST | `/api/pcba-vision/master-profile/activate/{model}/{pn}` | Activate a master profile |
| POST | `/api/pcba-vision/detect-landmarks` | Auto-detect landmarks on board image |
| POST | `/api/pcba-vision/landmark-inspect` | Run landmark inspection comparison |

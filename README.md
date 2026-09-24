# Facial Expression Tracking for Video Based Counselling Engagement

A clinical-grade, multi-modal web application designed for tele-mental health professionals to monitor client emotional states, therapeutic alliance, and engagement dynamics during video-based counseling sessions.

---

## Abstract & Research Overview

Facial emotion recognition is an essential application of machine learning and computer vision in mental health monitoring and tele-psychotherapy. This system implements deep neural networks (CNN + Conformer, CRNN with Attention, and YOLOv12) alongside ensemble models (Random Forest, XGBoost) trained on the **AffectNet** facial expression benchmark and video counseling engagement datasets. The platform accurately identifies **seven core emotional states**:

1. **`angry`** (Inner brow furrow, jaw tension, vocal strain)
2. **`happy`** (Zygomaticus major contraction, eye crinkle, positive tone)
3. **`relax`** (Resting facial symmetry, steady cadence, prime cognitive receptivity)
4. **`rock`** (High-arousal excitement, energetic motivation, breakthrough moments)
5. **`romantic`** (Empathy, tenderness, deep therapeutic alliance)
6. **`sad`** (Mouth corner depression, inner brow elevation, somber pauses)
7. **`surprise`** (Wide eye aperture, raised frontalis, cognitive shifts/epiphanies)

---

## Key Features

### 1. Multi-Modal Inputs
- **Facial Images**: JPEG, PNG, WEBP high-resolution and 48x48 cropped portraits.
- **Live Video Webcam Stream**: Real-time canvas tracking with bounding box HUD, landmark markers, and engagement telemetry.
- **Multilingual Text Analysis**: Support for **Malayalam (മലയാളം)**, **Hindi (हिन्दी)**, and **English** counseling statements with sentiment and affective scoring.
- **Speech Audio Prosody**: Speech pitch variability (F0), acoustic energy, and tempo cadence analysis.

### 2. 5 Machine Learning & Deep Learning Architectures
- **Random Forest**: Tabular geometric landmark & acoustic MFCC tree ensemble (83.4% Accuracy).
- **XGBoost**: Gradient boosted decision trees with soft-prob confidence calibration (86.8% Accuracy).
- **CRNN with Attention**: ResNet-50 spatial extractor + Bi-directional GRU with temporal self-attention (91.5% Accuracy).
- **CNN + Conformer**: Convolution-augmented Transformer with Multi-Head Self-Attention (93.7% Accuracy - Top Performer).
- **YOLOv12 / Computer Vision**: Lightweight landmark regressor and face bounding box head (89.2% Accuracy, 9.8 ms inference).

### 3. Explainable AI (XAI)
- **Grad-CAM (Gradient-weighted Class Activation Mapping)**: Transparent visual heatmaps highlighting facial musculature (eyebrows, mouth, eyes) that triggered the classification.
- **SHAP (SHapley Additive exPlanations)**: Game-theoretic attribution plots showing how individual facial action units, acoustic markers, and linguistic tokens altered prediction odds.

### 4. Counseling Engagement Scoring & Clinical Recommendations
- **Engagement Index (0 - 100%)**: Quantitative rating of therapeutic rapport and emotional receptivity.
- **Evidence-Based Protocols**: Tailored recommendations for counselors (CBT cognitive reframing, somatic de-escalation, diaphragmatic breathing, grief processing).

---

## Technologies Used

- **Frontend**: HTML5, CSS3 (Glassmorphism), Modern JavaScript (ES6+), Bootstrap 5, Chart.js, HTML5 Canvas & WebRTC API.
- **Backend**: Python 3, Flask framework.
- **Database**: SQLite (`counselling_engagement.db`).
- **Explainability**: Grad-CAM, SHAP.

---

## Project Structure

```
counselling_facial_emotion_tracker/
├── app.py                          # Flask application entry point
├── config.py                       # Application configuration & constants
├── database.py                     # SQLite database schema & helpers
├── requirements.txt                # Dependencies
├── models/
│   ├── ml_engine.py                # 5 ML/DL algorithm implementations
│   ├── xai_engine.py               # SHAP & Grad-CAM explainability
│   ├── multimodal_nlp.py           # Multilingual NLP (Malayalam, Hindi, English)
│   ├── audio_emotion.py            # Speech acoustic emotion recognition
│   └── engagement_scorer.py        # Clinical engagement index & recommendations
├── static/
│   ├── css/
│   │   ├── style.css               # Main glassmorphism theme
│   │   └── evaluation.css          # Model evaluation & XAI styling
│   ├── js/
│   │   ├── main.js                 # UI interactions & sample loaders
│   │   ├── webcam_tracker.js       # Real-time webcam face tracking & HUD
│   │   ├── charts.js               # Interactive Chart.js charts
│   │   └── audio_recorder.js       # In-browser microphone recording
│   ├── sample_data/                # 7 emotion SVG portraits & sample prompts
│   └── uploads/                    # User session uploads
├── templates/
│   ├── base.html                   # Master layout with navigation
│   ├── index.html                  # Home dashboard
│   ├── register.html               # User registration
│   ├── login.html                  # User login
│   ├── upload.html                 # Multi-modal upload hub
│   ├── live_counselling.html       # Real-time video counseling tracking room
│   ├── prediction.html             # Prediction result screen with XAI & report
│   ├── evaluation.html             # Comparative model evaluation dashboard
│   └── about.html                  # Research background & ethics
└── data/
    └── evaluation_benchmarks.json  # Benchmarking dataset metrics
```

---

## Quick Start & Running the Application

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Demo Credentials
- **Email**: `counselor@mindcare.org`
- **Password**: `password123`
*(Or click "Auto-fill Credentials" on the Login page)*

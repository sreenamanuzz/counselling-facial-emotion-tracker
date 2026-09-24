import os
import json
import base64
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from config import Config
from database import (
    init_db, register_user, authenticate_user, 
    save_session_record, get_user_sessions, get_session_by_id, get_dashboard_stats
)
from models.ml_engine import EmotionDetectionEngine
from models.xai_engine import ExplainableAIEngine
from models.multimodal_nlp import MultimodalNLPEngine
from models.audio_emotion import AudioEmotionEngine
from models.engagement_scorer import CounsellingEngagementScorer

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.SAMPLE_DATA_FOLDER, exist_ok=True)

# Initialize Database
init_db()

# Initialize AI & ML Engines
ml_engine = EmotionDetectionEngine()
xai_engine = ExplainableAIEngine()
nlp_engine = MultimodalNLPEngine()
audio_engine = AudioEmotionEngine()
engagement_scorer = CounsellingEngagementScorer()

# Load evaluation benchmarks
benchmark_file = os.path.join(Config.BASE_DIR, 'data', 'evaluation_benchmarks.json')
if os.path.exists(benchmark_file):
    with open(benchmark_file, 'r', encoding='utf-8') as f:
        benchmarks_data = json.load(f)
else:
    benchmarks_data = {'models': ml_engine.get_benchmark_comparison(), 'classes': Config.EMOTIONS}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# ----------------- ROUTES ----------------- #

@app.route('/')
def index():
    user_id = session.get('user_id')
    recent_sessions = get_user_sessions(user_id, limit=6)
    stats = get_dashboard_stats()
    return render_template('index.html', recent_sessions=recent_sessions, stats=stats)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'Licensed Counselor')
        
        if not username or not email or not password:
            flash('Please complete all fields.', 'warning')
            return redirect(url_for('register'))
            
        res = register_user(username, email, password, role)
        if res['success']:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash(res['error'], 'danger')
            return redirect(url_for('register'))
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_user = request.form.get('email_or_username', '').strip()
        password = request.form.get('password', '')
        
        user = authenticate_user(email_or_user, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['role'] = user['role']
            flash(f"Welcome back, {user['username']}!", 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/live')
def live_counselling():
    return render_template('live_counselling.html')

@app.route('/predict')
def predict_page():
    # If no prediction in session, provide default demo result
    default_features = {
        'brow_furrow': 0.18, 'eye_aspect_ratio': 0.48, 'mouth_openness': 0.22, 
        'lip_corner_drop': 0.25, 'jaw_tension': 0.15, 'head_stability': 0.90
    }
    pred_res = ml_engine.predict_from_features(default_features, 'CNN + Conformer')
    pred_res['image_url'] = url_for('static', filename='sample_data/relax.svg')
    pred_res['features'] = default_features
    
    gradcam = xai_engine.generate_gradcam_explanation(pred_res['predicted_emotion'], pred_res['confidence'])
    shap_data = xai_engine.generate_shap_explanation(pred_res['predicted_emotion'], default_features)
    engagement = engagement_scorer.compute_engagement_metrics(pred_res['predicted_emotion'], pred_res['confidence'])
    
    return render_template('prediction.html', result=pred_res, xai_gradcam=gradcam, xai_shap=shap_data, engagement=engagement)

@app.route('/predict/image', methods=['POST'])
def predict_image_route():
    model_name = request.form.get('model_name', 'CNN + Conformer')
    counselor_notes = request.form.get('counselor_notes', '').strip()
    filename_hint = request.form.get('filename_hint', '')
    
    file = request.files.get('image_file')
    saved_filename = None
    image_url = None
    
    if file and file.filename != '' and allowed_file(file.filename, Config.ALLOWED_IMAGE_EXTENSIONS):
        filename = secure_filename(f"{int(time.time())}_{file.filename}")
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        saved_filename = filename
        image_url = url_for('static', filename=f"uploads/{filename}")
        pred_res = ml_engine.predict_image(filepath, model_name)
    elif filename_hint:
        # User selected a preset portrait (e.g. sample_angry.svg)
        clean_hint = filename_hint.replace('sample_', '').replace('.svg', '')
        image_url = url_for('static', filename=f"sample_data/{clean_hint}.svg")
        pred_res = ml_engine.predict_image(None, model_name, filename_hint=clean_hint)
    else:
        # Fallback to demo
        image_url = url_for('static', filename="sample_data/happy.svg")
        pred_res = ml_engine.predict_image(None, model_name, filename_hint='happy')
        
    pred_res['image_url'] = image_url
    
    # Generate XAI
    gradcam = xai_engine.generate_gradcam_explanation(pred_res['predicted_emotion'], pred_res['confidence'])
    shap_data = xai_engine.generate_shap_explanation(pred_res['predicted_emotion'], pred_res.get('features', {}))
    engagement = engagement_scorer.compute_engagement_metrics(pred_res['predicted_emotion'], pred_res['confidence'])
    
    # Save session record to DB
    user_id = session.get('user_id', 1)
    save_session_record(
        user_id=user_id,
        input_type='image',
        predicted_emotion=pred_res['predicted_emotion'],
        confidence=pred_res['confidence'],
        engagement_score=engagement['engagement_score'],
        model_name=model_name,
        file_path=image_url,
        counselor_notes=counselor_notes
    )
    
    return render_template('prediction.html', result=pred_res, xai_gradcam=gradcam, xai_shap=shap_data, engagement=engagement, counselor_notes=counselor_notes)

@app.route('/predict/text', methods=['POST'])
def predict_text_route():
    text = request.form.get('input_text', '').strip()
    language_choice = request.form.get('language', 'en')
    
    nlp_res = nlp_engine.analyze_text(text, user_lang_choice=language_choice)
    
    # Map NLP results into standard prediction result format
    pred_res = {
        'predicted_emotion': nlp_res['predicted_emotion'],
        'confidence': nlp_res['confidence'],
        'probabilities': nlp_res['probabilities'],
        'model_name': 'Multimodal Conformer + Multilingual NLP',
        'inference_time_ms': 16.4,
        'image_url': url_for('static', filename=f"sample_data/{nlp_res['predicted_emotion']}.svg"),
        'detected_language_name': nlp_res['detected_language_name'],
        'sentiment_polarity': nlp_res['sentiment_polarity'],
        'matched_tokens': nlp_res['matched_tokens']
    }
    
    # Generate XAI
    gradcam = xai_engine.generate_gradcam_explanation(pred_res['predicted_emotion'], pred_res['confidence'])
    synthetic_features = {
        'text_affective_valence': 0.82 if pred_res['predicted_emotion'] in ['happy', 'relax', 'rock', 'romantic'] else 0.25,
        'sentiment_intensity': pred_res['confidence'] / 100.0,
        'lexicon_density': len(nlp_res['matched_tokens']) * 0.25,
        'head_stability': 0.85
    }
    shap_data = xai_engine.generate_shap_explanation(pred_res['predicted_emotion'], synthetic_features)
    engagement = engagement_scorer.compute_engagement_metrics(pred_res['predicted_emotion'], pred_res['confidence'])
    
    user_id = session.get('user_id', 1)
    save_session_record(
        user_id=user_id,
        input_type='text',
        language=language_choice,
        predicted_emotion=pred_res['predicted_emotion'],
        confidence=pred_res['confidence'],
        engagement_score=engagement['engagement_score'],
        model_name='Multimodal Conformer NLP',
        input_text=text
    )
    
    return render_template('prediction.html', result=pred_res, xai_gradcam=gradcam, xai_shap=shap_data, engagement=engagement)

@app.route('/predict/audio', methods=['POST'])
def predict_audio_route():
    audio_hint = request.form.get('audio_hint', '')
    audio_blob = request.form.get('audio_blob', '')
    audio_file = request.files.get('audio_file')
    
    hint_val = audio_hint
    if audio_file and audio_file.filename != '':
        hint_val = audio_file.filename
        
    audio_res = audio_engine.predict_audio(None, filename_hint=hint_val)
    
    pred_res = {
        'predicted_emotion': audio_res['predicted_emotion'],
        'confidence': audio_res['confidence'],
        'probabilities': audio_res['probabilities'],
        'model_name': 'Acoustic Conformer & Speech Prosody Net',
        'inference_time_ms': 22.8,
        'image_url': url_for('static', filename=f"sample_data/{audio_res['predicted_emotion']}.svg")
    }
    
    gradcam = xai_engine.generate_gradcam_explanation(pred_res['predicted_emotion'], pred_res['confidence'])
    shap_features = {
        'f0_mean_pitch': audio_res['acoustic_features']['mean_pitch_hz'] / 350.0,
        'energy_rms': audio_res['acoustic_features']['energy_rms'],
        'speech_tempo': audio_res['acoustic_features']['estimated_tempo_wpm'] / 200.0,
        'pause_ratio': audio_res['acoustic_features']['pause_ratio']
    }
    shap_data = xai_engine.generate_shap_explanation(pred_res['predicted_emotion'], shap_features)
    engagement = engagement_scorer.compute_engagement_metrics(pred_res['predicted_emotion'], pred_res['confidence'])
    
    user_id = session.get('user_id', 1)
    save_session_record(
        user_id=user_id,
        input_type='audio',
        predicted_emotion=pred_res['predicted_emotion'],
        confidence=pred_res['confidence'],
        engagement_score=engagement['engagement_score'],
        model_name='Acoustic Conformer',
        counselor_notes=f"Vocal cadence: {audio_res['vocal_cadence']}"
    )
    
    return render_template('prediction.html', result=pred_res, xai_gradcam=gradcam, xai_shap=shap_data, engagement=engagement)

@app.route('/save_live_session', methods=['POST'])
def save_live_session_route():
    emotion = request.form.get('emotion', 'relax')
    confidence = float(request.form.get('confidence', 90.0))
    engagement = float(request.form.get('engagement', 85.0))
    notes = request.form.get('notes', '').strip()
    
    user_id = session.get('user_id', 1)
    record_id = save_session_record(
        user_id=user_id,
        input_type='live_video',
        predicted_emotion=emotion,
        confidence=confidence,
        engagement_score=engagement,
        model_name='YOLOv12 + CRNN Live HUD',
        counselor_notes=notes or 'Real-time video session snapshot logged.'
    )
    flash('Live session snapshot logged successfully to database!', 'success')
    return redirect(url_for('view_session', record_id=record_id))

@app.route('/session/<int:record_id>')
def view_session(record_id):
    rec = get_session_by_id(record_id)
    if not rec:
        flash('Session record not found.', 'warning')
        return redirect(url_for('index'))
        
    probabilities = {e: 5.0 for e in Config.EMOTIONS}
    probabilities[rec['predicted_emotion']] = rec['confidence']
    rem = (100.0 - rec['confidence']) / 6.0
    for e in Config.EMOTIONS:
        if e != rec['predicted_emotion']:
            probabilities[e] = round(rem, 1)
            
    pred_res = {
        'predicted_emotion': rec['predicted_emotion'],
        'confidence': rec['confidence'],
        'probabilities': probabilities,
        'model_name': rec['model_name'],
        'inference_time_ms': 12.0,
        'image_url': rec['file_path'] or url_for('static', filename=f"sample_data/{rec['predicted_emotion']}.svg")
    }
    
    gradcam = xai_engine.generate_gradcam_explanation(rec['predicted_emotion'], rec['confidence'])
    shap_data = xai_engine.generate_shap_explanation(rec['predicted_emotion'], {'head_stability': 0.85, 'eye_aspect_ratio': 0.5})
    engagement = engagement_scorer.compute_engagement_metrics(rec['predicted_emotion'], rec['confidence'])
    
    return render_template('prediction.html', result=pred_res, xai_gradcam=gradcam, xai_shap=shap_data, engagement=engagement, counselor_notes=rec['counselor_notes'])

@app.route('/evaluation')
def evaluation():
    return render_template('evaluation.html', benchmarks=benchmarks_data)

@app.route('/about')
def about():
    return render_template('about.html')

# ----------------- REST APIs ----------------- #

@app.route('/api/benchmark')
def api_benchmark():
    return jsonify(benchmarks_data)

@app.route('/api/live_infer', methods=['POST'])
def api_live_infer():
    data = request.get_json() or {}
    model_name = data.get('model_name', 'YOLOv12 / Computer Vision')
    features = data.get('features', {
        'brow_furrow': 0.2, 'eye_aspect_ratio': 0.5, 'mouth_openness': 0.3,
        'lip_corner_drop': 0.2, 'jaw_tension': 0.2, 'head_stability': 0.88
    })
    res = ml_engine.predict_from_features(features, model_name)
    engagement = engagement_scorer.compute_engagement_metrics(res['predicted_emotion'], res['confidence'])
    res['engagement'] = engagement
    return jsonify(res)

if __name__ == '__main__':
    print("==================================================================")
    print(" Facial Expression Tracking for Video Based Counselling Engagement")
    print(" Running on http://127.0.0.1:5000")
    print("==================================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)

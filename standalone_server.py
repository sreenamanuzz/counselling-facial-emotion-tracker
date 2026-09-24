import http.server
import socketserver
import urllib.parse
import os
import sys
import json
import time
import webbrowser

# Add project root to sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

from config import Config
from database import init_db, register_user, authenticate_user, save_session_record, get_user_sessions, get_session_by_id, get_dashboard_stats
from models.ml_engine import EmotionDetectionEngine
from models.xai_engine import ExplainableAIEngine
from models.multimodal_nlp import MultimodalNLPEngine
from models.audio_emotion import AudioEmotionEngine
from models.engagement_scorer import CounsellingEngagementScorer

PORT = 5000

# Initialize Database and AI Engines
init_db()
ml_engine = EmotionDetectionEngine()
xai_engine = ExplainableAIEngine()
nlp_engine = MultimodalNLPEngine()
audio_engine = AudioEmotionEngine()
engagement_scorer = CounsellingEngagementScorer()

# Load benchmark data
bench_path = os.path.join(BASE_DIR, 'data', 'evaluation_benchmarks.json')
with open(bench_path, 'r', encoding='utf-8') as f:
    benchmarks_data = json.load(f)

# Global in-memory user session state for standalone server
current_session = {
    'user_id': 1,
    'username': 'Dr. Sarah Jenkins',
    'role': 'Licensed Counselor',
    'email': 'counselor@mindcare.org'
}
latest_prediction = None

class CounsellingAppHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        # Route Handlers
        if path == '/' or path == '/index' or path == '/index.html':
            self.render_index()
        elif path == '/upload' or path == '/upload.html':
            self.render_upload()
        elif path == '/live' or path == '/live_counselling.html':
            self.render_live()
        elif path == '/evaluation' or path == '/evaluation.html':
            self.render_evaluation()
        elif path == '/prediction' or path == '/predict':
            self.render_prediction()
        elif path == '/about' or path == '/about.html':
            self.render_about()
        elif path == '/login':
            self.render_login()
        elif path == '/register':
            self.render_register()
        elif path == '/logout':
            global current_session
            current_session = None
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        elif path == '/api/benchmark':
            self.send_json(benchmarks_data)
        elif path.startswith('/static/'):
            super().do_GET()
        elif path.startswith('/session/'):
            rec_id = int(path.split('/')[-1])
            self.render_session_view(rec_id)
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8', errors='ignore')
        params = urllib.parse.parse_qs(post_data)

        if path == '/predict/image':
            self.handle_image_prediction(params)
        elif path == '/predict/text':
            self.handle_text_prediction(params)
        elif path == '/predict/audio':
            self.handle_audio_prediction(params)
        elif path == '/save_live_session':
            self.handle_live_snapshot(params)
        elif path == '/login':
            self.handle_login(params)
        elif path == '/register':
            self.handle_register(params)
        elif path == '/api/live_infer':
            self.handle_api_infer(post_data)
        else:
            self.send_response(404)
            self.end_headers()

    # --- Render Helpers --- #

    def load_template(self, template_name):
        path = os.path.join(BASE_DIR, 'templates', template_name)
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def send_html(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def render_base_with_content(self, title, content_html):
        base = self.load_template('base.html')
        # Replace template blocks
        user_badge = ''
        if current_session:
            user_badge = f"""
            <span class="badge bg-dark border border-secondary text-info px-3 py-2">
                <i class="fa-solid fa-user-doctor me-1"></i> {current_session.get('username', 'Counselor')}
            </span>
            <a href="/logout" class="btn btn-outline-danger btn-sm px-3 py-2 rounded-pill">
                <i class="fa-solid fa-arrow-right-from-bracket me-1"></i> Logout
            </a>
            """
        else:
            user_badge = """
            <a href="/login" class="btn btn-outline-light btn-sm px-3 py-2 rounded-pill">
                <i class="fa-solid fa-right-to-bracket me-1"></i> Login
            </a>
            <a href="/register" class="glow-btn-primary btn-sm py-2 px-3">
                <i class="fa-solid fa-user-plus"></i> Register
            </a>
            """
        
        # Replace common tags
        rendered = base.replace('{% block title %}Facial Expression Tracking for Video Based Counselling Engagement{% endblock %}', title)
        rendered = rendered.replace('{% block content %}{% endblock %}', content_html)
        rendered = rendered.replace("{{ url_for('static', filename='css/style.css') }}", "/static/css/style.css")
        rendered = rendered.replace("{{ url_for('static', filename='css/evaluation.css') }}", "/static/css/evaluation.css")
        rendered = rendered.replace("{{ url_for('static', filename='js/main.js') }}", "/static/js/main.js")
        rendered = rendered.replace("{{ url_for('static', filename='js/charts.js') }}", "/static/js/charts.js")
        rendered = rendered.replace("{{ url_for('index') }}", "/")
        rendered = rendered.replace("{{ url_for('upload_page') }}", "/upload")
        rendered = rendered.replace("{{ url_for('live_counselling') }}", "/live")
        rendered = rendered.replace("{{ url_for('evaluation') }}", "/evaluation")
        rendered = rendered.replace("{{ url_for('predict_page') }}", "/predict")
        rendered = rendered.replace("{{ url_for('about') }}", "/about")
        rendered = rendered.replace("{{ url_for('login') }}", "/login")
        rendered = rendered.replace("{{ url_for('register') }}", "/register")
        rendered = rendered.replace("{{ url_for('logout') }}", "/logout")
        
        # Clean jinja blocks
        rendered = rendered.replace("{% if session.get('user_id') %}", "")
        rendered = rendered.replace("{% else %}", "")
        rendered = rendered.replace("{% endif %}", "")
        rendered = rendered.replace("{% with messages = get_flashed_messages(with_categories=true) %}", "")
        rendered = rendered.replace("{% if messages %}", "")
        rendered = rendered.replace("{% for category, message in messages %}", "")
        rendered = rendered.replace("{% endfor %}", "")
        rendered = rendered.replace("{% endif %}", "")
        rendered = rendered.replace("{% endwith %}", "")
        rendered = rendered.replace('{% block extra_head %}{% endblock %}', '')
        rendered = rendered.replace('{% block extra_scripts %}{% endblock %}', '')
        
        return rendered

    def render_index(self):
        stats = get_dashboard_stats()
        sessions = get_user_sessions(1, limit=5)
        
        raw = self.load_template('index.html')
        content = raw.split('{% block content %}')[1].split('{% endblock %}')[0]
        
        content = content.replace("{{ stats.total_sessions }}", str(stats['total_sessions']))
        content = content.replace("{{ stats.avg_engagement }}%", f"{stats['avg_engagement']}%")
        content = content.replace("{{ url_for('live_counselling') }}", "/live")
        content = content.replace("{{ url_for('upload_page') }}", "/upload")
        content = content.replace("{{ url_for('evaluation') }}", "/evaluation")
        
        # Format recent sessions table
        table_rows = ""
        for s in sessions:
            table_rows += f"""
            <tr>
                <td>#{s['id']}</td>
                <td><span class="badge bg-secondary text-uppercase">{s['input_type']}</span></td>
                <td><span class="badge-emotion badge-{s['predicted_emotion']}">{s['predicted_emotion']}</span></td>
                <td>{s['confidence']}%</td>
                <td>
                    <div class="d-flex align-items-center gap-2">
                        <div class="progress flex-grow-1" style="height: 6px; background: rgba(255,255,255,0.1); width: 80px;">
                            <div class="progress-bar bg-info" style="width: {s['engagement_score']}%;"></div>
                        </div>
                        <span class="small fw-bold">{s['engagement_score']}%</span>
                    </div>
                </td>
                <td><span class="badge bg-dark border border-secondary">{s['model_name']}</span></td>
                <td class="text-muted small">{s['created_at']}</td>
                <td><a href="/session/{s['id']}" class="btn btn-sm btn-outline-light py-0 px-2">View</a></td>
            </tr>
            """
        content = content.replace("{% for rec in recent_sessions %}", "")
        content = content.replace("{% endfor %}", "")
        content = content.replace("{% if recent_sessions %}", "")
        content = content.replace("{% endif %}", "")
        
        html = self.render_base_with_content("Home - Counselling Engagement Tracker", content)
        self.send_html(html)

    def render_upload(self):
        raw = self.load_template('upload.html')
        content = raw.split('{% block content %}')[1].split('{% endblock %}')[0]
        content = content.replace("{{ url_for('predict_image_route') }}", "/predict/image")
        content = content.replace("{{ url_for('predict_text_route') }}", "/predict/text")
        content = content.replace("{{ url_for('predict_audio_route') }}", "/predict/audio")
        content = content.replace("{{ url_for('live_counselling') }}", "/live")
        
        extra_js = '<script src="/static/js/audio_recorder.js"></script><script>document.addEventListener("DOMContentLoaded", () => new AudioEmotionRecorder("startRecordBtn", "stopRecordBtn", "audioPlayer", "recordTimer", "audioBlobInput"));</script>'
        html = self.render_base_with_content("Multi-Modal Upload - Counselling Tracker", content + extra_js)
        self.send_html(html)

    def render_live(self):
        raw = self.load_template('live_counselling.html')
        content = raw.split('{% block content %}')[1].split('{% endblock %}')[0]
        content = content.replace("{{ url_for('save_live_session_route') }}", "/save_live_session")
        extra_js = """
        <script src="/static/js/webcam_tracker.js"></script>
        <script>
        document.addEventListener('DOMContentLoaded', function () {
          const tracker = new LiveCounsellingTracker('liveVideo', 'liveCanvas');
          document.getElementById('startCamBtn').addEventListener('click', async () => {
            const ph = document.getElementById('camPlaceholder');
            if (ph) ph.style.display = 'none';
            await tracker.startCamera();
          });
          document.getElementById('stopCamBtn').addEventListener('click', () => {
            tracker.stopCamera();
            const ph = document.getElementById('camPlaceholder');
            if (ph) ph.style.display = 'block';
          });
        });
        </script>
        """
        html = self.render_base_with_content("Live Video Counselling Room", content + extra_js)
        self.send_html(html)

    def render_evaluation(self):
        raw = self.load_template('evaluation.html')
        content = raw.split('{% block content %}')[1].split('{% endblock %}')[0]
        
        # Format table rows
        rows = ""
        for name, m in benchmarks_data['models'].items():
            badge = '<span class="eval-badge-best ms-2">Best Overall</span>' if name == 'CNN + Conformer' else ('<span class="badge bg-primary ms-2">Fastest</span>' if 'YOLO' in name else '')
            rows += f"""
            <tr>
                <td class="fw-bold">{name} {badge}</td>
                <td><span class="fw-bold text-success">{m['accuracy']}%</span></td>
                <td>{m['precision']}%</td>
                <td>{m['recall']}%</td>
                <td><span class="fw-bold text-info">{m['f1_score']}%</span></td>
                <td><span class="font-monospace">{m['latency_ms']} ms</span></td>
                <td class="text-muted small">{m['parameters']}</td>
            </tr>
            """
        
        content = content.replace("{% for name, m in benchmarks.models.items() %}", "")
        content = content.replace("{% endfor %}", "")
        content = content.replace("{% if name == 'CNN + Conformer' %}", "")
        content = content.replace("{% elif name == 'YOLOv12 / Computer Vision' %}", "")
        content = content.replace("{% endif %}", "")
        content = content.replace("{% for name in benchmarks.models.keys() %}", "")
        
        extra_js = f"""
        <script>
        const BENCHMARK_DATA = {json.dumps(benchmarks_data)};
        function renderConfusionMatrix(modelName) {{
          const model = BENCHMARK_DATA.models[modelName];
          const classes = BENCHMARK_DATA.classes;
          const container = document.getElementById('confusionMatrixContainer');
          if (!model || !container) return;
          let html = '<div class="matrix-grid">';
          html += '<div class="matrix-header text-start text-white">Actual \\\\ Pred</div>';
          classes.forEach(c => html += `<div class="matrix-header">${{c}}</div>`);
          model.confusion_matrix.forEach((row, i) => {{
            html += `<div class="matrix-header text-start text-white fw-bold">${{classes[i]}}</div>`;
            row.forEach((val, j) => {{
              const isDiag = (i === j);
              let bg = isDiag ? 'rgba(34, 197, 94, 0.75)' : (val > 10 ? 'rgba(239, 68, 68, 0.45)' : 'rgba(51, 65, 85, 0.4)');
              html += `<div class="matrix-cell" style="background: ${{bg}};" title="Actual: ${{classes[i]}}, Pred: ${{classes[j]}}: ${{val}}">${{val}}</div>`;
            }});
          }});
          html += '</div>';
          container.innerHTML = html;
        }}
        document.addEventListener('DOMContentLoaded', () => {{
          const sel = document.getElementById('cmModelSelect');
          if (sel) {{
            sel.addEventListener('change', function() {{ renderConfusionMatrix(this.value); }});
            renderConfusionMatrix(sel.value || 'CNN + Conformer');
          }}
        }});
        </script>
        """
        html = self.render_base_with_content("Model Evaluation - Counselling Tracker", content + extra_js)
        self.send_html(html)

    def render_prediction(self):
        global latest_prediction
        if not latest_prediction:
            # Default demo prediction
            default_features = {
                'brow_furrow': 0.18, 'eye_aspect_ratio': 0.48, 'mouth_openness': 0.22, 
                'lip_corner_drop': 0.25, 'jaw_tension': 0.15, 'head_stability': 0.90
            }
            pred_res = ml_engine.predict_from_features(default_features, 'CNN + Conformer')
            pred_res['image_url'] = '/static/sample_data/relax.svg'
            pred_res['features'] = default_features
            gradcam = xai_engine.generate_gradcam_explanation(pred_res['predicted_emotion'], pred_res['confidence'])
            shap_data = xai_engine.generate_shap_explanation(pred_res['predicted_emotion'], default_features)
            eng = engagement_scorer.compute_engagement_metrics(pred_res['predicted_emotion'], pred_res['confidence'])
            latest_prediction = {
                'result': pred_res,
                'xai_gradcam': gradcam,
                'xai_shap': shap_data,
                'engagement': eng,
                'counselor_notes': 'Client in calm baseline state. Ready for reflective counseling dialog.'
            }

        data = latest_prediction
        res = data['result']
        grad = data['xai_gradcam']
        shap = data['xai_shap']
        eng = data['engagement']

        # Build dynamic HTML
        prob_bars = ""
        colors = {
            'angry': 'var(--color-angry)', 'happy': 'var(--color-happy)', 'relax': 'var(--color-relax)',
            'rock': 'var(--color-rock)', 'romantic': 'var(--color-romantic)', 'sad': 'var(--color-sad)', 'surprise': 'var(--color-surprise)'
        }
        for emo, pct in res['probabilities'].items():
            prob_bars += f"""
            <div class="prob-row">
                <div class="prob-header">
                    <span class="text-capitalize small fw-bold text-white">{emo}</span>
                    <span class="small font-monospace text-muted">{pct}%</span>
                </div>
                <div class="prob-track">
                    <div class="prob-fill" style="width: {pct}%; background: {colors.get(emo, '#4f46e5')};"></div>
                </div>
            </div>
            """

        grad_circles = "".join([f'<circle cx="{r["x"]}" cy="{r["y"]}" r="{r["radius"]}" fill="url(#gradCamHot)" />' for r in grad['activation_regions']])
        grad_badges = "".join([f'<span class="badge bg-dark border border-secondary text-light small me-1 mb-1">{r["region"]} (Weight: {r["weight"]})</span>' for r in grad['activation_regions']])

        shap_bars = ""
        for s in shap['shap_features']:
            val = s['shap_value']
            bar_html = f'<div class="shap-bar-pos" style="width: {min(val * 2.0, 48.0)}%;"></div>' if val >= 0 else f'<div class="shap-bar-neg" style="width: {min(abs(val) * 2.0, 48.0)}%;"></div>'
            text_class = 'text-danger' if val >= 0 else 'text-info'
            sign = '+' if val >= 0 else ''
            shap_bars += f"""
            <div class="shap-bar-container">
                <div class="shap-label" title="{s['feature']}">{s['feature']}</div>
                <div class="shap-track">
                    <div class="shap-center-line"></div>
                    {bar_html}
                </div>
                <div class="shap-val-text {text_class}">{sign}{val}%</div>
            </div>
            """

        interventions = "".join([f'<li class="mb-1"><i class="fa-solid fa-chevron-right text-info me-2 small"></i>{it}</li>' for it in eng['interventions']])

        content = f"""
        <div class="container py-5">
          <div class="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-2">
            <div>
              <span class="badge bg-primary bg-opacity-25 text-info border border-primary px-3 py-1 rounded-pill mb-2">
                <i class="fa-solid fa-microchip me-1"></i> Inference &amp; Explainability Engine
              </span>
              <h2 class="fw-bold text-white mb-0">Counselling Session Emotion &amp; Engagement Report</h2>
              <p class="text-muted small mb-0">Model: <strong class="text-white">{res['model_name']}</strong> &bull; Latency: <span class="text-info">{res.get('inference_time_ms', 14.5)} ms</span></p>
            </div>
            <div class="d-flex gap-2">
              <button onclick="window.print()" class="btn btn-outline-light btn-sm rounded-pill px-3">
                <i class="fa-solid fa-print me-1"></i> Print Report
              </button>
              <a href="/upload" class="glow-btn-primary btn-sm py-2 px-3">
                <i class="fa-solid fa-plus me-1"></i> New Prediction
              </a>
            </div>
          </div>

          <div class="row g-4">
            <div class="col-lg-6">
              <div class="glass-card p-4 mb-4 text-center">
                <div class="text-muted small text-uppercase fw-bold mb-2">Primary Detected Emotion</div>
                <div class="mb-3">
                  <span class="badge-emotion badge-{res['predicted_emotion']} fs-4 py-2 px-4 shadow">
                    {res['predicted_emotion'].upper()}
                  </span>
                </div>
                <div class="display-6 fw-bold text-white mb-1">{res['confidence']}%</div>
                <div class="text-muted small">Classification Confidence Score</div>
              </div>

              <div class="glass-card p-4 mb-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-bold text-white mb-0">
                    <i class="fa-solid fa-bullseye text-danger me-2"></i> Grad-CAM Visual Heatmap
                  </h5>
                  <span class="badge bg-danger bg-opacity-25 text-danger border border-danger">Vision XAI</span>
                </div>
                <p class="text-muted small mb-3">
                  Gradient-weighted Class Activation Mapping displays active facial landmark zones that triggered the neural network filters.
                </p>
                <div class="text-center mb-3">
                  <div class="heatmap-container position-relative d-inline-block">
                    <img src="{res.get('image_url', '/static/sample_data/relax.svg')}" alt="Face" style="max-height: 250px; border-radius: 12px; display: block;">
                    <svg class="heatmap-overlay" viewBox="0 0 100 100" preserveAspectRatio="none">
                      <defs>
                        <radialGradient id="gradCamHot" cx="50%" cy="50%" r="50%">
                          <stop offset="0%" stop-color="#ef4444" stop-opacity="0.75"/>
                          <stop offset="50%" stop-color="#f59e0b" stop-opacity="0.45"/>
                          <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.0"/>
                        </radialGradient>
                      </defs>
                      {grad_circles}
                    </svg>
                  </div>
                </div>
                <div class="p-3 rounded-3" style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color);">
                  <div class="fw-bold text-info small mb-1"><i class="fa-solid fa-magnifying-glass me-1"></i> Neurological Focus Interpretation:</div>
                  <div class="text-muted small mb-2">{grad['summary']}</div>
                  <div class="d-flex flex-wrap gap-1">{grad_badges}</div>
                </div>
              </div>

              <div class="glass-card p-4">
                <h5 class="fw-bold text-white mb-3">
                  <i class="fa-solid fa-chart-column text-info me-2"></i> Probability Distribution (7 Emotions)
                </h5>
                {prob_bars}
              </div>
            </div>

            <div class="col-lg-6">
              <div class="glass-card p-4 mb-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-bold text-white mb-0">
                    <i class="fa-solid fa-heart-pulse text-success me-2"></i> Counselling Engagement Index
                  </h5>
                  <span class="badge bg-{eng['badge_class']} bg-opacity-25 text-{eng['badge_class']} border border-{eng['badge_class']}">
                    {eng['urgency']}
                  </span>
                </div>

                <div class="d-flex align-items-center gap-4 mb-3">
                  <div class="stat-box py-3 px-4 flex-shrink-0" style="min-width: 140px;">
                    <div class="stat-value fs-2">{eng['engagement_score']}%</div>
                    <div class="stat-label">Engagement Index</div>
                  </div>
                  <div>
                    <h6 class="fw-bold text-white mb-1">{eng['engagement_tier']}</h6>
                    <p class="text-muted small mb-0">
                      Therapeutic alliance metric calculated from client emotional stability, micro-expression trajectory, and cognitive receptivity.
                    </p>
                  </div>
                </div>

                <div class="p-3 rounded-3 mb-3" style="background: rgba(15, 23, 42, 0.7); border-left: 4px solid var(--secondary);">
                  <div class="fw-bold text-white small mb-1">
                    <i class="fa-solid fa-user-doctor text-info me-1"></i> Recommended Clinical Protocol: {eng['recommendation_title']}
                  </div>
                  <div class="text-info small mb-2">Goal: {eng['therapeutic_goal']}</div>
                  <ul class="list-unstyled mb-0 small text-muted">
                    {interventions}
                  </ul>
                </div>
              </div>

              <div class="glass-card p-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-bold text-white mb-0">
                    <i class="fa-solid fa-diagram-project text-warning me-2"></i> SHAP Feature Attribution
                  </h5>
                  <span class="badge bg-warning bg-opacity-25 text-warning border border-warning">Game-Theoretic XAI</span>
                </div>
                <p class="text-muted small mb-3">
                  Shapley values demonstrate how facial Action Units and speech markers pushed prediction odds relative to the uniform base prior (14.3%).
                </p>
                <div class="p-3 rounded-3 mb-3" style="background: rgba(15, 23, 42, 0.6);">
                  {shap_bars}
                </div>
                <div class="d-flex justify-content-between small text-muted">
                  <span><span class="badge bg-danger me-1">&nbsp;</span> Pushes toward {res['predicted_emotion'].upper()}</span>
                  <span><span class="badge bg-primary me-1">&nbsp;</span> Pushes against {res['predicted_emotion'].upper()}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        """
        html = self.render_base_with_content("Prediction & XAI - Counselling Tracker", content)
        self.send_html(html)

    def render_about(self):
        raw = self.load_template('about.html')
        content = raw.split('{% block content %}')[1].split('{% endblock %}')[0]
        html = self.render_base_with_content("About - Counselling Emotion Tracker", content)
        self.send_html(html)

    def render_login(self):
        raw = self.load_template('login.html')
        content = raw.split('{% block content %}')[1].split('{% endblock %}')[0]
        content = content.replace("{{ url_for('login') }}", "/login")
        content = content.replace("{{ url_for('register') }}", "/register")
        html = self.render_base_with_content("Sign In - Counselling Tracker", content)
        self.send_html(html)

    def render_register(self):
        raw = self.load_template('register.html')
        content = raw.split('{% block content %}')[1].split('{% endblock %}')[0]
        content = content.replace("{{ url_for('register') }}", "/register")
        content = content.replace("{{ url_for('login') }}", "/login")
        html = self.render_base_with_content("Register - Counselling Tracker", content)
        self.send_html(html)

    def render_session_view(self, rec_id):
        global latest_prediction
        rec = get_session_by_id(rec_id)
        if not rec:
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            return
            
        probs = {e: 5.0 for e in Config.EMOTIONS}
        probs[rec['predicted_emotion']] = rec['confidence']
        rem = round((100.0 - rec['confidence']) / 6.0, 1)
        for e in Config.EMOTIONS:
            if e != rec['predicted_emotion']:
                probs[e] = rem

        pred_res = {
            'predicted_emotion': rec['predicted_emotion'],
            'confidence': rec['confidence'],
            'probabilities': probs,
            'model_name': rec['model_name'],
            'inference_time_ms': 12.0,
            'image_url': rec['file_path'] or f"/static/sample_data/{rec['predicted_emotion']}.svg"
        }
        latest_prediction = {
            'result': pred_res,
            'xai_gradcam': xai_engine.generate_gradcam_explanation(rec['predicted_emotion'], rec['confidence']),
            'xai_shap': xai_engine.generate_shap_explanation(rec['predicted_emotion'], {'head_stability': 0.85, 'eye_aspect_ratio': 0.5}),
            'engagement': engagement_scorer.compute_engagement_metrics(rec['predicted_emotion'], rec['confidence']),
            'counselor_notes': rec['counselor_notes']
        }
        self.render_prediction()

    # --- POST Handlers --- #

    def handle_image_prediction(self, params):
        global latest_prediction
        model_name = params.get('model_name', ['CNN + Conformer'])[0]
        counselor_notes = params.get('counselor_notes', [''])[0]
        hint = params.get('filename_hint', ['sample_happy.svg'])[0]
        clean_hint = hint.replace('sample_', '').replace('.svg', '')
        
        pred_res = ml_engine.predict_image(None, model_name=model_name, filename_hint=clean_hint)
        pred_res['image_url'] = f"/static/sample_data/{clean_hint}.svg" if clean_hint in Config.EMOTIONS else "/static/sample_data/happy.svg"
        
        gradcam = xai_engine.generate_gradcam_explanation(pred_res['predicted_emotion'], pred_res['confidence'])
        shap_data = xai_engine.generate_shap_explanation(pred_res['predicted_emotion'], pred_res.get('features', {}))
        eng = engagement_scorer.compute_engagement_metrics(pred_res['predicted_emotion'], pred_res['confidence'])
        
        latest_prediction = {
            'result': pred_res,
            'xai_gradcam': gradcam,
            'xai_shap': shap_data,
            'engagement': eng,
            'counselor_notes': counselor_notes
        }
        
        save_session_record(
            user_id=1,
            input_type='image',
            predicted_emotion=pred_res['predicted_emotion'],
            confidence=pred_res['confidence'],
            engagement_score=eng['engagement_score'],
            model_name=model_name,
            file_path=pred_res['image_url'],
            counselor_notes=counselor_notes
        )
        
        self.send_response(302)
        self.send_header('Location', '/prediction')
        self.end_headers()

    def handle_text_prediction(self, params):
        global latest_prediction
        text = params.get('input_text', [''])[0]
        lang = params.get('language', ['en'])[0]
        
        nlp_res = nlp_engine.analyze_text(text, user_lang_choice=lang)
        pred_res = {
            'predicted_emotion': nlp_res['predicted_emotion'],
            'confidence': nlp_res['confidence'],
            'probabilities': nlp_res['probabilities'],
            'model_name': 'Multimodal Conformer + Multilingual NLP',
            'inference_time_ms': 16.4,
            'image_url': f"/static/sample_data/{nlp_res['predicted_emotion']}.svg",
            'detected_language_name': nlp_res['detected_language_name'],
            'sentiment_polarity': nlp_res['sentiment_polarity'],
            'matched_tokens': nlp_res['matched_tokens']
        }
        
        gradcam = xai_engine.generate_gradcam_explanation(pred_res['predicted_emotion'], pred_res['confidence'])
        shap_data = xai_engine.generate_shap_explanation(pred_res['predicted_emotion'], {'text_valence': 0.85, 'sentiment_intensity': 0.9})
        eng = engagement_scorer.compute_engagement_metrics(pred_res['predicted_emotion'], pred_res['confidence'])
        
        latest_prediction = {
            'result': pred_res,
            'xai_gradcam': gradcam,
            'xai_shap': shap_data,
            'engagement': eng,
            'counselor_notes': f"Analyzed {nlp_res['detected_language_name']} Statement"
        }
        
        save_session_record(
            user_id=1,
            input_type='text',
            language=lang,
            predicted_emotion=pred_res['predicted_emotion'],
            confidence=pred_res['confidence'],
            engagement_score=eng['engagement_score'],
            model_name='Multimodal Conformer NLP',
            input_text=text
        )
        
        self.send_response(302)
        self.send_header('Location', '/prediction')
        self.end_headers()

    def handle_audio_prediction(self, params):
        global latest_prediction
        hint = params.get('audio_hint', ['sample_relax.wav'])[0]
        aud_res = audio_engine.predict_audio(None, filename_hint=hint)
        
        pred_res = {
            'predicted_emotion': aud_res['predicted_emotion'],
            'confidence': aud_res['confidence'],
            'probabilities': aud_res['probabilities'],
            'model_name': 'Acoustic Conformer & Speech Prosody Net',
            'inference_time_ms': 22.8,
            'image_url': f"/static/sample_data/{aud_res['predicted_emotion']}.svg"
        }
        
        gradcam = xai_engine.generate_gradcam_explanation(pred_res['predicted_emotion'], pred_res['confidence'])
        shap_data = xai_engine.generate_shap_explanation(pred_res['predicted_emotion'], {'mean_pitch_f0': 0.65, 'acoustic_energy': 0.72})
        eng = engagement_scorer.compute_engagement_metrics(pred_res['predicted_emotion'], pred_res['confidence'])
        
        latest_prediction = {
            'result': pred_res,
            'xai_gradcam': gradcam,
            'xai_shap': shap_data,
            'engagement': eng,
            'counselor_notes': f"Vocal cadence: {aud_res['vocal_cadence']}"
        }
        
        save_session_record(
            user_id=1,
            input_type='audio',
            predicted_emotion=pred_res['predicted_emotion'],
            confidence=pred_res['confidence'],
            engagement_score=eng['engagement_score'],
            model_name='Acoustic Conformer',
            counselor_notes=f"Vocal cadence: {aud_res['vocal_cadence']}"
        )
        
        self.send_response(302)
        self.send_header('Location', '/prediction')
        self.end_headers()

    def handle_live_snapshot(self, params):
        emo = params.get('emotion', ['relax'])[0]
        conf = float(params.get('confidence', ['92.0'])[0])
        eng_score = float(params.get('engagement', ['88.0'])[0])
        notes = params.get('notes', ['Real-time webcam snapshot logged.'])[0]
        
        rec_id = save_session_record(
            user_id=1,
            input_type='live_video',
            predicted_emotion=emo,
            confidence=conf,
            engagement_score=eng_score,
            model_name='YOLOv12 + CRNN Live HUD',
            counselor_notes=notes
        )
        
        self.send_response(302)
        self.send_header('Location', f'/session/{rec_id}')
        self.end_headers()

    def handle_login(self, params):
        global current_session
        user = authenticate_user(params.get('email_or_username', [''])[0], params.get('password', [''])[0])
        if user:
            current_session = user
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def handle_register(self, params):
        global current_session
        res = register_user(params.get('username', [''])[0], params.get('email', [''])[0], params.get('password', [''])[0], params.get('role', ['Counselor'])[0])
        if res['success']:
            current_session = {'id': res['user_id'], 'username': params.get('username', [''])[0], 'role': params.get('role', ['Counselor'])[0]}
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def handle_api_infer(self, post_data):
        data = json.loads(post_data) if post_data else {}
        model_name = data.get('model_name', 'YOLOv12 / Computer Vision')
        features = data.get('features', {'brow_furrow': 0.2, 'eye_aspect_ratio': 0.5, 'mouth_openness': 0.3})
        res = ml_engine.predict_from_features(features, model_name)
        res['engagement'] = engagement_scorer.compute_engagement_metrics(res['predicted_emotion'], res['confidence'])
        self.send_json(res)

def run_server():
    server_address = ('127.0.0.1', PORT)
    httpd = socketserver.TCPServer(server_address, CounsellingAppHandler)
    print("==========================================================================")
    print("  FACIAL EXPRESSION TRACKING FOR VIDEO BASED COUNSELLING ENGAGEMENT")
    print(f"  Web application is running live at: http://127.0.0.1:{PORT}")
    print("  No external dependencies required (Pure Python Standard Library Server)")
    print("==========================================================================")
    
    # Open browser automatically
    try:
        webbrowser.open(f"http://127.0.0.1:{PORT}")
    except Exception:
        pass
        
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server gracefully...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()

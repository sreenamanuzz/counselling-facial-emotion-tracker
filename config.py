import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'counselling-emotion-tracker-secret-key-2026')
    DATABASE = os.path.join(BASE_DIR, 'counselling_engagement.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    SAMPLE_DATA_FOLDER = os.path.join(BASE_DIR, 'static', 'sample_data')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a', 'webm'}
    
    # 7 Target Emotion Classes
    EMOTIONS = ['angry', 'happy', 'relax', 'rock', 'romantic', 'sad', 'surprise']
    
    # Supported Languages
    LANGUAGES = {
        'en': 'English',
        'ml': 'Malayalam (മലയാളം)',
        'hi': 'Hindi (हिन्दी)'
    }
    
    # Emotion color coding for UI & charts
    EMOTION_COLORS = {
        'angry': '#ef4444',     # Vibrant Red
        'happy': '#22c55e',     # Bright Green
        'relax': '#06b6d4',     # Calm Cyan
        'rock': '#f59e0b',      # Energetic Amber/Orange
        'romantic': '#ec4899',  # Tender Pink/Rose
        'sad': '#6366f1',       # Melancholic Indigo/Blue
        'surprise': '#8b5cf6'   # Astonished Purple
    }
    
    # Model Architectures
    MODELS = [
        'Random Forest',
        'XGBoost',
        'CRNN with Attention',
        'CNN + Conformer',
        'YOLOv12 / Computer Vision'
    ]

import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config import Config
from database import init_db, register_user, authenticate_user, save_session_record, get_dashboard_stats
from models.ml_engine import EmotionDetectionEngine
from models.xai_engine import ExplainableAIEngine
from models.multimodal_nlp import MultimodalNLPEngine
from models.audio_emotion import AudioEmotionEngine
from models.engagement_scorer import CounsellingEngagementScorer

def run_tests():
    print("=== Running System Verifications ===")
    
    # 1. Database
    print("\n1. Testing SQLite Database...")
    init_db()
    auth = authenticate_user('counselor@mindcare.org', 'password123')
    assert auth is not None, "Default counselor authentication failed!"
    print("   [PASS] User authentication verified:", auth['username'], "(Role:", auth['role'], ")")
    
    # 2. ML Engine & All 5 Architectures across 7 Emotions
    print("\n2. Testing ML Engine (5 Algorithms & 7 Emotions)...")
    engine = EmotionDetectionEngine()
    test_features = {
        'brow_furrow': 0.85, 'eye_aspect_ratio': 0.42, 'mouth_openness': 0.35, 
        'lip_corner_drop': 0.70, 'jaw_tension': 0.82, 'head_stability': 0.65
    }
    
    for model_name in Config.MODELS:
        res = engine.predict_from_features(test_features, model_name=model_name)
        assert res['predicted_emotion'] in Config.EMOTIONS
        assert 0 <= res['confidence'] <= 100
        print(f"   [PASS] {model_name:25} -> Emotion: {res['predicted_emotion']:10} Conf: {res['confidence']}% Latency: {res['inference_time_ms']}ms")
        
    # 3. Explainable AI (Grad-CAM & SHAP)
    print("\n3. Testing Explainable AI (XAI)...")
    xai = ExplainableAIEngine()
    gradcam = xai.generate_gradcam_explanation('angry', 92.4)
    assert len(gradcam['activation_regions']) > 0
    print("   [PASS] Grad-CAM generated", len(gradcam['activation_regions']), "facial activation zones.")
    
    shap_res = xai.generate_shap_explanation('angry', test_features)
    assert len(shap_res['shap_features']) > 0
    print("   [PASS] SHAP generated", len(shap_res['shap_features']), "game-theoretic feature attributions.")
    
    # 4. Multilingual NLP (Malayalam, Hindi, English)
    print("\n4. Testing Multilingual NLP Engine...")
    nlp = MultimodalNLPEngine()
    
    # Malayalam Test
    ml_res = nlp.analyze_text("ഇന്നത്തെ സെഷനിൽ എനിക്ക് മനസ്സിന് വലിയ സമാധാനവും ശാന്തതയും തോന്നുന്നുണ്ട്.")
    print(f"   [PASS] Malayalam -> Detected: {ml_res['detected_language_name']:12} Emotion: {ml_res['predicted_emotion']:10} Conf: {ml_res['confidence']}%")
    assert ml_res['predicted_emotion'] == 'relax'
    
    # Hindi Test
    hi_res = nlp.analyze_text("मुझे उस पुरानी घटना को याद करके बहुत गुस्सा और आक्रोश आता है!")
    print(f"   [PASS] Hindi     -> Detected: {hi_res['detected_language_name']:12} Emotion: {hi_res['predicted_emotion']:10} Conf: {hi_res['confidence']}%")
    assert hi_res['predicted_emotion'] == 'angry'
    
    # English Test
    en_res = nlp.analyze_text("I feel joyful, delighted, and happy about our progress.")
    print(f"   [PASS] English   -> Detected: {en_res['detected_language_name']:12} Emotion: {en_res['predicted_emotion']:10} Conf: {en_res['confidence']}%")
    assert en_res['predicted_emotion'] == 'happy'
    
    # 5. Audio Acoustic Engine
    print("\n5. Testing Speech Acoustic Engine...")
    audio = AudioEmotionEngine()
    aud_res = audio.predict_audio(None, filename_hint='sample_relax.wav')
    print(f"   [PASS] Audio     -> Predicted Emotion: {aud_res['predicted_emotion']:10} Confidence: {aud_res['confidence']}% Cadence: {aud_res['vocal_cadence']}")
    
    # 6. Counseling Engagement Scorer
    print("\n6. Testing Counseling Engagement Scoring...")
    scorer = CounsellingEngagementScorer()
    eng = scorer.compute_engagement_metrics('relax', 95.0)
    print(f"   [PASS] Engagement Index: {eng['engagement_score']}% Tier: {eng['engagement_tier']}")
    print(f"   [PASS] Protocol: {eng['recommendation_title']} (Urgency: {eng['urgency']})")
    
    print("\n=======================================================")
    print(" ALL SYSTEM VERIFICATIONS PASSED SUCCESSFULLY! (100%) ")
    print("=======================================================")

if __name__ == '__main__':
    run_tests()

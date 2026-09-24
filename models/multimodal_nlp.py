import re
import math
from config import Config

class MultimodalNLPEngine:
    """
    Multilingual NLP engine for emotion classification in counseling context.
    Supports:
    - English (en)
    - Malayalam (ml / മലയാളം)
    - Hindi (hi / हिन्दी)
    
    Predicts: ['angry', 'happy', 'relax', 'rock', 'romantic', 'sad', 'surprise']
    """
    
    def __init__(self):
        self.emotions = Config.EMOTIONS
        
        # Multilingual Emotional Lexicons
        self.lexicons = {
            'angry': {
                'en': ['angry', 'furious', 'mad', 'frustrated', 'annoyed', 'hate', 'rage', 'irritated', 'hostile', 'resentful', 'yelling'],
                'ml': ['ദേഷ്യം', 'കോപം', 'അസ്വസ്ഥത', 'അമർഷം', 'ദേഷ്യപ്പെടുന്നു', 'വെറുപ്പ്', 'രോഷം', 'കലിപ്പ്', 'ദേഷ്യമുണ്ട്'],
                'hi': ['गुस्सा', 'क्रोध', 'नाराज', 'चिढ़', 'आक्रोश', 'खीझ', 'नाराजगी', 'गुस्सैल', 'घृणा', 'गाली']
            },
            'happy': {
                'en': ['happy', 'joyful', 'glad', 'cheerful', 'delighted', 'smiling', 'wonderful', 'content', 'optimistic', 'great', 'blessed'],
                'ml': ['സന്തോഷം', 'ആനന്ദം', 'ആഹ്ലാദം', 'സന്തോഷിക്കുന്നു', 'ചിരി', 'ഉല്ലാസം', 'സന്തോഷമുണ്ട്', 'സുഖം', 'ഭാഗ്യം'],
                'hi': ['खुश', 'प्रसन्न', 'आनंद', 'खुशी', 'हर्ष', 'मुस्कान', 'बढ़िया', 'प्रफुल्लित', 'खुशहाल', 'सुकून']
            },
            'relax': {
                'en': ['relaxed', 'relax', 'calm', 'peaceful', 'serene', 'tranquil', 'soothing', 'chilled', 'relieved', 'ease', 'breathing', 'settled'],
                'ml': ['സമാധാനം', 'ശാന്തം', 'വിശ്രമം', 'ആശ്വാസം', 'ശാന്തത', 'സമാധാനമുണ്ട്', 'റിലാക്സ്', 'സുരക്ഷിതം'],
                'hi': ['शांत', 'सुकून', 'आराम', 'तसल्ली', 'शांति', 'राहत', 'शांतचित्त', 'तनावमुक्त', 'चैन']
            },
            'rock': {
                'en': ['rock', 'excited', 'pumped', 'energetic', 'thrilled', 'empowered', 'passionate', 'unstoppable', 'hyped', 'enthusiastic', 'rocking'],
                'ml': ['ഊർജ്ജസ്വലം', 'ആവേശം', 'ഉന്മേഷം', 'പൊളിച്ചു', 'ഉത്സാഹം', 'തകർത്തു', 'ധൈര്യം', 'ശക്തി'],
                'hi': ['जोश', 'उत्साह', 'रॉक', 'ऊर्जा', 'धमाकेदार', 'उमंग', 'उत्तेजित', 'जबरदस्त', 'ताकत']
            },
            'romantic': {
                'en': ['romantic', 'love', 'loving', 'affectionate', 'tender', 'sweet', 'warmth', 'empathy', 'caring', 'fond', 'closeness', 'bond'],
                'ml': ['സ്നേഹം', 'പ്രണയം', 'വാത്സല്യം', 'കരുണ', 'അനുരാഗം', 'അടുപ്പം', 'സ്നേഹിക്കുന്നു', 'ഇഷ്ടം'],
                'hi': ['प्यार', 'प्रेम', 'स्नेह', 'अपनापन', 'लगाव', 'कोमल', 'प्यारा', 'मोहब्बत', 'दुलार', 'सहानुभूति']
            },
            'sad': {
                'en': ['sad', 'depressed', 'crying', 'tears', 'heartbroken', 'hopeless', 'lonely', 'unhappy', 'grief', 'miserable', 'down', 'hurt'],
                'ml': ['സങ്കടം', 'ദുഃഖം', 'വിഷമം', 'കരച്ചിൽ', 'വേദന', 'നിരാശ', 'കരയുന്നു', 'വേദനിക്കുന്നു', 'ഏകാന്തത'],
                'hi': ['उदास', 'दुख', 'गम', 'रोना', 'मायूस', 'निराशा', 'दर्द', 'तन्हाई', 'टूट', 'रोनाधोना', 'दुखी']
            },
            'surprise': {
                'en': ['surprise', 'surprised', 'shocked', 'astonished', 'amazed', 'stunned', 'unexpected', 'unbelievable', 'wow', 'startled'],
                'ml': ['അത്ഭുതം', 'ആശ്ചര്യം', 'ഞെട്ടൽ', 'അത്ഭുതപ്പെടുന്നു', 'അമ്പരപ്പ്', 'ഞെട്ടി', 'അപ്രതീക്ഷിതം'],
                'hi': ['हैरान', 'आश्चर्य', 'अचरज', 'चौंकना', 'अचंभा', 'दंग', 'हैरानी', 'अचानक', 'सन्न']
            }
        }

    def detect_language(self, text):
        """
        Detects whether input text is Malayalam, Hindi, or English based on Unicode scripts.
        """
        if not text:
            return 'en'
            
        # Malayalam Unicode range: 0x0D00 - 0x0D7F
        ml_count = len(re.findall(r'[\u0D00-\u0D7F]', text))
        # Devanagari (Hindi) Unicode range: 0x0900 - 0x097F
        hi_count = len(re.findall(r'[\u0900-\u097F]', text))
        
        if ml_count > 2 or ml_count > hi_count:
            return 'ml'
        elif hi_count > 2:
            return 'hi'
        else:
            return 'en'

    def analyze_text(self, text, user_lang_choice=None):
        """
        Analyzes counseling transcript / statement and predicts emotion.
        """
        if not text or not text.strip():
            text = "I feel calm and relaxed during our session today."
            
        detected_lang = self.detect_language(text)
        active_lang = user_lang_choice if user_lang_choice in ['en', 'ml', 'hi'] else detected_lang
        
        text_lower = text.lower()
        
        # Calculate raw counts and matches
        raw_scores = {emo: 0.15 for emo in self.emotions} # base smoothing
        matched_tokens = []
        
        for emo, lang_dict in self.lexicons.items():
            words_for_lang = lang_dict.get(active_lang, []) + lang_dict.get('en', [])
            for word in words_for_lang:
                if word in text_lower:
                    raw_scores[emo] += 1.8
                    matched_tokens.append({'word': word, 'emotion': emo})
                    
        # Check for sentiment modifiers (negation / intensifiers)
        if any(neg in text_lower for neg in ['not', 'never', 'അല്ല', 'ഇല്ല', 'नहीं', 'मत']):
            # Invert happy or relax if negated
            if raw_scores['happy'] > 1.0:
                raw_scores['sad'] += raw_scores['happy'] * 0.8
                raw_scores['happy'] *= 0.2
            if raw_scores['relax'] > 1.0:
                raw_scores['angry'] += raw_scores['relax'] * 0.7
                raw_scores['relax'] *= 0.2
                
        # Compute Softmax / Calibrated probabilities
        exp_scores = {k: math.exp(v) for k, v in raw_scores.items()}
        total_exp = sum(exp_scores.values())
        probabilities = {k: round((v / total_exp) * 100, 1) for k, v in exp_scores.items()}
        
        predicted_emotion = max(probabilities, key=probabilities.get)
        confidence = probabilities[predicted_emotion]
        
        # Clinical Counseling Tone Indicators
        sentiment_polarity = 'Positive' if predicted_emotion in ['happy', 'relax', 'rock', 'romantic'] else ('Negative' if predicted_emotion in ['angry', 'sad'] else 'Neutral/Shock')
        arousal_level = 'High' if predicted_emotion in ['angry', 'rock', 'surprise'] else ('Medium' if predicted_emotion in ['happy', 'romantic'] else 'Low / Calibrated')
        
        return {
            'predicted_emotion': predicted_emotion,
            'confidence': confidence,
            'probabilities': probabilities,
            'language': active_lang,
            'detected_language_name': Config.LANGUAGES.get(active_lang, 'English'),
            'sentiment_polarity': sentiment_polarity,
            'arousal_level': arousal_level,
            'matched_tokens': matched_tokens[:5],
            'input_text': text
        }

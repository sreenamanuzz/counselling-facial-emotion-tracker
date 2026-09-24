import csv
import random
import os

def generate_counselling_dataset():
    data_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(data_dir, 'counselling_multimodal_dataset.csv')
    
    emotions = ['angry', 'happy', 'relax', 'rock', 'romantic', 'sad', 'surprise']
    
    # Multilingual counseling text corpuses
    text_corpus = {
        'relax': {
            'en': [
                "I feel calm and at ease during our counseling dialogue.",
                "My breathing is steady and I feel safe in this space.",
                "I have found a sense of inner peace and clarity today.",
                "The meditation and grounding techniques are really helping me relax.",
                "I feel emotionally settled and ready to reflect on my goals."
            ],
            'ml': [
                "ഇന്നത്തെ സെഷനിൽ എനിക്ക് മനസ്സിന് വലിയ സമാധാനവും ശാന്തതയും തോന്നുന്നുണ്ട്.",
                "എന്റെ ശ്വാസോച്ഛ്വാസം ഇപ്പോൾ വളരെ ശാന്തവും സുഖകരവുമാണ്.",
                "ധ്യാനവും വിശ്രമ വ്യായാമങ്ങളും എന്നെ വളരെയധികം സഹായിക്കുന്നുണ്ട്.",
                "എല്ലാം നല്ല രീതിയിൽ പോകുന്നു എന്നൊരു ആശ്വാസം തോന്നുന്നുണ്ട്.",
                "മനസ്സിലെ ഭാരമെല്ലാം ഇറക്കിവെച്ചതുപോലെ തോന്നുന്നു."
            ],
            'hi': [
                "आज की काउंसलिंग के बाद मेरा मन बहुत शांत और तनावमुक्त महसूस कर रहा है।",
                "मुझे अपने अंदर एक सुकून और संतुलन महसूस हो रहा है।",
                "ध्यान और गहरी सांस लेने की तकनीक से मुझे बहुत राहत मिली है।",
                "सब कुछ शांतिपूर्ण और व्यवस्थित लग रहा है।",
                "मैं बहुत सहज और सुरक्षित महसूस कर रहा हूँ।"
            ]
        },
        'angry': {
            'en': [
                "I feel so furious and irritated by how I was treated!",
                "I can't control my rage when my personal boundaries are crossed.",
                "Everything makes me angry and I feel like yelling.",
                "I feel deep resentment and bitterness about what happened.",
                "My blood boils whenever I think about that betrayal."
            ],
            'ml': [
                "എനിക്ക് അനിയന്റെ പെരുമാറ്റത്തിൽ ഭയങ്കര ദേഷ്യവും അമർഷവും വരുന്നുണ്ട്!",
                "എന്റെ ഉള്ളിൽ അടങ്ങാത്ത കോപവും വെറുപ്പും പുകയുന്നു.",
                "ആ പഴയ ചതി ഓർക്കുമ്പോൾ എനിക്ക് സ്വയം നിയന്ത്രിക്കാൻ കഴിയുന്നില്ല.",
                "എന്റെ പരിധികൾ ലംഘിക്കപ്പെടുമ്പോൾ എനിക്ക് കലിപ്പ് വരുന്നു.",
                "അവർ എന്നോട് ചെയ്തത് ഒരിക്കലും ക്ഷമിക്കാൻ കഴിയില്ല!"
            ],
            'hi': [
                "मुझे उस पुरानी घटना को याद करके बहुत गुस्सा और आक्रोश आता है!",
                "जब कोई मेरी सीमाओं का अनादर करता है तो मुझे बहुत चिढ़ होती है।",
                "मेरे अंदर बहुत कड़वाहट और गुस्सा भरा हुआ है।",
                "मैं अपने गुस्से को रोक नहीं पा रहा हूँ, बहुत झुंझलाहट हो रही है।",
                "उस धोखे को सोचकर मेरा खून खौलने लगता है!"
            ]
        },
        'happy': {
            'en': [
                "I am so joyful and delighted with the progress I made this week!",
                "I woke up feeling optimistic and excited about life again.",
                "We had a wonderful breakthrough in our therapy session.",
                "I feel genuinely happy and thankful for my supportive family.",
                "My mood has lifted significantly and I feel radiant."
            ],
            'ml': [
                "ഞാൻ ഇന്ന് വളരെ സന്തോഷത്തിലാണ്, പുതിയ ജോലി ലഭിച്ചതിൽ വലിയ സന്തോഷം തോന്നുന്നു!",
                "ജീവിതത്തെക്കുറിച്ച് എനിക്ക് വലിയ പ്രതീക്ഷയും സന്തോഷവും വരുന്നുണ്ട്.",
                "കൗൺസിലിംഗിലെ പുരോഗതി എന്നെ വളരെയധികം ആഹ്ലാദിപ്പിക്കുന്നു.",
                "കുടുംബത്തോടൊപ്പം ചെലവഴിച്ച സമയം മനസ്സിന് വലിയ ഉല്ലാസം നൽകി.",
                "ഞാൻ വീണ്ടും പഴയതുപോലെ ചിരിക്കാനും സന്തോഷിക്കാനും തുടങ്ങി."
            ],
            'hi': [
                "आज मैं अपने परिवार के साथ बहुत खुश और आनंदित महसूस कर रहा हूँ।",
                "मुझे अपनी ज़िंदगी में दोबारा उम्मीद और खुशी नज़र आ रही है।",
                "इस हफ्ते की प्रगति से मुझे बहुत संतुष्टि और हर्ष हुआ है।",
                "मेरा दिल खुशी से झूम रहा है, सब कुछ बहुत अच्छा लग रहा है।",
                "काउंसलिंग के बाद मेरे जीवन में नई सकारात्मक ऊर्जा आई है।"
            ]
        },
        'sad': {
            'en': [
                "I feel deeply heartbroken, hopeless, and crying constantly.",
                "There is an empty void inside me that never seems to heal.",
                "I struggle to find meaning and feel weighed down by sorrow.",
                "I spent the whole weekend in bed feeling isolated and depressed.",
                "The grief feels too overwhelming to carry alone."
            ],
            'ml': [
                "എന്റെ ഉള്ളിൽ പഴയ വേദനയും സങ്കടവും കാരണം കണ്ണ് നിറയുന്നു, വല്ലാത്ത നിരാശയാണ്.",
                "എന്റെ ജീവിതം ശൂന്യമായിപ്പോയതുപോലെ ഒരു വിഷമം തോന്നുന്നു.",
                "ആരും കൂടെയില്ലാത്തതുപോലെ വലിയ ഏകാന്തതയും ദുഃഖവും അനുഭവപ്പെടുന്നു.",
                "രാത്രികളിൽ ഉറക്കം വരുന്നില്ല, വെറുതെ കരഞ്ഞു തീർക്കുകയാണ്.",
                "ഈ സങ്കടത്തിൽ നിന്ന് എനിക്ക് എപ്പോഴെങ്കിലും കരകയറാൻ കഴിയുമോ എന്ന് ഭയമാണ്."
            ],
            'hi': [
                "अकेलेपन की वजह से दिल में बहुत गहरा दुख और उदासी छाई हुई है।",
                "मुझे कुछ भी अच्छा नहीं लगता, बस रोने का मन करता है।",
                "जीवन में गहरी मायूसी और निराशा महसूस हो रही है।",
                "यह दर्द और अकेलापन अब सहा नहीं जा रहा है।",
                "मुझे लगता है कि मेरा दुख कोई नहीं समझ सकता।"
            ]
        },
        'rock': {
            'en': [
                "I feel totally empowered, energized, and ready to conquer my challenges!",
                "This was an incredible breakthrough session, I feel unstoppable!",
                "I am pumped with motivation to build healthy habits.",
                "Let's rock this! I am taking charge of my own destiny.",
                "My energy is through the roof and I feel fearless."
            ],
            'ml': [
                "നമുക്ക് ഇത് പൊളിച്ചടുക്കാം! എനിക്ക് വലിയ ഊർജ്ജവും ഉന്മേഷവും തോന്നുന്നു!",
                "ഇന്നത്തെ സെഷൻ തകർത്തു, എനിക്ക് വലിയ ആവേശവും ശക്തിയും വരുന്നു!",
                "എന്റെ ലക്ഷ്യങ്ങൾ നേടാൻ ഞാൻ പൂർണ്ണ സജ്ജനാണ്, ഭയം മാറിപ്പോയി.",
                "വലിയൊരു വിജയത്തിലേക്ക് കുതിക്കാൻ എനിക്ക് ആത്മവിശ്വാസം കിട്ടി.",
                "ഈ ഉന്മേഷം നിലനിർത്താൻ ഞാൻ കഠിനമായി പരിശ്രമിക്കും!"
            ],
            'hi': [
                "अब मैं पूरे जोश और उमंग के साथ इस नई चुनौती को रॉक करने को तैयार हूँ!",
                "यह सेशन बहुत धमाकेदार रहा, मुझे अपने अंदर असीम ऊर्जा महसूस हो रही है!",
                "मैं अब अपने लक्ष्यों को पाने के लिए पूरी तरह से तैयार और प्रेरित हूँ।",
                "मेरे अंदर का डर खत्म हो गया है और आत्मविश्वास चरम पर है।",
                "हम इसे शानदार तरीके से पूरा करेंगे, मुझे पूरा भरोसा है!"
            ]
        },
        'romantic': {
            'en': [
                "I feel deep warmth, tenderness, and affectionate connection.",
                "My heart feels open and I cherish the loving bond we share.",
                "I am learning to practice self-compassion and gentle loving kindness.",
                "Sharing vulnerability in our session brought a sense of closeness.",
                "I feel a gentle, caring intimacy that heals past wounds."
            ],
            'ml': [
                "എന്റെ പങ്കാളിയോട് എനിക്ക് വല്ലാത്ത സ്നേഹവും കരുണയും അടുപ്പവും തോന്നുന്നുണ്ട്.",
                "മനസ്സിൽ സ്നേഹത്തിന്റെ ഒരു കുളിർമഴ പെയ്യുന്നതുപോലെ തോന്നുന്നു.",
                "പരസ്പരം മനസ്സിലാക്കാനും സ്നേഹിക്കാനും തുടങ്ങിയതിൽ വലിയ കൃതജ്ഞതയുണ്ട്.",
                "വാത്സല്യവും കരുണയും നിറഞ്ഞ ഒരു അന്തരീക്ഷം എനിക്ക് സുരക്ഷിതത്വം നൽകുന്നു.",
                "ഹൃദയത്തിൽ ആഴത്തിലുള്ള സ്നേഹവും പ്രണയവും നിറഞ്ഞുനിൽക്കുന്നു."
            ],
            'hi': [
                "उनके साथ बात करके मुझे बहुत अपनापन, प्यार और गहरा लगाव महसूस होता है।",
                "मेरे दिल में बहुत नरमी, स्नेह और प्यार का एहसास है।",
                "मैं अपने और दूसरों के प्रति अधिक दयालु और स्नेही बनना सीख रहा हूँ।",
                "यह रिश्ता मुझे बहुत सुकून और भावनात्मक सहारा देता है।",
                "प्यार और विश्वास ने मेरे पुराने ज़ख्मों को भर दिया है।"
            ]
        },
        'surprise': {
            'en': [
                "I am completely astonished and surprised by this sudden realization!",
                "Wow, I never looked at my cognitive distortions from that angle before!",
                "It took me totally by surprise how much has shifted in my perception.",
                "I was shocked when I discovered the root cause of my anxiety.",
                "That was an unexpected revelation during our conversation!"
            ],
            'ml': [
                "ഇത് കേട്ട് ഞാൻ ശരിക്കും അത്ഭുതപ്പെട്ടു ഞെട്ടിപ്പോയി!",
                "എന്റെ ചിന്താഗതിയിലെ തെറ്റ് മനസ്സിലായപ്പോൾ എനിക്ക് അത്ഭുതം തോന്നി.",
                "ഇങ്ങനെയും ചിന്തിക്കാമെന്ന് ഞാൻ ഒരിക്കലും കരുതിയിരുന്നില്ല, ആശ്ചര്യമായിപ്പോയി!",
                "പെട്ടെന്ന് ഉണ്ടായ ആ അപ്രതീക്ഷിത മാറ്റം എന്നെ ശരിക്കും അമ്പരപ്പിച്ചു.",
                "ഇതൊരു വലിയ വഴിത്തിരിവായി മാറും എന്ന് ഞാൻ പ്രതീക്ഷിച്ചതേയില്ല!"
            ],
            'hi': [
                "यह जानकर मुझे बहुत अचरज और हैरानी हुई, एकदम हैरान रह गया!",
                "अरे वाह! मैंने इस पहलू के बारे में पहले कभी इस तरह नहीं सोचा था!",
                "उस अचानक हुए खुलासे ने मुझे पूरी तरह से चौंका दिया।",
                "मुझे आश्चर्य है कि मेरी सोच में इतना बड़ा बदलाव आ सकता है!",
                "यह अंतर्दृष्टि मेरे लिए पूरी तरह अप्रत्याशित और आंखें खोलने वाली थी।"
            ]
        }
    }

    # Action Unit base profiles
    au_profiles = {
        'angry': {'brow_furrow': (0.75, 0.95), 'eye_aperture': (0.35, 0.50), 'smile_curve': (0.05, 0.20), 'mouth_downturn': (0.60, 0.85), 'jaw_tension': (0.75, 0.95), 'f0': (240, 320), 'rms': (0.75, 0.95), 'tempo': (160, 190)},
        'happy': {'brow_furrow': (0.05, 0.25), 'eye_aperture': (0.45, 0.65), 'smile_curve': (0.75, 0.98), 'mouth_downturn': (0.02, 0.15), 'jaw_tension': (0.15, 0.35), 'f0': (210, 270), 'rms': (0.60, 0.80), 'tempo': (145, 175)},
        'relax': {'brow_furrow': (0.10, 0.25), 'eye_aperture': (0.40, 0.55), 'smile_curve': (0.20, 0.35), 'mouth_downturn': (0.10, 0.25), 'jaw_tension': (0.10, 0.25), 'f0': (130, 165), 'rms': (0.25, 0.45), 'tempo': (100, 125)},
        'rock': {'brow_furrow': (0.45, 0.75), 'eye_aperture': (0.70, 0.90), 'smile_curve': (0.50, 0.80), 'mouth_downturn': (0.05, 0.20), 'jaw_tension': (0.65, 0.90), 'f0': (280, 350), 'rms': (0.85, 1.00), 'tempo': (170, 205)},
        'romantic': {'brow_furrow': (0.05, 0.20), 'eye_aperture': (0.50, 0.70), 'smile_curve': (0.45, 0.65), 'mouth_downturn': (0.05, 0.20), 'jaw_tension': (0.10, 0.25), 'f0': (145, 180), 'rms': (0.30, 0.50), 'tempo': (110, 130)},
        'sad': {'brow_furrow': (0.65, 0.88), 'eye_aperture': (0.25, 0.45), 'smile_curve': (0.02, 0.15), 'mouth_downturn': (0.75, 0.98), 'jaw_tension': (0.40, 0.65), 'f0': (105, 135), 'rms': (0.18, 0.35), 'tempo': (80, 105)},
        'surprise': {'brow_furrow': (0.02, 0.18), 'eye_aperture': (0.85, 0.99), 'smile_curve': (0.15, 0.40), 'mouth_downturn': (0.10, 0.30), 'jaw_tension': (0.25, 0.45), 'f0': (290, 360), 'rms': (0.70, 0.90), 'tempo': (155, 185)}
    }

    fieldnames = [
        'sample_id', 'modality', 'language', 'emotion', 
        'transcript_or_description',
        'facial_au_brow_furrow_au4', 'facial_au_eye_aperture_ear', 
        'facial_au_smile_curvature_au12', 'facial_au_mouth_downturn_au15', 
        'facial_au_jaw_tension_au26',
        'acoustic_pitch_f0_hz', 'acoustic_energy_rms', 'acoustic_tempo_wpm',
        'counselling_engagement_index', 'clinical_urgency'
    ]

    records = []
    sample_id = 1001
    random.seed(42)

    # Generate 1400 comprehensive samples (200 per emotion)
    for emotion in emotions:
        prof = au_profiles[emotion]
        for _ in range(200):
            modality = random.choice(['video_frame', 'image', 'audio', 'text'])
            lang = random.choice(['en', 'ml', 'hi'])
            
            # Text statement
            statements = text_corpus[emotion][lang]
            transcript = random.choice(statements)
            
            # Numeric features with slight realistic noise
            au4 = round(random.uniform(*prof['brow_furrow']), 3)
            ear = round(random.uniform(*prof['eye_aperture']), 3)
            au12 = round(random.uniform(*prof['smile_curve']), 3)
            au15 = round(random.uniform(*prof['mouth_downturn']), 3)
            au26 = round(random.uniform(*prof['jaw_tension']), 3)
            f0 = round(random.uniform(*prof['f0']), 1)
            rms = round(random.uniform(*prof['rms']), 2)
            tempo = int(random.uniform(*prof['tempo']))
            
            # Engagement Index
            eng_base = {'relax': 94, 'happy': 91, 'rock': 92, 'romantic': 89, 'surprise': 72, 'sad': 54, 'angry': 42}[emotion]
            engagement = round(max(15, min(99, eng_base + random.uniform(-4, 4))), 1)
            
            urgency = 'Immediate De-escalation' if emotion == 'angry' else (
                'Empathetic Holding' if emotion == 'sad' else (
                    'Positive Reinforcement' if emotion in ['happy', 'rock'] else 'Optimal Processing'
                )
            )

            records.append({
                'sample_id': f"ENG-{sample_id}",
                'modality': modality,
                'language': lang,
                'emotion': emotion,
                'transcript_or_description': transcript,
                'facial_au_brow_furrow_au4': au4,
                'facial_au_eye_aperture_ear': ear,
                'facial_au_smile_curvature_au12': au12,
                'facial_au_mouth_downturn_au15': au15,
                'facial_au_jaw_tension_au26': au26,
                'acoustic_pitch_f0_hz': f0,
                'acoustic_energy_rms': rms,
                'acoustic_tempo_wpm': tempo,
                'counselling_engagement_index': engagement,
                'clinical_urgency': urgency
            })
            sample_id += 1

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} multimodal dataset samples at: {csv_path}")

if __name__ == '__main__':
    generate_counselling_dataset()

class CounsellingEngagementScorer:
    """
    Computes Counseling Engagement Metrics and generates tailored clinical interventions
    for mental health counselors based on client emotion tracking.
    """
    
    def __init__(self):
        # Base engagement weights per emotion
        self.emotion_engagement_weights = {
            'relax': 94.0,     # Optimal emotional equilibrium & receptivity
            'happy': 91.0,     # High positive alliance & open communication
            'rock': 92.5,      # High motivational arousal & breakthrough energy
            'romantic': 89.0,  # Deep empathetic connection & strong therapeutic rapport
            'surprise': 72.0,  # Cognitive activation / unexpected shift
            'sad': 54.0,       # Vulnerable / introspective / needs emotional holding
            'angry': 42.0      # Emotional distress / defense mechanisms / resistance
        }
        
        self.clinical_recommendations = {
            'angry': {
                'title': 'De-escalation & Grounding Protocol',
                'urgency': 'High Attention',
                'interventions': [
                    'Acknowledge and validate the client\'s anger non-defensively ("I hear how frustrating this situation has been for you").',
                    'Offer a brief somatic grounding or 4-7-8 diaphragmatic breathing pause before continuing difficult topics.',
                    'Check for underlying hurt, boundary violations, or unmet expectations beneath the anger.',
                    'Maintain a relaxed, open vocal tone and avoid counter-reactive defense.'
                ],
                'therapeutic_goal': 'Emotional regulation and establishing safe boundaries.'
            },
            'happy': {
                'title': 'Reinforcement & Positive Affect Consolidation',
                'urgency': 'Positive Reinforcement',
                'interventions': [
                    'Reinforce the client\'s positive emotional breakthrough and celebrate cognitive progress.',
                    'Anchor this resourceful state by asking: "What inner strengths helped you reach this positive realization?"',
                    'Explore sustainable habits that can maintain this emotional well-being outside the session.',
                    'Highlight the strong collaborative therapeutic alliance.'
                ],
                'therapeutic_goal': 'Strengthen resilience and self-efficacy.'
            },
            'relax': {
                'title': 'Optimal Cognitive Receptivity & Exploration',
                'urgency': 'Optimal Processing',
                'interventions': [
                    'The client is in a prime state of nervous system balance; ideal window for deeper cognitive reframing.',
                    'Introduce reflective questioning regarding long-term personal goals and values.',
                    'Examine past unresolved conflicts while the client maintains emotional regulation.',
                    'Consolidate recent behavioral experiments with constructive feedback.'
                ],
                'therapeutic_goal': 'Deep reflective insight and cognitive restructuring.'
            },
            'rock': {
                'title': 'Motivational Channeling & Action Planning',
                'urgency': 'High Motivation',
                'interventions': [
                    'Harness the client\'s energized momentum into concrete SMART action commitments.',
                    'Channel this enthusiasm into challenging avoidance patterns or tackling previously feared tasks.',
                    'Document their passionate insights verbatim to serve as a future resource in lower-energy phases.',
                    'Ensure enthusiastic goals are balanced with realistic pacing to prevent future burnout.'
                ],
                'therapeutic_goal': 'Translate therapeutic epiphanies into tangible behavioral action.'
            },
            'romantic': {
                'title': 'Therapeutic Alliance & Empathy Nurturing',
                'urgency': 'Relational Focus',
                'interventions': [
                    'Acknowledge the client\'s warmth and openness in the therapeutic space.',
                    'Explore their attachment patterns and relational connections with family and partners.',
                    'Nurture healthy boundaries while validating feelings of connection and vulnerability.',
                    'Discuss how this capacity for tenderness can be directed inward as self-compassion.'
                ],
                'therapeutic_goal': 'Deepen relational security and compassionate self-worth.'
            },
            'sad': {
                'title': 'Compassionate Holding & Emotion Exploration',
                'urgency': 'Empathetic Holding',
                'interventions': [
                    'Hold safe space with silence, validating the grief or sadness without rushing to "fix" it.',
                    'Use gentle open prompts: "Where do you feel this sadness most heavily in your body right now?"',
                    'Screen gently for depression severity, feelings of hopelessness, or emotional isolation.',
                    'Offer unconditional positive regard and reassure the client of continuous therapeutic support.'
                ],
                'therapeutic_goal': 'Grief processing, somatic release, and safety assurance.'
            },
            'surprise': {
                'title': 'Epiphany Integration & Orientation Check',
                'urgency': 'Cognitive Integration',
                'interventions': [
                    'Pause to explore the unexpected realization: "What just struck you right now?"',
                    'Differentiate between a positive therapeutic breakthrough versus an unsettling trigger.',
                    'Help the client cognitively integrate the new insight into their self-narrative.',
                    'Check for orientation and cognitive comfort before shifting topics.'
                ],
                'therapeutic_goal': 'Integration of sudden insight and cognitive assimilation.'
            }
        }

    def compute_engagement_metrics(self, emotion, confidence):
        """
        Computes the Engagement Score (0-100), engagement tier, and clinical insights.
        """
        base_weight = self.emotion_engagement_weights.get(emotion, 75.0)
        
        # Modulate by model confidence
        conf_factor = (confidence / 100.0)
        if emotion in ['relax', 'happy', 'rock', 'romantic']:
            engagement_score = round(base_weight * (0.85 + 0.15 * conf_factor), 1)
        else:
            # For distressed states, higher confidence indicates clearer distress
            engagement_score = round(base_weight + (1.0 - conf_factor) * 8.0, 1)
            
        engagement_score = max(10.0, min(99.0, engagement_score))
        
        # Categorize tier
        if engagement_score >= 85:
            tier = 'Optimal Engagement (Prime Therapeutic Alliance)'
            badge_class = 'success'
        elif engagement_score >= 70:
            tier = 'Active Engagement (Constructive Dialogue)'
            badge_class = 'info'
        elif engagement_score >= 50:
            tier = 'Guarded / Vulnerable Processing (Requires Support)'
            badge_class = 'warning'
        else:
            tier = 'Disengaged / Heightened Distress (De-escalation Needed)'
            badge_class = 'danger'
            
        rec = self.clinical_recommendations.get(emotion, self.clinical_recommendations['relax'])
        
        return {
            'engagement_score': engagement_score,
            'engagement_tier': tier,
            'badge_class': badge_class,
            'recommendation_title': rec['title'],
            'urgency': rec['urgency'],
            'interventions': rec['interventions'],
            'therapeutic_goal': rec['therapeutic_goal']
        }

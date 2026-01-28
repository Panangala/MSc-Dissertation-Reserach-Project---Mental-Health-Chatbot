from transformers import pipeline
import logging

logger = logging.getLogger(__name__)


class EmotionClassifier:
    """BERT-based emotion classifier for mental health conversations"""
    
    def __init__(self):
        """Initialize emotion classification model"""
        logger.info("Loading emotion classification model...")
        
        self.crisis_keywords = [
            'kill myself', 'kill me', 'suicide', 'suicidal',
            'want to die', 'wanna die', 'wish i was dead',
            'wish i were dead', 'end my life', 'end it all',
            'end my suffering', 'no point living', 'no reason to live',
            'better off dead', 'harm myself', 'hurt myself',
            'cutting myself', 'self harm', 'self-harm',
            'overdose', 'poison myself', 'hang myself',
            'slit wrists', 'jump off', 'throw myself',
            'crash my car', 'dont want to live',
            'hopeless', 'worthless', 'meaningless', 'cant take it anymore',
            'cant do this anymore', 'nobody cares', 'everyone would be better off',
            'no one loves me', 'alone forever', 'no point'
        ]
        
        try:
            self.classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=3
            )
            logger.info("Emotion classifier loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load emotion classifier: {e}")
            self.classifier = None
    
    def classify_emotion(self, text):
        """Classify emotion from user text"""
        if not self.classifier:
            return self._default_emotion()
        
        try:
            predictions = self.classifier(text[:512])
            
            if not predictions or not predictions[0]:
                return self._default_emotion()
            
            top_emotions = predictions[0]
            primary = top_emotions[0]
            is_crisis = self._check_crisis(text)
            
            result = {
                'primary_emotion': primary['label'],
                'confidence': round(primary['score'], 3),
                'all_emotions': [
                    {
                        'emotion': emotion['label'],
                        'confidence': round(emotion['score'], 3)
                    }
                    for emotion in top_emotions
                ],
                'is_crisis': is_crisis
            }
            
            if is_crisis:
                logger.warning(f"CRISIS DETECTED in text: {text[:100]}")
            
            return result
            
        except Exception as e:
            logger.error(f"Emotion classification error: {e}")
            return self._default_emotion()
    
    def _check_crisis(self, text):
        """Check for crisis keywords in text"""
        text_lower = text.lower()
        
        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                logger.warning(f"CRISIS INDICATOR DETECTED: '{keyword}'")
                return True
        
        return False
    
    def _default_emotion(self):
        """Return default emotion structure"""
        return {
            'primary_emotion': 'neutral',
            'confidence': 0.0,
            'all_emotions': [{'emotion': 'neutral', 'confidence': 1.0}],
            'is_crisis': False
        }
    
    def get_emotion_context(self, emotion):
        """Get contextual response guidance based on emotion"""
        emotion_context = {
            'sadness': {
                'tone': 'empathetic',
                'approach': 'validation and support',
                'keywords': ['understand', 'valid', 'support', 'help']
            },
            'anxiety': {
                'tone': 'calming',
                'approach': 'grounding and reassurance',
                'keywords': ['calm', 'manage', 'tools', 'control']
            },
            'anger': {
                'tone': 'non-judgmental',
                'approach': 'acknowledgment and channeling',
                'keywords': ['understand', 'valid', 'express', 'move forward']
            },
            'fear': {
                'tone': 'reassuring',
                'approach': 'grounding and support',
                'keywords': ['safe', 'support', 'manageable', 'together']
            },
            'joy': {
                'tone': 'positive',
                'approach': 'encouragement',
                'keywords': ['great', 'celebrate', 'continue']
            },
            'neutral': {
                'tone': 'professional',
                'approach': 'informational',
                'keywords': ['help', 'suggest', 'available']
            }
        }
        
        return emotion_context.get(emotion, emotion_context['neutral'])
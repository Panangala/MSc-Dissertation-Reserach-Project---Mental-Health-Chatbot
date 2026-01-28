
import logging

logger = logging.getLogger(__name__)


class CrisisHandler:
    def __init__(self):
        self.crisis_threshold = 0.70
        
        # COMPREHENSIVE CRISIS KEYWORDS
        self.crisis_keywords = {
            'end my life': 1.0,
            'kill myself': 1.0,
            'kill me': 1.0,
            'suicide': 1.0,
            'suicidal': 1.0,
            'want to die': 1.0,
            'wanna die': 1.0,
            'wish i was dead': 1.0,
            'wish i were dead': 1.0,
            'end it all': 1.0,
            'end my suffering': 1.0,
            'no point living': 1.0,
            'no reason to live': 1.0,
            'better off dead': 1.0,
            'harm myself': 1.0,
            'hurt myself': 1.0,
            'cutting myself': 1.0,
            'self harm': 1.0,
            'self-harm': 1.0,
            'overdose': 1.0,
            'poison myself': 1.0,
            'hang myself': 1.0,
            'slit wrists': 1.0,
            'jump off': 1.0,
            'throw myself': 1.0,
            'crash my car': 1.0,
            'dont want to live': 1.0,
            'hopeless': 0.8,
            'worthless': 0.8,
            'meaningless': 0.8,
            'cant take it anymore': 0.8,
            'cant do this anymore': 0.8,
            'nobody cares': 0.75,
            'everyone would be better off': 0.9,
            'no one loves me': 0.75,
            'alone forever': 0.7,
            'no point': 0.8,
        }
    
    def detect_crisis(self, text, sentiment_score=None):
        """
        Detect crisis indicators from user input
        Returns: (is_crisis: bool, severity: float, keywords_found: list)
        """
        if not text:
            return False, 0, []
        
        text_lower = text.lower()
        found_keywords = []
        max_severity = 0
        
        # Check for crisis keywords
        for keyword, severity in self.crisis_keywords.items():
            if keyword in text_lower:
                found_keywords.append((keyword, severity))
                max_severity = max(max_severity, severity)
                logger.warning(f"CRISIS KEYWORD FOUND: '{keyword}' (severity: {severity})")
        
        # Boost severity if very negative sentiment
        if sentiment_score is not None and sentiment_score < -0.7 and found_keywords:
            max_severity = min(1.0, max_severity + 0.1)
        
        # Determine if crisis
        is_crisis = max_severity >= self.crisis_threshold
        
        return is_crisis, max_severity, found_keywords
    
    def format_crisis_response(self, severity_level, keywords_found=None):
        """Format crisis response with emergency resources"""
        
        if severity_level >= 0.95:
            urgency = "IMMEDIATE CRISIS - EMERGENCY SUPPORT NEEDED"
            color = "🔴"
        elif severity_level >= 0.85:
            urgency = "URGENT CRISIS - IMMEDIATE SUPPORT RECOMMENDED"
            color = "🟠"
        else:
            urgency = "CRISIS SUPPORT AVAILABLE"
            color = "🟡"
        
        response = f"""{color} {urgency}

I hear you. What you're feeling is real and important. You don't have to face this alone.

IMMEDIATE HELP AVAILABLE - REACH OUT NOW:

📞 National Suicide Prevention Lifeline: 988
   Available 24/7 • Free & Confidential
   
💬 Crisis Text Line: Text "HELLO" to 741741
   Text-based support available 24/7
   
🏥 Emergency Services: 911
   If in immediate danger, call 911 or go to nearest ER
   
🌐 International Crisis Lines:
   • UK: 116 123 (Samaritans)
   • Australia: 1300 659 467 (Lifeline)
   • Canada: 1-833-456-4566

Your life has value. These feelings are temporary. Professional support works.
I'm here to listen. Please reach out to one of these resources.
"""
        
        return response
    
    def get_crisis_response(self, text, sentiment_score=None):
        """
        Main method to get formatted crisis response if crisis detected
        Returns: (is_crisis: bool, formatted_response: str or None)
        """
        is_crisis, severity, keywords = self.detect_crisis(text, sentiment_score)
        
        if is_crisis:
            formatted_response = self.format_crisis_response(severity, keywords)
            return True, formatted_response
        
        return False, None
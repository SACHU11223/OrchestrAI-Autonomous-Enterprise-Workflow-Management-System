"""
OrchestrAI - Sentiment Analysis Agent
Analyzes employee mood and sentiment from feedback text.
"""
import json
import re
from core.hf_models import hf_client
from agents.base_agent import BaseAgent


class SentimentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Sentiment Analysis Agent",
            system_instruction="""You are a Sentiment Analysis Agent specialized in workplace communication.
            Analyze employee feedback to determine sentiment, mood indicators, and potential concerns.
            Consider both explicit statements and implicit emotional cues."""
        )

    async def analyze(self, text: str, employee_name: str = "") -> dict:
        """Analyze sentiment of employee feedback."""
        hf_result = hf_client.analyze_sentiment(text)
        hf_context = ""
        if hf_result:
            hf_context = f"\n[HuggingFace ML Output]: The NLP model predicts this is {hf_result['sentiment'].upper()} sentiment with {hf_result['score']} confidence. Please incorporate this core sentiment into your analysis unless fundamentally incorrect."

        prompt = f"""Analyze the sentiment of this employee feedback:

EMPLOYEE: {employee_name or 'Unknown'}
FEEDBACK: {text}{hf_context}

Return JSON with:
- "sentiment": "positive" | "neutral" | "negative"
- "score": float 0-1 (0=very negative, 1=very positive)
- "confidence": float 0-1
- "mood_indicators": ["indicator1", "indicator2"]
- "concerns": ["concern1"] or empty array
- "highlights": ["positive thing1"] or empty array
- "recommendation": string (brief recommendation for manager)"""

        # Wait for the AI output
        result = await self._call_gemini_json(prompt)
        
        # Enforce HF values if present
        if result and "sentiment" in result:
            if hf_result:
                result["hf_enhanced"] = True
            return result

        return self._demo_sentiment(text)

    def _demo_sentiment(self, text: str) -> dict:
        """Analyze sentiment using keyword matching for demo mode."""
        text_lower = text.lower()

        positive_words = ["great", "good", "excellent", "amazing", "confident", "happy", "progress",
                         "completed", "ahead", "smooth", "wonderful", "love", "excited", "fantastic",
                         "well", "succeed", "improved", "productive"]
        negative_words = ["struggling", "frustrated", "difficult", "delayed", "problem", "issue",
                         "overwhelmed", "stuck", "failing", "behind", "stress", "worried", "concern",
                         "frustrated", "hard", "slow", "bad", "terrible"]
        neutral_words = ["okay", "fine", "working", "normal", "continuing", "proceeding", "expected"]

        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        neu_count = sum(1 for w in neutral_words if w in text_lower)

        total = pos_count + neg_count + neu_count + 1
        score = (pos_count - neg_count + total) / (2 * total)
        score = max(0.0, min(1.0, score))

        if pos_count > neg_count * 1.5:
            sentiment = "positive"
        elif neg_count > pos_count * 1.5:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        concerns = []
        if neg_count > 0:
            if "delay" in text_lower or "behind" in text_lower:
                concerns.append("Potential timeline delays")
            if "stress" in text_lower or "overwhelmed" in text_lower:
                concerns.append("Employee may be experiencing burnout")
            if "frustrated" in text_lower or "struggling" in text_lower:
                concerns.append("Technical challenges causing frustration")
            if not concerns:
                concerns.append("Some negative indicators detected")

        highlights = []
        if pos_count > 0:
            if "completed" in text_lower or "ahead" in text_lower:
                highlights.append("Task progress ahead of schedule")
            if "confident" in text_lower or "good" in text_lower:
                highlights.append("Employee morale is high")
            if "progress" in text_lower or "improved" in text_lower:
                highlights.append("Positive momentum on deliverables")
            if not highlights:
                highlights.append("Generally positive outlook")

        recommendations = {
            "positive": "Continue supporting the current work pattern. Consider recognizing the employee's contributions.",
            "neutral": "Schedule a brief check-in to understand any underlying concerns. Provide clarity on priorities.",
            "negative": "Immediate check-in recommended. Consider workload adjustment or additional support resources."
        }

        return {
            "sentiment": sentiment,
            "score": round(score, 2),
            "confidence": 0.78,
            "mood_indicators": [sentiment, "engaged" if pos_count > 0 else "concerned"],
            "concerns": concerns,
            "highlights": highlights,
            "recommendation": recommendations[sentiment]
        }

    def _fallback_response(self, prompt: str) -> str:
        return json.dumps(self._demo_sentiment(prompt))

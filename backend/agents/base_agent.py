"""
OrchestrAI - Base Agent
Base class for all AI agents with Gemini API integration.
"""
import json
import os
from typing import Optional
from core.config import get_settings

settings = get_settings()

# Try importing Gemini
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False


class BaseAgent:
    """Base class for all AI agents."""

    def __init__(self, agent_name: str, system_instruction: str = ""):
        self.agent_name = agent_name
        self.system_instruction = system_instruction
        self.model = None

        if HAS_GEMINI and settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                system_instruction=system_instruction or f"You are {agent_name}, an AI agent in the OrchestrAI enterprise workflow system."
            )

    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API with the given prompt."""
        if self.model:
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"[{self.agent_name}] Gemini API error: {e}")
                return self._fallback_response(prompt)
        return self._fallback_response(prompt)

    async def _call_gemini_json(self, prompt: str) -> dict:
        """Call Gemini API and parse JSON response."""
        raw = await self._call_gemini(prompt + "\n\nRespond ONLY with valid JSON. No markdown formatting.")
        try:
            # Clean response - remove markdown code blocks if present
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                cleaned = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])
            return json.loads(cleaned)
        except json.JSONDecodeError:
            try:
                # Try to find JSON in the response
                start = raw.find("{")
                end = raw.rfind("}") + 1
                if start >= 0 and end > start:
                    return json.loads(raw[start:end])
                start = raw.find("[")
                end = raw.rfind("]") + 1
                if start >= 0 and end > start:
                    return json.loads(raw[start:end])
            except:
                pass
            return {}

    def _fallback_response(self, prompt: str) -> str:
        """Override in subclasses for demo/fallback responses."""
        return '{"status": "demo_mode", "message": "AI response simulated"}'

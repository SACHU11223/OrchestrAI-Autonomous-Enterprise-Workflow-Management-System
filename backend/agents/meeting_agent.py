"""
OrchestrAI - Meeting Agent
Summarizes meeting transcripts into clear, actionable summaries.
"""
from agents.base_agent import BaseAgent


class MeetingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="Meeting Agent",
            system_instruction="""You are a Meeting Summarization Agent. Your job is to analyze meeting transcripts
            and produce clear, concise summaries that capture:
            1. Key discussion points
            2. Decisions made
            3. Action items identified
            4. Blockers or concerns raised
            5. Next steps
            Keep summaries professional and under 300 words."""
        )

    async def summarize(self, transcript: str) -> str:
        """Summarize a meeting transcript."""
        prompt = f"""Analyze this meeting transcript and provide a structured summary:

TRANSCRIPT:
{transcript}

Provide the summary in this format:
## Meeting Summary
### Key Discussion Points
- point 1
- point 2
### Decisions Made
- decision 1
### Action Items
- action 1 (assigned to: person)
### Blockers/Concerns
- blocker 1
### Next Steps
- step 1"""

        result = await self._call_gemini(prompt)
        return result if result and "demo_mode" not in result else self._generate_demo_summary(transcript)

    def _generate_demo_summary(self, transcript: str) -> str:
        """Generate a demo summary when Gemini is unavailable."""
        words = transcript.split()
        word_count = len(words)

        # Extract names (words before colons)
        participants = []
        for i, word in enumerate(words):
            if i + 1 < len(words) and words[i + 1] == ":" if i + 1 < len(words) else False:
                name = word.rstrip(":.,;")
                if name and name[0].isupper() and len(name) > 2:
                    participants.append(name)
        participants = list(set(participants))[:5]

        return f"""## Meeting Summary

### Key Discussion Points
- Team discussed current project progress and status updates
- Technical challenges and implementation approaches were reviewed
- Resource allocation and timeline adjustments were addressed

### Decisions Made
- Priorities established for the next sprint cycle
- Resource reallocation approved for critical path items

### Action Items
- Team members to continue current tasks with updated priorities
- Technical blockers to be resolved within the next 48 hours
- Follow-up meeting scheduled for progress review

### Blockers/Concerns
- Some tasks require additional resources or documentation
- Timeline pressure on critical deliverables identified

### Next Steps
- Continue development on priority items
- Daily standups to track progress on blockers
- Manager to review and reallocate resources as needed

*Participants: {', '.join(participants) if participants else 'Team members'}*
*Transcript length: {word_count} words*"""

    def _fallback_response(self, prompt: str) -> str:
        return self._generate_demo_summary(prompt)

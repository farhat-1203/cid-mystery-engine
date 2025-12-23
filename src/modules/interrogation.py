"""
AI-Powered Interrogation Module
Integrates with LLM APIs for dynamic suspect dialogue
"""

import json
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class StressLevel(Enum):
    CALM = 1
    NERVOUS = 2
    AGITATED = 3
    BREAKING = 4
    CONFESSING = 5

@dataclass
class Evidence:
    id: str
    description: str
    strength: float  # 0.0 to 1.0
    revealed: bool = False

@dataclass
class SuspectProfile:
    name: str
    age: int
    occupation: str
    background: str
    personality_traits: List[str]
    guilty: bool
    alibi: str
    secrets: List[str]
    stress_triggers: List[str]

class InterrogationEngine:
    def __init__(self, api_type: str = "ollama", api_key: Optional[str] = None):
        self.api_type = api_type
        self.api_key = api_key
        self.conversation_history = []
        self.current_suspect = None
        self.stress_meter = 0.0  # 0.0 to 100.0
        self.evidence_presented = []
        
        # Interrogation team members and their specialties
        self.team_approaches = {
            "ACP": "logical and authoritative questioning",
            "DAYA": "intimidating and aggressive approach", 
            "ABHIJEET": "observational and analytical questioning",
            "SALUNKHE": "scientific and methodical approach"
        }
    
    def start_interrogation(self, suspect: SuspectProfile, available_evidence: List[Evidence]):
        """Initialize a new interrogation session"""
        self.current_suspect = suspect
        self.available_evidence = available_evidence
        self.conversation_history = []
        self.stress_meter = 10.0  # Start with slight nervousness
        self.evidence_presented = []
        
        # Generate initial suspect response
        initial_prompt = self._build_system_prompt()
        opening_statement = "I don't know why I'm here. I haven't done anything wrong."
        
        self.conversation_history.append({
            "role": "suspect",
            "content": opening_statement,
            "stress_level": self.stress_meter
        })
        
        return opening_statement
    
    def ask_question(self, question: str, team_member: str = "ACP", evidence_id: Optional[str] = None) -> Dict:
        """
        Ask a question to the suspect
        Returns: {
            'response': str,
            'stress_change': float,
            'new_stress_level': float,
            'behavioral_notes': List[str],
            'breakthrough': bool
        }
        """
        if not self.current_suspect:
            return {"error": "No active interrogation session"}
        
        # Handle evidence presentation
        stress_modifier = 0.0
        if evidence_id:
            stress_modifier = self._present_evidence(evidence_id)
        
        # Build the prompt for the LLM
        prompt = self._build_interrogation_prompt(question, team_member, evidence_id)
        
        # Get AI response
        ai_response = self._get_ai_response(prompt)
        
        # Update stress meter
        question_stress = self._calculate_stress_impact(question, team_member, evidence_id)
        self.stress_meter = min(100.0, self.stress_meter + question_stress + stress_modifier)
        
        # Analyze behavioral changes
        behavioral_notes = self._analyze_behavior_change(question_stress + stress_modifier)
        
        # Check for breakthrough moments
        breakthrough = self._check_breakthrough()
        
        # Update conversation history
        self.conversation_history.append({
            "role": "investigator",
            "content": question,
            "team_member": team_member,
            "evidence_used": evidence_id
        })
        
        self.conversation_history.append({
            "role": "suspect",
            "content": ai_response,
            "stress_level": self.stress_meter
        })
        
        return {
            "response": ai_response,
            "stress_change": question_stress + stress_modifier,
            "new_stress_level": self.stress_meter,
            "behavioral_notes": behavioral_notes,
            "breakthrough": breakthrough
        }
    
    def _present_evidence(self, evidence_id: str) -> float:
        """Present evidence and calculate stress impact"""
        evidence = next((e for e in self.available_evidence if e.id == evidence_id), None)
        if not evidence or evidence_id in self.evidence_presented:
            return 0.0
        
        self.evidence_presented.append(evidence_id)
        evidence.revealed = True
        
        # Calculate stress based on evidence strength and suspect's guilt
        base_stress = evidence.strength * 15.0
        
        # Guilty suspects are more affected by strong evidence
        if self.current_suspect.guilty:
            base_stress *= 1.5
        
        # Check if evidence contradicts suspect's previous statements
        contradiction_bonus = self._check_contradiction(evidence)
        
        return base_stress + contradiction_bonus
    
    def _calculate_stress_impact(self, question: str, team_member: str, evidence_id: Optional[str]) -> float:
        """Calculate how much stress a question/approach adds"""
        base_stress = 2.0
        
        # Team member approach modifiers
        approach_modifiers = {
            "ACP": 1.0,      # Balanced approach
            "DAYA": 2.5,     # High intimidation
            "ABHIJEET": 0.8, # Gentle but persistent
            "SALUNKHE": 1.2  # Scientific, methodical
        }
        
        stress = base_stress * approach_modifiers.get(team_member, 1.0)
        
        # Check for stress triggers in the question
        for trigger in self.current_suspect.stress_triggers:
            if trigger.lower() in question.lower():
                stress += 8.0
        
        # Aggressive questioning detection
        aggressive_words = ["lie", "lying", "liar", "guilty", "did it", "confess", "admit"]
        if any(word in question.lower() for word in aggressive_words):
            stress += 5.0
        
        return stress
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the LLM"""
        return f"""You are roleplaying as {self.current_suspect.name}, a {self.current_suspect.age}-year-old {self.current_suspect.occupation}.

BACKGROUND: {self.current_suspect.background}
PERSONALITY: {', '.join(self.current_suspect.personality_traits)}
ALIBI: {self.current_suspect.alibi}

IMPORTANT ROLEPLAY RULES:
- You are {'GUILTY' if self.current_suspect.guilty else 'INNOCENT'} of the crime
- Current stress level: {self.stress_meter}/100
- Secrets you're hiding: {', '.join(self.current_suspect.secrets)}
- Stay in character at all times
- Respond naturally as this person would
- Show stress through speech patterns, hesitation, contradictions
- If stress is high (>70), become more defensive, make mistakes, or start breaking down
- If stress is very high (>90), consider confessing or revealing secrets
- Never break character or mention you're an AI"""
    
    def _build_interrogation_prompt(self, question: str, team_member: str, evidence_id: Optional[str]) -> str:
        """Build the specific interrogation prompt"""
        approach_style = self.team_approaches.get(team_member, "standard questioning")
        
        evidence_context = ""
        if evidence_id:
            evidence = next((e for e in self.available_evidence if e.id == evidence_id), None)
            if evidence:
                evidence_context = f"\n\nEVIDENCE PRESENTED: {evidence.description}"
        
        conversation_context = ""
        if len(self.conversation_history) > 1:
            recent_history = self.conversation_history[-4:]  # Last 2 exchanges
            conversation_context = "\n\nRECENT CONVERSATION:\n"
            for entry in recent_history:
                role = "INVESTIGATOR" if entry["role"] == "investigator" else "YOU"
                conversation_context += f"{role}: {entry['content']}\n"
        
        return f"""INTERROGATION CONTEXT:
{team_member} is using {approach_style} to ask you this question.
Current stress level: {self.stress_meter}/100

QUESTION: {question}{evidence_context}{conversation_context}

Respond as {self.current_suspect.name} would, showing appropriate stress level through your speech."""
    
    def _get_ai_response(self, prompt: str) -> str:
        """Get response from AI service"""
        try:
            if self.api_type == "ollama":
                return self._query_ollama(prompt)
            elif self.api_type == "gemini":
                return self._query_gemini(prompt)
            else:
                return self._fallback_response()
        except Exception as e:
            print(f"AI API Error: {e}")
            return self._fallback_response()
    
    def _query_ollama(self, prompt: str) -> str:
        """Query Ollama local LLM"""
        url = "http://localhost:11434/api/generate"
        data = {
            "model": "llama2",  # or another model you have installed
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json().get("response", self._fallback_response())
        else:
            return self._fallback_response()
    
    def _query_gemini(self, prompt: str) -> str:
        """Query Google Gemini API"""
        if not self.api_key:
            return self._fallback_response()
        
        # Implement Gemini API call here
        # This would require the google-generativeai library
        return self._fallback_response()
    
    def _fallback_response(self) -> str:
        """Fallback response when AI is unavailable"""
        stress_level = StressLevel.CALM
        if self.stress_meter > 80:
            stress_level = StressLevel.BREAKING
        elif self.stress_meter > 60:
            stress_level = StressLevel.AGITATED
        elif self.stress_meter > 30:
            stress_level = StressLevel.NERVOUS
        
        responses = {
            StressLevel.CALM: [
                "I already told you, I don't know anything about this.",
                "I was at home that night, like I said.",
                "Why are you asking me these questions?"
            ],
            StressLevel.NERVOUS: [
                "I... I don't remember exactly...",
                "Look, I might have been there, but I didn't do anything!",
                "You're making me nervous with all these questions."
            ],
            StressLevel.AGITATED: [
                "This is harassment! I want a lawyer!",
                "I don't have to listen to this!",
                "You're trying to pin this on me, aren't you?"
            ],
            StressLevel.BREAKING: [
                "Okay, okay! Maybe I was there, but...",
                "I didn't mean for it to happen!",
                "You don't understand the pressure I was under!"
            ]
        }
        
        import random
        return random.choice(responses[stress_level])
    
    def _analyze_behavior_change(self, stress_change: float) -> List[str]:
        """Analyze behavioral changes based on stress"""
        notes = []
        
        if stress_change > 15:
            notes.append("Suspect shows visible signs of distress")
        if stress_change > 25:
            notes.append("Suspect's voice is shaking")
        if self.stress_meter > 70:
            notes.append("Suspect is sweating profusely")
        if self.stress_meter > 85:
            notes.append("Suspect appears to be on the verge of breaking")
        
        return notes
    
    def _check_breakthrough(self) -> bool:
        """Check if we've reached a breakthrough moment"""
        return self.stress_meter > 90 and self.current_suspect.guilty
    
    def _check_contradiction(self, evidence: Evidence) -> float:
        """Check if evidence contradicts previous statements"""
        # Simple implementation - in a real game, this would be more sophisticated
        if len(self.conversation_history) > 2:
            return 10.0  # Bonus stress for contradictory evidence
        return 0.0
    
    def get_interrogation_summary(self) -> Dict:
        """Get a summary of the interrogation session"""
        return {
            "suspect": self.current_suspect.name,
            "final_stress_level": self.stress_meter,
            "evidence_presented": len(self.evidence_presented),
            "total_questions": len([h for h in self.conversation_history if h["role"] == "investigator"]),
            "breakthrough_achieved": self._check_breakthrough(),
            "confession_likelihood": min(100, self.stress_meter) if self.current_suspect.guilty else 0
        }
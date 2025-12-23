"""
Interrogation Room State - AI-powered suspect questioning
"""

import pygame
from src.states.base_state import BaseState
from src.engine.config import Config
from src.modules.interrogation import InterrogationEngine, SuspectProfile, Evidence

class InterrogationState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.interrogation_engine = InterrogationEngine()
        self.current_suspect = None
        self.conversation_display = []
        self.input_text = ""
        self.selected_team_member = "ACP"
        self.team_members = ["ACP", "DAYA", "ABHIJEET", "SALUNKHE"]
        self.team_index = 0
        
        # Sample suspect for demo
        self.setup_demo_suspect()
    
    def setup_demo_suspect(self):
        """Setup a demo suspect for testing"""
        self.current_suspect = SuspectProfile(
            name="Rajesh Kumar",
            age=35,
            occupation="Office Manager",
            background="Works at the victim's company, recently passed over for promotion",
            personality_traits=["nervous", "defensive", "ambitious"],
            guilty=True,
            alibi="I was at home watching TV",
            secrets=["Had argument with victim", "Needed money badly"],
            stress_triggers=["promotion", "money", "argument", "victim's name"]
        )
        
        # Sample evidence
        evidence = [
            Evidence("fingerprint", "Fingerprints found on victim's desk", 0.8),
            Evidence("witness", "Witness saw suspect near office", 0.6),
            Evidence("motive", "Financial records show suspect's debt", 0.9)
        ]
        
        # Start interrogation
        opening = self.interrogation_engine.start_interrogation(self.current_suspect, evidence)
        self.conversation_display.append(f"SUSPECT: {opening}")
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(Config.STATE_BUREAU)
            elif event.key == pygame.K_TAB:
                # Switch team member
                self.team_index = (self.team_index + 1) % len(self.team_members)
                self.selected_team_member = self.team_members[self.team_index]
            elif event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    self._ask_question()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_1:
                self._present_evidence("fingerprint")
            elif event.key == pygame.K_2:
                self._present_evidence("witness")
            elif event.key == pygame.K_3:
                self._present_evidence("motive")
            else:
                # Add character to input
                if event.unicode.isprintable() and len(self.input_text) < 100:
                    self.input_text += event.unicode
    
    def _ask_question(self):
        """Ask the current question"""
        question = self.input_text.strip()
        if not question:
            return
        
        # Add question to display
        team_name = Config.TEAM_MEMBERS[self.selected_team_member]["name"]
        self.conversation_display.append(f"{team_name}: {question}")
        
        # Get AI response
        result = self.interrogation_engine.ask_question(
            question, 
            self.selected_team_member
        )
        
        if "response" in result:
            self.conversation_display.append(f"SUSPECT: {result['response']}")
            
            # Add behavioral notes
            if result["behavioral_notes"]:
                for note in result["behavioral_notes"]:
                    self.conversation_display.append(f"[OBSERVATION: {note}]")
            
            # Check for breakthrough
            if result["breakthrough"]:
                self.conversation_display.append("[BREAKTHROUGH MOMENT!]")
        
        # Clear input
        self.input_text = ""
        
        # Limit conversation display
        if len(self.conversation_display) > 15:
            self.conversation_display = self.conversation_display[-15:]
    
    def _present_evidence(self, evidence_id):
        """Present evidence during questioning"""
        if self.input_text.strip():
            result = self.interrogation_engine.ask_question(
                self.input_text.strip(),
                self.selected_team_member,
                evidence_id
            )
            
            team_name = Config.TEAM_MEMBERS[self.selected_team_member]["name"]
            self.conversation_display.append(f"{team_name}: {self.input_text} [PRESENTS EVIDENCE]")
            
            if "response" in result:
                self.conversation_display.append(f"SUSPECT: {result['response']}")
            
            self.input_text = ""
    
    def render(self, screen):
        # Background
        screen.fill((30, 30, 30))  # Dark interrogation room
        
        # Title
        title_text = self.title_font.render("Interrogation Room", True, Config.EVIDENCE_YELLOW)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 30))
        screen.blit(title_text, title_rect)
        
        # Suspect info
        if self.current_suspect:
            suspect_info = f"{self.current_suspect.name} - {self.current_suspect.occupation}"
            suspect_text = self.font.render(suspect_info, True, Config.WHITE)
            screen.blit(suspect_text, (50, 70))
        
        # Stress meter
        stress_level = self.interrogation_engine.stress_meter
        stress_width = 300
        stress_height = 20
        stress_x = Config.SCREEN_WIDTH - stress_width - 50
        stress_y = 70
        
        # Stress meter background
        pygame.draw.rect(screen, Config.CID_GRAY, (stress_x, stress_y, stress_width, stress_height))
        
        # Stress meter fill
        stress_fill = int(stress_width * (stress_level / 100))
        stress_color = Config.DANGER_RED if stress_level > 70 else Config.EVIDENCE_YELLOW
        pygame.draw.rect(screen, stress_color, (stress_x, stress_y, stress_fill, stress_height))
        
        # Stress meter label
        stress_text = self.font.render(f"Stress: {stress_level:.0f}%", True, Config.WHITE)
        screen.blit(stress_text, (stress_x, stress_y + 25))
        
        # Team member selection
        team_y = 110
        team_text = self.font.render(f"Active: {Config.TEAM_MEMBERS[self.selected_team_member]['name']}", True, Config.EVIDENCE_YELLOW)
        screen.blit(team_text, (50, team_y))
        
        specialty = Config.TEAM_MEMBERS[self.selected_team_member]['specialty']
        specialty_text = self.font.render(f"Specialty: {specialty}", True, Config.CID_GRAY)
        screen.blit(specialty_text, (50, team_y + 25))
        
        # Conversation display
        conv_y = 170
        conv_height = 300
        
        # Conversation background
        pygame.draw.rect(screen, (20, 20, 20), (50, conv_y, Config.SCREEN_WIDTH - 100, conv_height))
        pygame.draw.rect(screen, Config.CID_GRAY, (50, conv_y, Config.SCREEN_WIDTH - 100, conv_height), 2)
        
        # Display conversation
        line_height = 20
        start_line = max(0, len(self.conversation_display) - (conv_height // line_height))
        
        for i, line in enumerate(self.conversation_display[start_line:]):
            y_pos = conv_y + 10 + i * line_height
            
            if line.startswith("SUSPECT:"):
                color = Config.WHITE
            elif line.startswith("["):
                color = Config.EVIDENCE_YELLOW
            else:
                color = Config.CID_GRAY
            
            # Wrap long lines
            if len(line) > 80:
                line = line[:77] + "..."
            
            line_text = self.font.render(line, True, color)
            screen.blit(line_text, (60, y_pos))
        
        # Input area
        input_y = conv_y + conv_height + 20
        input_label = self.font.render("Your Question:", True, Config.WHITE)
        screen.blit(input_label, (50, input_y))
        
        # Input box
        input_box_y = input_y + 30
        pygame.draw.rect(screen, Config.WHITE, (50, input_box_y, Config.SCREEN_WIDTH - 100, 30))
        pygame.draw.rect(screen, Config.BLACK, (52, input_box_y + 2, Config.SCREEN_WIDTH - 104, 26))
        
        # Input text
        input_display = self.input_text + "|"  # Cursor
        input_text_surface = self.font.render(input_display, True, Config.WHITE)
        screen.blit(input_text_surface, (60, input_box_y + 5))
        
        # Evidence shortcuts
        evidence_y = input_box_y + 50
        evidence_title = self.font.render("Evidence (Press number key):", True, Config.WHITE)
        screen.blit(evidence_title, (50, evidence_y))
        
        evidence_list = [
            "1. Fingerprint Evidence",
            "2. Witness Testimony", 
            "3. Financial Motive"
        ]
        
        for i, evidence in enumerate(evidence_list):
            evidence_text = self.font.render(evidence, True, Config.EVIDENCE_YELLOW)
            screen.blit(evidence_text, (70, evidence_y + 30 + i * 25))
        
        # Instructions
        instructions = [
            "Tab: Switch Team Member | Enter: Ask Question | 1-3: Present Evidence | Escape: Back"
        ]
        
        for i, instruction in enumerate(instructions):
            instruction_text = self.font.render(instruction, True, Config.CID_GRAY)
            screen.blit(instruction_text, (50, Config.SCREEN_HEIGHT - 30 + i * 20))
"""
Team Briefing State - Coordinate with team members and get updates
"""

import pygame
from src.states.base_state import BaseState
from src.engine.config import Config

class TeamBriefingState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.selected_member = 0
        self.team_members = ["ACP", "DAYA", "ABHIJEET", "SALUNKHE"]
        
        # Team member briefings and current status
        self.briefings = {
            "ACP": {
                "status": "Coordinating Investigation",
                "current_task": "Reviewing case evidence and planning next steps",
                "briefing": [
                    "Team, we have a complex case on our hands.",
                    "The victim was found in his locked office with signs of struggle.",
                    "We need to examine all evidence carefully and question suspects thoroughly.",
                    "Daya, I want you to check the building security.",
                    "Abhijeet, review the victim's recent activities.",
                    "Dr. Salunkhe, prioritize the forensic analysis.",
                    "Remember: Every detail matters in solving this case."
                ],
                "availability": "Available for consultation"
            },
            "DAYA": {
                "status": "Security Investigation",
                "current_task": "Checking building security and interviewing guards",
                "briefing": [
                    "Boss, I've been investigating the building security.",
                    "The main entrance has CCTV but the back exit camera was broken.",
                    "Security guard mentions seeing someone suspicious around 9 PM.",
                    "I found signs of forced entry at the emergency exit.",
                    "The suspect might have used the service elevator to avoid detection.",
                    "I'm ready to bring in suspects for questioning.",
                    "Just give me the word, and I'll make them talk!"
                ],
                "availability": "Ready for field work"
            },
            "ABHIJEET": {
                "status": "Evidence Analysis",
                "current_task": "Analyzing victim's background and recent activities",
                "briefing": [
                    "I've been studying the victim's profile and recent behavior.",
                    "Mr. Sharma had been receiving threatening calls last week.",
                    "His secretary mentioned he was worried about something.",
                    "Bank records show unusual transactions in his account.",
                    "He had meetings with three different people on the day he died.",
                    "I've prepared detailed profiles of all potential suspects.",
                    "The pattern suggests this wasn't a random crime."
                ],
                "availability": "Analyzing evidence"
            },
            "SALUNKHE": {
                "status": "Forensic Analysis",
                "current_task": "Processing physical evidence from crime scene",
                "briefing": [
                    "The forensic analysis reveals several important findings.",
                    "Time of death was between 8:30 and 9:30 PM yesterday.",
                    "The victim was struck with a blunt object, likely a paperweight.",
                    "I found three different sets of fingerprints on the desk.",
                    "Blood spatter analysis suggests the attacker was right-handed.",
                    "DNA analysis is still in progress, results expected soon.",
                    "The evidence clearly indicates this was a planned attack."
                ],
                "availability": "In laboratory"
            }
        }
        
        self.case_updates = [
            "New witness came forward with information",
            "Forensic analysis of fingerprints completed", 
            "Suspect's alibi has been verified as false",
            "Additional evidence found at secondary location"
        ]
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_member = (self.selected_member - 1) % len(self.team_members)
            elif event.key == pygame.K_RIGHT:
                self.selected_member = (self.selected_member + 1) % len(self.team_members)
            elif event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(Config.STATE_BUREAU)
    
    def render(self, screen):
        # Background
        screen.fill(Config.CID_BLUE)
        
        # Title
        title_text = self.title_font.render("Team Briefing - Case Status Update", True, Config.EVIDENCE_YELLOW)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 40))
        screen.blit(title_text, title_rect)
        
        # Team member tabs
        tab_width = Config.SCREEN_WIDTH // len(self.team_members)
        tab_height = 50
        tab_y = 90
        
        for i, member in enumerate(self.team_members):
            tab_x = i * tab_width
            
            # Tab background
            if i == self.selected_member:
                tab_color = Config.EVIDENCE_YELLOW
                text_color = Config.BLACK
            else:
                tab_color = Config.CID_GRAY
                text_color = Config.WHITE
            
            pygame.draw.rect(screen, tab_color, (tab_x, tab_y, tab_width, tab_height))
            pygame.draw.rect(screen, Config.WHITE, (tab_x, tab_y, tab_width, tab_height), 2)
            
            # Tab text
            member_info = Config.TEAM_MEMBERS[member]
            tab_text = self.font.render(member_info["name"], True, text_color)
            tab_rect = tab_text.get_rect(center=(tab_x + tab_width // 2, tab_y + tab_height // 2))
            screen.blit(tab_text, tab_rect)
        
        # Selected member briefing
        selected_member_key = self.team_members[self.selected_member]
        member_info = Config.TEAM_MEMBERS[selected_member_key]
        briefing_data = self.briefings[selected_member_key]
        
        # Member details panel
        panel_y = tab_y + tab_height + 20
        panel_height = 400
        
        # Panel background
        pygame.draw.rect(screen, (20, 20, 40), (50, panel_y, Config.SCREEN_WIDTH - 100, panel_height))
        pygame.draw.rect(screen, Config.EVIDENCE_YELLOW, (50, panel_y, Config.SCREEN_WIDTH - 100, panel_height), 2)
        
        # Member name and specialty
        name_text = self.title_font.render(member_info["name"], True, Config.EVIDENCE_YELLOW)
        screen.blit(name_text, (70, panel_y + 20))
        
        specialty_text = self.font.render(f"Specialty: {member_info['specialty']}", True, Config.WHITE)
        screen.blit(specialty_text, (70, panel_y + 60))
        
        # Current status
        status_text = self.font.render(f"Status: {briefing_data['status']}", True, Config.EVIDENCE_YELLOW)
        screen.blit(status_text, (70, panel_y + 90))
        
        task_text = self.font.render(f"Current Task: {briefing_data['current_task']}", True, Config.WHITE)
        screen.blit(task_text, (70, panel_y + 115))
        
        availability_text = self.font.render(f"Availability: {briefing_data['availability']}", True, Config.CID_GRAY)
        screen.blit(availability_text, (70, panel_y + 140))
        
        # Briefing content
        briefing_title = self.font.render("Briefing:", True, Config.EVIDENCE_YELLOW)
        screen.blit(briefing_title, (70, panel_y + 180))
        
        for i, line in enumerate(briefing_data["briefing"]):
            # Wrap long lines
            if len(line) > 80:
                words = line.split()
                wrapped_lines = []
                current_line = ""
                
                for word in words:
                    if len(current_line + word) < 80:
                        current_line += word + " "
                    else:
                        wrapped_lines.append(current_line.strip())
                        current_line = word + " "
                
                if current_line:
                    wrapped_lines.append(current_line.strip())
                
                for j, wrapped_line in enumerate(wrapped_lines):
                    line_text = self.font.render(f"• {wrapped_line}" if j == 0 else f"  {wrapped_line}", True, Config.WHITE)
                    screen.blit(line_text, (90, panel_y + 210 + (i * len(wrapped_lines) + j) * 25))
            else:
                line_text = self.font.render(f"• {line}", True, Config.WHITE)
                screen.blit(line_text, (90, panel_y + 210 + i * 25))
        
        # Case updates sidebar
        updates_x = Config.SCREEN_WIDTH - 300
        updates_y = panel_y
        updates_width = 250
        
        # Updates background
        pygame.draw.rect(screen, (40, 20, 20), (updates_x, updates_y, updates_width, 200))
        pygame.draw.rect(screen, Config.DANGER_RED, (updates_x, updates_y, updates_width, 200), 2)
        
        updates_title = self.font.render("Recent Updates:", True, Config.DANGER_RED)
        screen.blit(updates_title, (updates_x + 10, updates_y + 10))
        
        for i, update in enumerate(self.case_updates):
            # Wrap update text
            words = update.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line + word) < 30:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line.strip())
            
            for j, line in enumerate(lines):
                update_text = self.font.render(f"• {line}" if j == 0 else f"  {line}", True, Config.WHITE)
                screen.blit(update_text, (updates_x + 15, updates_y + 40 + (i * len(lines) + j) * 20))
        
        # Instructions
        instruction_text = self.font.render("Left/Right Arrow: Switch Team Members | Escape: Back to Bureau", True, Config.CID_GRAY)
        instruction_rect = instruction_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 30))
        screen.blit(instruction_text, instruction_rect)
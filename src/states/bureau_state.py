"""
CID Bureau State - Main hub for case management
"""

import pygame
from src.states.base_state import BaseState
from src.engine.config import Config

class BureauState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.menu_options = [
            ("Crime Scene Investigation", Config.STATE_CRIME_SCENE),
            ("Forensic Lab", Config.STATE_LAB),
            ("Interrogation Room", Config.STATE_INTERROGATION),
            ("Case Files", Config.STATE_CASE_FILES),
            ("Team Briefing", Config.STATE_TEAM_BRIEFING),
            ("Back to Menu", Config.STATE_MENU)
        ]
        self.selected_option = 0
        self.team_status = {
            "ACP": "Available - Ready for leadership",
            "DAYA": "Available - Ready for action", 
            "ABHIJEET": "Available - Analyzing evidence",
            "SALUNKHE": "In Lab - Processing samples"
        }
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self._select_option()
            elif event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(Config.STATE_MENU)
    
    def _select_option(self):
        """Handle menu selection"""
        option_text, action = self.menu_options[self.selected_option]
        
        if action:
            self.state_manager.change_state(action)
    
    def render(self, screen):
        # Background
        screen.fill(Config.CID_BLUE)
        
        # Title
        title_text = self.title_font.render("CID Bureau - Mumbai", True, Config.EVIDENCE_YELLOW)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 80))
        screen.blit(title_text, title_rect)
        
        # Team status panel
        team_y = 150
        team_title = self.font.render("Team Status:", True, Config.WHITE)
        screen.blit(team_title, (50, team_y))
        
        for i, (member, status) in enumerate(self.team_status.items()):
            member_info = Config.TEAM_MEMBERS[member]
            text = f"{member_info['name']}: {status}"
            color = Config.EVIDENCE_YELLOW if "Available" in status else Config.CID_GRAY
            
            member_text = self.font.render(text, True, color)
            screen.blit(member_text, (70, team_y + 40 + i * 30))
        
        # Main menu
        menu_x = Config.SCREEN_WIDTH // 2
        menu_y = 350
        
        menu_title = self.font.render("Select Investigation Area:", True, Config.WHITE)
        menu_title_rect = menu_title.get_rect(center=(menu_x, menu_y))
        screen.blit(menu_title, menu_title_rect)
        
        for i, (option_text, _) in enumerate(self.menu_options):
            color = Config.EVIDENCE_YELLOW if i == self.selected_option else Config.WHITE
            text = self.font.render(f"> {option_text}" if i == self.selected_option else f"  {option_text}", True, color)
            text_rect = text.get_rect(center=(menu_x, menu_y + 50 + i * 40))
            screen.blit(text, text_rect)
        
        # Instructions
        instruction_text = self.font.render("Arrow Keys: Navigate | Enter: Select | Escape: Back", True, Config.CID_GRAY)
        instruction_rect = instruction_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 30))
        screen.blit(instruction_text, instruction_rect)
"""
Main Menu State
"""

import pygame
from src.states.base_state import BaseState
from src.engine.config import Config

class MenuState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.menu_options = [
            ("New Case", Config.STATE_BUREAU),
            ("Load Case", None),
            ("Exit", "exit")
        ]
        self.selected_option = 0
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self._select_option()
    
    def _select_option(self):
        """Handle menu selection"""
        option_text, action = self.menu_options[self.selected_option]
        
        if action == "exit":
            pygame.quit()
            exit()
        elif action:
            self.state_manager.change_state(action)
    
    def render(self, screen):
        # Title
        title_text = self.title_font.render("CID: The Silicon Casefiles", True, Config.EVIDENCE_YELLOW)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font.render("A Detective Simulation Experience", True, Config.WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 200))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options
        for i, (option_text, _) in enumerate(self.menu_options):
            color = Config.EVIDENCE_YELLOW if i == self.selected_option else Config.WHITE
            text = self.font.render(option_text, True, color)
            text_rect = text.get_rect(center=(Config.SCREEN_WIDTH // 2, 350 + i * 60))
            screen.blit(text, text_rect)
        
        # Instructions
        instruction_text = self.font.render("Use Arrow Keys and Enter to navigate", True, Config.CID_GRAY)
        instruction_rect = instruction_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 50))
        screen.blit(instruction_text, instruction_rect)
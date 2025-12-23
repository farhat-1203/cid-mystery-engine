"""
Forensic Lab State - Dr. Salunkhe's domain
"""

import pygame
from src.states.base_state import BaseState
from src.engine.config import Config

class LabState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.analysis_options = [
            "Fingerprint Analysis",
            "DNA Testing", 
            "Ballistics Report",
            "Image Enhancement",
            "Chemical Analysis",
            "Back to Bureau"
        ]
        self.selected_option = 0
        self.analysis_results = {}
        self.current_analysis = None
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.analysis_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.analysis_options)
            elif event.key == pygame.K_RETURN:
                self._select_analysis()
            elif event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(Config.STATE_BUREAU)
    
    def _select_analysis(self):
        """Handle analysis selection"""
        selected = self.analysis_options[self.selected_option]
        
        if selected == "Back to Bureau":
            self.state_manager.change_state(Config.STATE_BUREAU)
        elif selected == "Image Enhancement":
            # This would integrate with the forensics module
            self.current_analysis = "Enhancing security footage..."
            self.analysis_results["image_enhancement"] = {
                "status": "Processing",
                "progress": 0,
                "result": "Face detected with 78% confidence"
            }
        else:
            # Simulate other analyses
            self.current_analysis = f"Running {selected}..."
            self.analysis_results[selected.lower().replace(" ", "_")] = {
                "status": "Processing",
                "progress": 0,
                "result": f"{selected} completed successfully"
            }
    
    def update(self, dt):
        """Update analysis progress"""
        if self.current_analysis:
            # Simulate analysis progress
            for analysis_id, data in self.analysis_results.items():
                if data["status"] == "Processing":
                    data["progress"] += dt * 20  # 20% per second
                    if data["progress"] >= 100:
                        data["status"] = "Complete"
                        data["progress"] = 100
                        if analysis_id == "image_enhancement":
                            self.current_analysis = None
    
    def render(self, screen):
        # Background
        screen.fill((20, 30, 40))  # Lab-like dark blue
        
        # Title
        title_text = self.title_font.render("Forensic Laboratory - Dr. Salunkhe", True, Config.EVIDENCE_YELLOW)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        # Dr. Salunkhe quote
        quote_text = self.font.render('"Science never lies, it only reveals the truth"', True, Config.WHITE)
        quote_rect = quote_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 90))
        screen.blit(quote_text, quote_rect)
        
        # Analysis menu
        menu_x = 100
        menu_y = 150
        
        menu_title = self.font.render("Available Analyses:", True, Config.WHITE)
        screen.blit(menu_title, (menu_x, menu_y))
        
        for i, option in enumerate(self.analysis_options):
            color = Config.EVIDENCE_YELLOW if i == self.selected_option else Config.WHITE
            prefix = "> " if i == self.selected_option else "  "
            text = self.font.render(f"{prefix}{option}", True, color)
            screen.blit(text, (menu_x + 20, menu_y + 40 + i * 35))
        
        # Analysis results panel
        results_x = Config.SCREEN_WIDTH // 2 + 50
        results_y = 150
        
        results_title = self.font.render("Analysis Results:", True, Config.WHITE)
        screen.blit(results_title, (results_x, results_y))
        
        y_offset = 40
        for analysis_id, data in self.analysis_results.items():
            # Analysis name
            name = analysis_id.replace("_", " ").title()
            name_text = self.font.render(name, True, Config.EVIDENCE_YELLOW)
            screen.blit(name_text, (results_x + 20, results_y + y_offset))
            
            # Status and progress
            if data["status"] == "Processing":
                progress_text = f"Progress: {data['progress']:.0f}%"
                color = Config.CID_GRAY
            else:
                progress_text = "Complete ✓"
                color = (0, 255, 0)
            
            status_text = self.font.render(progress_text, True, color)
            screen.blit(status_text, (results_x + 40, results_y + y_offset + 25))
            
            # Result (if complete)
            if data["status"] == "Complete":
                result_text = self.font.render(data["result"], True, Config.WHITE)
                screen.blit(result_text, (results_x + 40, results_y + y_offset + 50))
                y_offset += 75
            else:
                y_offset += 50
            
            y_offset += 20
        
        # Current analysis status
        if self.current_analysis:
            status_text = self.font.render(self.current_analysis, True, Config.EVIDENCE_YELLOW)
            status_rect = status_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 100))
            screen.blit(status_text, status_rect)
        
        # Instructions
        instruction_text = self.font.render("Arrow Keys: Navigate | Enter: Start Analysis | Escape: Back", True, Config.CID_GRAY)
        instruction_rect = instruction_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 30))
        screen.blit(instruction_text, instruction_rect)
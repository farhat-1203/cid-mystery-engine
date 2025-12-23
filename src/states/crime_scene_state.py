"""
Crime Scene Investigation State
"""

import pygame
from src.states.base_state import BaseState
from src.engine.config import Config

class CrimeSceneState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.evidence_found = []
        self.investigation_progress = 0
        self.current_scene = "Office Building - Floor 12"
        
        # Available evidence at the scene
        self.available_evidence = [
            {"id": "fingerprint_1", "name": "Fingerprint on Door", "found": False, "x": 200, "y": 300},
            {"id": "blood_sample", "name": "Blood Sample", "found": False, "x": 400, "y": 250},
            {"id": "security_footage", "name": "Security Camera", "found": False, "x": 600, "y": 150},
            {"id": "witness_statement", "name": "Witness", "found": False, "x": 300, "y": 400}
        ]
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(Config.STATE_BUREAU)
            elif event.key == pygame.K_SPACE:
                self._investigate_nearby_evidence()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._check_evidence_click(event.pos)
    
    def _investigate_nearby_evidence(self):
        """Investigate evidence near the player"""
        # Simple implementation - find first unfound evidence
        for evidence in self.available_evidence:
            if not evidence["found"]:
                evidence["found"] = True
                self.evidence_found.append(evidence)
                self.investigation_progress = len(self.evidence_found) / len(self.available_evidence) * 100
                break
    
    def _check_evidence_click(self, pos):
        """Check if player clicked on evidence"""
        mouse_x, mouse_y = pos
        
        for evidence in self.available_evidence:
            if not evidence["found"]:
                # Check if click is near evidence location
                distance = ((mouse_x - evidence["x"]) ** 2 + (mouse_y - evidence["y"]) ** 2) ** 0.5
                if distance < 50:  # 50 pixel radius
                    evidence["found"] = True
                    self.evidence_found.append(evidence)
                    self.investigation_progress = len(self.evidence_found) / len(self.available_evidence) * 100
                    break
    
    def render(self, screen):
        # Background
        screen.fill((40, 40, 60))  # Dark scene
        
        # Scene title
        title_text = self.title_font.render(f"Crime Scene: {self.current_scene}", True, Config.EVIDENCE_YELLOW)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        # Progress bar
        progress_width = 400
        progress_height = 20
        progress_x = (Config.SCREEN_WIDTH - progress_width) // 2
        progress_y = 100
        
        # Progress background
        pygame.draw.rect(screen, Config.CID_GRAY, (progress_x, progress_y, progress_width, progress_height))
        
        # Progress fill
        fill_width = int(progress_width * (self.investigation_progress / 100))
        pygame.draw.rect(screen, Config.EVIDENCE_YELLOW, (progress_x, progress_y, fill_width, progress_height))
        
        # Progress text
        progress_text = self.font.render(f"Investigation Progress: {self.investigation_progress:.0f}%", True, Config.WHITE)
        progress_text_rect = progress_text.get_rect(center=(Config.SCREEN_WIDTH // 2, progress_y + 35))
        screen.blit(progress_text, progress_text_rect)
        
        # Draw evidence locations
        for evidence in self.available_evidence:
            if evidence["found"]:
                # Found evidence - green circle
                pygame.draw.circle(screen, (0, 255, 0), (evidence["x"], evidence["y"]), 15)
                pygame.draw.circle(screen, Config.WHITE, (evidence["x"], evidence["y"]), 15, 2)
            else:
                # Unfound evidence - yellow circle (investigation point)
                pygame.draw.circle(screen, Config.EVIDENCE_YELLOW, (evidence["x"], evidence["y"]), 10)
                pygame.draw.circle(screen, Config.WHITE, (evidence["x"], evidence["y"]), 10, 2)
        
        # Evidence list
        evidence_y = 200
        evidence_title = self.font.render("Evidence Found:", True, Config.WHITE)
        screen.blit(evidence_title, (50, evidence_y))
        
        for i, evidence in enumerate(self.evidence_found):
            evidence_text = self.font.render(f"• {evidence['name']}", True, Config.EVIDENCE_YELLOW)
            screen.blit(evidence_text, (70, evidence_y + 30 + i * 25))
        
        # Instructions
        instructions = [
            "Click on yellow circles to investigate evidence",
            "Space: Quick investigate | Escape: Return to Bureau"
        ]
        
        for i, instruction in enumerate(instructions):
            instruction_text = self.font.render(instruction, True, Config.CID_GRAY)
            screen.blit(instruction_text, (50, Config.SCREEN_HEIGHT - 60 + i * 25))
        
        # Scene completion check
        if self.investigation_progress >= 100:
            completion_text = self.title_font.render("Scene Investigation Complete!", True, Config.EVIDENCE_YELLOW)
            completion_rect = completion_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
            
            # Semi-transparent background
            overlay = pygame.Surface((Config.SCREEN_WIDTH, 100))
            overlay.set_alpha(128)
            overlay.fill(Config.BLACK)
            screen.blit(overlay, (0, Config.SCREEN_HEIGHT // 2 - 50))
            
            screen.blit(completion_text, completion_rect)
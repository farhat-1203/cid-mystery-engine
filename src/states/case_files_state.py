"""
Case Files State - Review active and closed cases
"""

import pygame
from src.states.base_state import BaseState
from src.engine.config import Config

class CaseFilesState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.selected_case = 0
        self.cases = [
            {
                "id": "CASE_001",
                "title": "The Office Murder",
                "status": "Active",
                "victim": "Mr. Sharma",
                "location": "Corporate Office, Floor 12",
                "date": "2024-12-20",
                "evidence_count": 4,
                "suspects": ["Rajesh Kumar", "Priya Singh", "Amit Patel"],
                "description": "Senior manager found dead in his office. Signs of struggle. Multiple suspects with motives.",
                "progress": 65
            },
            {
                "id": "CASE_002", 
                "title": "The Missing Diamond",
                "status": "Cold",
                "victim": "Mrs. Gupta",
                "location": "Jewelry Store, Linking Road",
                "date": "2024-11-15",
                "evidence_count": 2,
                "suspects": ["Security Guard", "Store Assistant"],
                "description": "Rare diamond worth 50 lakhs stolen during business hours. No signs of break-in.",
                "progress": 30
            },
            {
                "id": "CASE_003",
                "title": "The Cyber Fraud",
                "status": "Solved",
                "victim": "Tech Company",
                "location": "IT Park, Andheri",
                "date": "2024-10-08",
                "evidence_count": 8,
                "suspects": ["Former Employee"],
                "description": "Company database hacked, sensitive data stolen. Inside job suspected.",
                "progress": 100
            }
        ]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_case = (self.selected_case - 1) % len(self.cases)
            elif event.key == pygame.K_DOWN:
                self.selected_case = (self.selected_case + 1) % len(self.cases)
            elif event.key == pygame.K_RETURN:
                self._open_case()
            elif event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(Config.STATE_BUREAU)
    
    def _open_case(self):
        """Open selected case for investigation"""
        case = self.cases[self.selected_case]
        if case["status"] == "Active":
            # For active cases, go to crime scene
            self.state_manager.change_state(Config.STATE_CRIME_SCENE)
        # For solved/cold cases, just display details (already shown)
    
    def render(self, screen):
        # Background
        screen.fill(Config.CID_BLUE)
        
        # Title
        title_text = self.title_font.render("CID Case Files Database", True, Config.EVIDENCE_YELLOW)
        title_rect = title_text.get_rect(center=(Config.SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        # Case list (left side)
        list_x = 50
        list_y = 120
        list_width = 400
        
        list_title = self.font.render("Active Cases:", True, Config.WHITE)
        screen.blit(list_title, (list_x, list_y))
        
        for i, case in enumerate(self.cases):
            y_pos = list_y + 40 + i * 80
            
            # Case background
            if i == self.selected_case:
                pygame.draw.rect(screen, Config.EVIDENCE_YELLOW, (list_x, y_pos, list_width, 70), 2)
                bg_color = (40, 40, 80)
            else:
                bg_color = (30, 30, 60)
            
            pygame.draw.rect(screen, bg_color, (list_x + 2, y_pos + 2, list_width - 4, 66))
            
            # Case info
            case_title = self.font.render(f"{case['id']}: {case['title']}", True, Config.WHITE)
            screen.blit(case_title, (list_x + 10, y_pos + 10))
            
            # Status color coding
            status_colors = {
                "Active": Config.EVIDENCE_YELLOW,
                "Cold": Config.CID_GRAY,
                "Solved": (0, 255, 0)
            }
            status_color = status_colors.get(case["status"], Config.WHITE)
            
            status_text = self.font.render(f"Status: {case['status']}", True, status_color)
            screen.blit(status_text, (list_x + 10, y_pos + 35))
            
            progress_text = self.font.render(f"Progress: {case['progress']}%", True, Config.WHITE)
            screen.blit(progress_text, (list_x + 200, y_pos + 35))
        
        # Case details (right side)
        if self.cases:
            selected_case = self.cases[self.selected_case]
            details_x = list_x + list_width + 50
            details_y = 120
            
            details_title = self.font.render("Case Details:", True, Config.WHITE)
            screen.blit(details_title, (details_x, details_y))
            
            # Case details
            details = [
                f"Case ID: {selected_case['id']}",
                f"Title: {selected_case['title']}",
                f"Victim: {selected_case['victim']}",
                f"Location: {selected_case['location']}",
                f"Date: {selected_case['date']}",
                f"Evidence Collected: {selected_case['evidence_count']} items",
                f"Suspects: {len(selected_case['suspects'])} persons",
                "",
                "Description:",
                selected_case['description']
            ]
            
            for i, detail in enumerate(details):
                if detail == "Description:":
                    color = Config.EVIDENCE_YELLOW
                elif detail == "":
                    continue
                else:
                    color = Config.WHITE
                
                # Wrap long descriptions
                if len(detail) > 50 and detail.startswith(selected_case['description']):
                    words = detail.split()
                    lines = []
                    current_line = ""
                    
                    for word in words:
                        if len(current_line + word) < 50:
                            current_line += word + " "
                        else:
                            lines.append(current_line.strip())
                            current_line = word + " "
                    
                    if current_line:
                        lines.append(current_line.strip())
                    
                    for j, line in enumerate(lines):
                        detail_text = self.font.render(line, True, color)
                        screen.blit(detail_text, (details_x + 10, details_y + 40 + (i + j) * 25))
                else:
                    detail_text = self.font.render(detail, True, color)
                    screen.blit(detail_text, (details_x + 10, details_y + 40 + i * 25))
            
            # Suspects list
            suspects_y = details_y + 300
            suspects_title = self.font.render("Suspects:", True, Config.EVIDENCE_YELLOW)
            screen.blit(suspects_title, (details_x, suspects_y))
            
            for i, suspect in enumerate(selected_case['suspects']):
                suspect_text = self.font.render(f"• {suspect}", True, Config.WHITE)
                screen.blit(suspect_text, (details_x + 10, suspects_y + 30 + i * 25))
            
            # Action hint
            if selected_case["status"] == "Active":
                action_text = self.font.render("Press ENTER to investigate this case", True, Config.EVIDENCE_YELLOW)
                action_rect = action_text.get_rect(center=(details_x + 200, suspects_y + 120))
                screen.blit(action_text, action_rect)
        
        # Instructions
        instruction_text = self.font.render("Arrow Keys: Navigate | Enter: Open Case | Escape: Back to Bureau", True, Config.CID_GRAY)
        instruction_rect = instruction_text.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT - 30))
        screen.blit(instruction_text, instruction_rect)
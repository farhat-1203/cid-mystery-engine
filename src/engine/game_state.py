"""
Game State Manager - Handles switching between different game states
"""

import pygame
from src.engine.config import Config
from src.states.menu_state import MenuState
from src.states.bureau_state import BureauState
from src.states.crime_scene_state import CrimeSceneState
from src.states.lab_state import LabState
from src.states.interrogation_state import InterrogationState
from src.states.case_files_state import CaseFilesState
from src.states.team_briefing_state import TeamBriefingState

class GameStateManager:
    def __init__(self, screen):
        self.screen = screen
        self.states = {}
        self.current_state = None
        
        # Initialize all game states
        self._initialize_states()
        
        # Start with menu
        self.change_state(Config.STATE_MENU)
    
    def _initialize_states(self):
        """Initialize all game states"""
        self.states[Config.STATE_MENU] = MenuState(self)
        self.states[Config.STATE_BUREAU] = BureauState(self)
        self.states[Config.STATE_CRIME_SCENE] = CrimeSceneState(self)
        self.states[Config.STATE_LAB] = LabState(self)
        self.states[Config.STATE_INTERROGATION] = InterrogationState(self)
        self.states[Config.STATE_CASE_FILES] = CaseFilesState(self)
        self.states[Config.STATE_TEAM_BRIEFING] = TeamBriefingState(self)
    
    def change_state(self, new_state):
        """Change to a new game state"""
        if new_state in self.states:
            if self.current_state:
                self.current_state.exit()
            
            self.current_state = self.states[new_state]
            self.current_state.enter()
    
    def handle_event(self, event):
        """Handle pygame events"""
        if self.current_state:
            self.current_state.handle_event(event)
    
    def update(self, dt):
        """Update current state"""
        if self.current_state:
            self.current_state.update(dt)
    
    def render(self):
        """Render current state"""
        self.screen.fill(Config.BLACK)
        if self.current_state:
            self.current_state.render(self.screen)
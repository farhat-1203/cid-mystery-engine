"""
Base State class - All game states inherit from this
"""

class BaseState:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.font = None
        self._load_fonts()
    
    def _load_fonts(self):
        """Load fonts for the state"""
        import pygame
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
    
    def enter(self):
        """Called when entering this state"""
        pass
    
    def exit(self):
        """Called when exiting this state"""
        pass
    
    def handle_event(self, event):
        """Handle pygame events"""
        pass
    
    def update(self, dt):
        """Update state logic"""
        pass
    
    def render(self, screen):
        """Render state to screen"""
        pass
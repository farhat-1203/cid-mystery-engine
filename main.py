"""
CID: The Silicon Casefiles
Main entry point for the detective simulation game
"""

import pygame
import sys
from src.engine.game_state import GameStateManager
from src.engine.config import Config

def main():
    """Initialize and run the game"""
    pygame.init()
    
    # Initialize display
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("CID: The Silicon Casefiles")
    
    # Initialize game state manager
    game_state_manager = GameStateManager(screen)
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(Config.FPS) / 1000.0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game_state_manager.handle_event(event)
        
        # Update game state
        game_state_manager.update(dt)
        
        # Render
        game_state_manager.render()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
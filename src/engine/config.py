"""
Game configuration constants
"""

class Config:
    # Display settings
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 60
    
    # Colors (CID theme - dark blues and grays)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    CID_BLUE = (25, 25, 112)
    CID_GRAY = (105, 105, 105)
    EVIDENCE_YELLOW = (255, 215, 0)
    DANGER_RED = (220, 20, 60)
    
    # Game states
    STATE_MENU = "menu"
    STATE_BUREAU = "bureau"
    STATE_CRIME_SCENE = "crime_scene"
    STATE_LAB = "lab"
    STATE_INTERROGATION = "interrogation"
    STATE_CASE_FILES = "case_files"
    STATE_TEAM_BRIEFING = "team_briefing"
    
    # Team members
    TEAM_MEMBERS = {
        "ACP": {"name": "ACP Pradyuman", "specialty": "Logic & Leadership"},
        "DAYA": {"name": "Inspector Daya", "specialty": "Intimidation & Action"},
        "ABHIJEET": {"name": "Inspector Abhijeet", "specialty": "Observation & Analysis"},
        "SALUNKHE": {"name": "Dr. Salunkhe", "specialty": "Forensics & Science"}
    }
    
    # API Configuration
    GEMINI_API_KEY = None  # Set this in environment or config file
    OLLAMA_BASE_URL = "http://localhost:11434"
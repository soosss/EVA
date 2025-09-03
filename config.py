"""
===============================
GAME CONFIGURATION - COMPLETE
===============================
Complete game configuration with all required constants
"""

# === SCREEN SETTINGS ===
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_TITLE = "Evangelion Visual Novel"

# === ENHANCED COLOR PALETTE ===
COLORS = {
    # Core EVA Colors
    'NERV_RED': (200, 50, 50),
    'EVA_PURPLE': (150, 100, 200),
    'TERMINAL_GREEN': (50, 200, 50),
    'HANGAR_BLUE': (100, 150, 200),
    'SCHOOL_YELLOW': (255, 200, 50),
    'WARNING_ORANGE': (255, 150, 50),
    
    # UI Colors
    'TEXT_WHITE': (255, 255, 255),
    'TEXT_BLACK': (0, 0, 0),
    'UI_GRAY': (150, 150, 150),
    'BACKGROUND_DARK': (30, 30, 40),
    
    # Status Colors
    'SUCCESS_GREEN': (100, 255, 100),
    'ERROR_RED': (255, 100, 100),
    'INFO_BLUE': (100, 150, 255),
    'WARNING_YELLOW': (255, 255, 100)
}

# === GAME PATHS ===
ASSETS_PATH = "assets"
SAVE_PATH = "saves"
DATA_PATH = "data"

# === PLAYER SETTINGS ===
PLAYER_SPEED = 180
PLAYER_SIZE = (20, 30)

# === PLAYER START VALUES ===
PLAYER_START_HEALTH = 100
PLAYER_START_SYNC_RATIO = 50.0
PLAYER_START_STRESS = 30
PLAYER_START_LEVEL = 1
PLAYER_START_EXPERIENCE = 0
PLAYER_START_MOOD = "neutral"

# === PLAYER RELATIONSHIPS ===
PLAYER_START_RELATIONSHIPS = {
    "Asuka": 30,
    "Rei": 20,
    "Misato": 50,
    "Gendo": 10,
    "Shinji": 40
}

# === AUDIO SETTINGS ===
AUDIO_FREQUENCY = 44100
AUDIO_SIZE = -16
AUDIO_CHANNELS = 2
AUDIO_BUFFER = 512

# === DEBUG SETTINGS ===
DEBUG_MODE = False
SHOW_FPS = False
LOG_LEVEL = "INFO"

# === GAME METADATA ===
VERSION = "1.0.0"
AUTHOR = "EVA Development Team"
DESCRIPTION = "Enhanced Evangelion Visual Novel with advanced features"

# === GAME MECHANICS ===
MAX_SYNC_RATIO = 100.0
MIN_SYNC_RATIO = 0.0
MAX_STRESS_LEVEL = 100
MIN_STRESS_LEVEL = 0
EXPERIENCE_PER_LEVEL = 100

# === UI SETTINGS ===
HUD_WIDTH = 220
MESSAGE_DISPLAY_TIME = 3.0
TOOLTIP_DELAY = 0.5

print("⚙️ Complete configuration loaded with all player constants")
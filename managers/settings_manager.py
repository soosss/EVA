"""
===============================
SETTINGS MANAGER - COMPLETE
===============================
Professional settings management system
"""

import pygame
import json
import os

# Add proper imports for screen dimensions
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT

class SettingsManager:
    """Complete settings management system"""
    
    def __init__(self):
        """Initialize settings manager"""
        self.settings_file = "data/settings.json"
        self.default_settings = {
            "audio": {
                "master_volume": 100,
                "music_volume": 80,
                "sfx_volume": 90,
                "voice_volume": 100
            },
            "display": {
                "resolution": f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}",
                "fullscreen": False,
                "vsync": True,
                "brightness": 100
            },
            "gameplay": {
                "difficulty": "normal",
                "auto_save": True,
                "text_speed": 3,
                "skip_read": False
            },
            "controls": {
                "confirm": pygame.K_RETURN,
                "cancel": pygame.K_ESCAPE,
                "skip": pygame.K_TAB,
                "menu": pygame.K_ESCAPE
            }
        }
        
        self.current_settings = self.default_settings.copy()
        self._ensure_directories()
        self.load_settings()
        
        print("⚙️ Settings Manager initialized")
    
    def _ensure_directories(self):
        """Ensure settings directory exists"""
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to handle new settings
                    self._merge_settings(loaded_settings)
        except Exception as e:
            print(f"⚠️ Error loading settings: {e}")
            self.current_settings = self.default_settings.copy()
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.current_settings, f, indent=4)
            return True
        except Exception as e:
            print(f"⚠️ Error saving settings: {e}")
            return False
    
    def get_setting(self, category, key):
        """Get specific setting value"""
        return self.current_settings.get(category, {}).get(key)
    
    def set_setting(self, category, key, value):
        """Set specific setting value"""
        if category not in self.current_settings:
            self.current_settings[category] = {}
        self.current_settings[category][key] = value
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.current_settings = self.default_settings.copy()
    
    def _merge_settings(self, loaded_settings):
        """Merge loaded settings with defaults"""
        for category, settings in self.default_settings.items():
            if category in loaded_settings:
                for key, default_value in settings.items():
                    if key in loaded_settings[category]:
                        self.current_settings[category][key] = loaded_settings[category][key]
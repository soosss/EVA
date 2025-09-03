"""
===============================
DIRECTORY CREATOR
===============================
Creates all necessary directories for the game
"""

import os

def create_game_directories():
    """Create all necessary game directories"""
    directories = [
        # Main directories
        "assets",
        "assets/art",
        "assets/art/characters",
        "assets/art/angels",
        "assets/art/backgrounds", 
        "assets/art/portraits",
        "assets/art/ui",
        "assets/art/icons",
        "assets/art/effects",
        "assets/art/eva_units",
        
        # Data directories
        "data",
        "data/dialogues",
        "data/dialogues/backups",
        
        # Manager directories
        "managers",
        
        # Scene directories
        "scenes",
        
        # Entity directories
        "entities",
        
        # UI directories
        "ui",
        
        # Input directories
        "input",
        
        # Graphics directories
        "graphics"
    ]
    
    print("📁 Creating game directories...")
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ {directory}")
    
    print("📁 All directories created!")

if __name__ == "__main__":
    create_game_directories()
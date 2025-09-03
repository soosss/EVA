#!/usr/bin/env python3
"""
Easy launcher for the Evangelion game
Checks dependencies and provides helpful error messages
"""

import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    return True

def check_pygame():
    """Check if pygame is installed"""
    try:
        import pygame
        print(f"✅ Pygame {pygame.version.ver} found")
        return True
    except ImportError:
        print("❌ Pygame not found!")
        print("   Install with: pip install pygame")
        return False

def launch_game():
    """Launch the main game"""
    print("🎮 Launching Evangelion: Third Child...")
    print("=" * 50)
    
    # Import and run main game
    try:
        from main import main
        main()
    except KeyboardInterrupt:
        print("\n👋 Game closed by user")
    except Exception as e:
        print(f"\n❌ Game error: {e}")
        print("   Check the crash_log.txt file for details")

def main():
    """Main launcher function"""
    print("🚀 Evangelion Game Launcher")
    print("=" * 30)
    
    # Check system requirements
    if not check_python_version():
        return 1
    
    if not check_pygame():
        return 1
    
    # Launch game
    launch_game()
    return 0

if __name__ == "__main__":
    exit(main())
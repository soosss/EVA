"""
===============================
NEON GENESIS EVANGELION: THIRD CHILD
MAIN GAME LAUNCHER
===============================
Clean, optimized game entry point

Features:
- Error handling and crash protection
- Performance monitoring
- Clean shutdown procedures
"""

import pygame
import sys
from game_engine import GameEngine
from config import GAME_TITLE, VERSION

def main():
    """
    Main game entry point
    Handles initialization, execution, and cleanup
    """
    print("=" * 60)
    print(f"🎮 {GAME_TITLE}")
    print(f"📦 Version {VERSION}")
    print("=" * 60)
    
    game_engine = None
    
    try:
        # Initialize Pygame
        pygame.init()
        print("✅ Pygame initialized successfully")
        
        # Create and run game engine
        game_engine = GameEngine()
        print("✅ Game engine created successfully")
        
        # Start main game loop
        print("🚀 Starting game...")
        game_engine.run()
        
    except KeyboardInterrupt:
        print("\n⏹️ Game interrupted by user")
        
    except Exception as e:
        print(f"\n❌ Game crashed with error: {e}")
        import traceback
        traceback.print_exc()
        
        # Save crash log
        try:
            with open("crash_log.txt", "w") as f:
                f.write(f"Game Crash Report\n")
                f.write(f"Version: {VERSION}\n")
                f.write(f"Error: {str(e)}\n")
                f.write(f"Traceback:\n{traceback.format_exc()}")
            print("💾 Crash log saved to crash_log.txt")
        except:
            pass
    
    finally:
        # Clean shutdown
        if game_engine:
            try:
                game_engine.shutdown()
                print("🧹 Game engine cleaned up")
            except:
                pass
        
        pygame.quit()
        print("👋 Game shutdown complete")
        sys.exit()

if __name__ == "__main__":
    main()
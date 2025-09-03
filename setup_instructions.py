"""
===============================
SETUP INSTRUCTIONS
===============================
Script to help users set up art and dialogue systems
"""

import os
from assets.art_manager import ArtManager
from data.dialogue_editor import DialogueEditor

def setup_game_content():
    """Set up game content systems"""
    print("🎮 NEON GENESIS EVANGELION: THIRD CHILD")
    print("=" * 50)
    print("🎨 CONTENT SETUP GUIDE")
    print()
    
    # Initialize systems
    art_manager = ArtManager()
    dialogue_editor = DialogueEditor()
    
    print("✅ Art and dialogue systems initialized!")
    print()
    
    # Save default assets for editing
    print("💾 Saving default assets for editing...")
    art_manager.save_default_assets()
    print("✅ Default assets saved to asset folders")
    print()
    
    # Show folder locations
    print("📁 FOLDER LOCATIONS:")
    print(f"  🎨 Art Assets: {os.path.abspath('assets/art/')}")
    print(f"  💬 Dialogues: {os.path.abspath('data/dialogues/')}")
    print()
    
    print("🎨 ART CUSTOMIZATION:")
    print("  1. Find the assets/art/ folders")
    print("  2. Edit the PNG files with your favorite image editor")
    print("  3. Keep the same filenames and dimensions")
    print("  4. Restart the game to see changes")
    print()
    
    print("💬 DIALOGUE EDITING:")
    print("  1. Open data/dialogues/ folder")
    print("  2. Edit the JSON files or create new ones")
    print("  3. Use TEMPLATE.json as a guide")
    print("  4. Follow the README.txt instructions")
    print()
    
    print("🔧 QUICK CUSTOMIZATION:")
    print("  • Character sprites: 32x48 pixels")
    print("  • Character portraits: 96x96 pixels")
    print("  • Backgrounds: 800x600 pixels")
    print("  • Icons: 24x24 pixels")
    print()
    
    print("🚀 Ready to customize your EVA game!")

if __name__ == "__main__":
    setup_game_content()
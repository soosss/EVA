# Neon Genesis Evangelion: Third Child - Python/Pygame Game

## Overview

This is a complete **Python/Pygame implementation** of an Evangelion-themed visual novel/RPG game. The game features a comprehensive story-driven experience with character relationships, battles, and exploration elements.

## 🎮 Game Features

### ✅ **COMPLETE IMPLEMENTATION**
- **Full Python/Pygame architecture** with optimized game engine
- **Multiple interactive scenes** (9 different areas)
- **Character relationship system** with 5 main characters
- **Player progression** (levels, sync ratio, health, stress)
- **Save/Load system** with multiple save slots
- **Enhanced UI** with HUD, status messages, and menus
- **Action battle system** for Angel encounters
- **Dialogue system** with conditional branching
- **Performance monitoring** and debug features

### 🎬 Available Scenes
- **Main Menu** - Game entry point with animated background
- **Bedroom** - Starting location with Asuka interactions
- **NERV Arrival** - Mission briefing and story progression
- **Hub Scene** - Complete NERV HQ with multiple areas
- **Town** - Tokyo-3 exploration
- **Action Battle** - Angel combat system
- **Pause Menu** - Game controls and options
- **Settings** - Configuration options
- **Art Gallery** - Visual showcase

### 👥 Character System
**Main Characters:**
- Shinji Ikari (Player Character)
- Asuka Langley Soryu (Second Child) - Relationship: 30
- Rei Ayanami (First Child) - Relationship: 20
- Misato Katsuragi (Guardian) - Relationship: 50
- Gendo Ikari (Father/Commander) - Relationship: 10

### 🎯 Player Stats
- **Health:** 100/100
- **Sync Ratio:** 50.0%
- **Stress Level:** 30/100
- **Level:** 1
- **Experience:** 0

## 🚀 Running the Game

### Prerequisites
```bash
pip install pygame
```

### Launch Game
```bash
python3 main.py
```

### Demo Script
```bash
python3 demo_test.py
```

## 🎮 Controls
- **Mouse** - Navigate menus and interact with objects
- **Keyboard** - Number keys for dialogue choices
- **F11** - Toggle fullscreen
- **TAB** - Toggle HUD
- **ESC** - Pause menu/exit
- **F1** - Debug info (if debug mode enabled)

## 📁 Project Structure

```
EVA/
├── main.py                 # Game entry point
├── game_engine.py          # Core game engine
├── config.py              # Game configuration
├── managers/              # Game systems
│   ├── game_manager.py    # Player data & game state
│   ├── scene_manager.py   # Scene transitions
│   └── dialogue_manager.py # Dialogue system
├── scenes/                # Game scenes
│   ├── main_menu.py
│   ├── bedroom_scene.py
│   ├── hub_scene.py
│   └── ...
├── ui/                    # User interface
│   ├── hud.py
│   └── status_popup.py
├── graphics/              # Visual effects
├── data/                  # Game data
└── assets/               # Game assets
```

## 🔧 Technical Features

- **Error Handling:** Comprehensive exception handling with crash logging
- **Performance:** Optimized rendering with FPS monitoring
- **Save System:** JSON-based save files with backup support
- **Modular Design:** Clean separation of concerns
- **Debug Mode:** Built-in debugging and performance tools

## 📝 Current Status

**✅ COMPLETE AND FUNCTIONAL**

This is a fully working Python/Pygame game with all core systems implemented. The game can be played from start and includes:

- Complete game loop
- Working scenes and navigation
- Character interactions
- Save/load functionality
- Battle system
- Progression mechanics

## 🎨 Screenshots

![Main Menu](main_menu_screenshot.png)
*The game's main menu with animated background*

---

**Created by:** EVA Development Team  
**Version:** 1.0.0  
**Engine:** Python 3.x + Pygame 2.x
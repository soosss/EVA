# Installation and Setup Guide

## Quick Start

1. **Install Python 3.7+** (if not already installed)
2. **Install Pygame:**
   ```bash
   pip install pygame
   ```
3. **Run the game:**
   ```bash
   python3 main.py
   # OR use the launcher
   python3 launch_game.py
   ```

## Alternative Launch Methods

### Method 1: Direct Launch
```bash
python3 main.py
```

### Method 2: Using Launcher (Recommended)
```bash
python3 launch_game.py
```

### Method 3: Demo Mode
```bash
python3 demo_test.py
```

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'pygame'"**
- Solution: `pip install pygame`

**"Permission denied"**
- Solution: `chmod +x launch_game.py` (Linux/Mac)

**Audio errors (ALSA warnings)**
- These are normal on headless systems and don't affect gameplay

### System Requirements

- **Python:** 3.7 or higher
- **Pygame:** 2.0 or higher  
- **OS:** Windows, macOS, or Linux
- **Memory:** 512MB RAM minimum
- **Storage:** 50MB free space

## Game Controls

- **Navigation:** Mouse or arrow keys
- **Select:** Click or Enter
- **Menu:** ESC key
- **Fullscreen:** F11
- **Debug:** F1 (if enabled)

## Features Verification

Run the demo script to verify all features work:
```bash
python3 demo_test.py
```

Expected output:
```
🎮 Evangelion Visual Novel - DEMO
✅ Pygame initialized successfully
✅ Game engine created successfully
📸 Main menu screenshot saved
🎬 Available scenes: 9 scenes
🎯 Current scene: MainMenuScene
🎮 Player level: 1
🔄 Sync ratio: 50.0%
❤️ Health: 100
😰 Stress: 30
💕 Relationships: 5 characters
✅ Demo completed successfully!
```
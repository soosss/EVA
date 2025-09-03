# Bedroom Scene UI Fixes

## Issues Fixed

### 1. Conversation UI Overlap with Right-side HUD
**Problem**: The conversation UI was spanning the full width (x=50 to x=700) which overlapped with the HUD starting at x=570.

**Solution**: Modified the conversation width calculation in `scenes/bedroom_scene.py`:
```python
# Before: 
conv_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 120)

# After:
hud_start_x = SCREEN_WIDTH - 220 - 10  # Match HUD positioning
conv_width = hud_start_x - 50 - 20  # Leave 20px margin from HUD  
conv_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, conv_width, 120)
```

### 2. HUD Visual Separation
**Problem**: The HUD had insufficient visual separation from the game area, making it appear as if game content was rendering behind it.

**Solution**: Enhanced the HUD background in `ui/hud.py`:
- Increased background opacity from 220 to 240 alpha
- Added thicker red border (3px instead of 2px)
- Added subtle secondary border for better visual definition

### 3. Game Area Rendering Behind HUD
**Problem**: Background and floor elements were rendering across the full screen width, appearing behind the HUD.

**Solution**: Constrained game area rendering in `scenes/bedroom_scene.py`:
```python
# Calculate playable area
hud_start_x = SCREEN_WIDTH - 220 - 10
playable_width = hud_start_x

# Constrain background and floor to playable area
background_rect = pygame.Rect(0, 0, playable_width, SCREEN_HEIGHT)
floor_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, playable_width, 100)
```

## Result
- Conversation UI no longer overlaps with HUD
- Clear visual separation between HUD and game area
- Improved usability and user experience
- Screenshots captured showing the improvements
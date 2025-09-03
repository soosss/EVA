"""
===============================
STATUS SYSTEM - COMPLETE
===============================
Professional status message system
"""

import pygame
import time

# Add proper imports for screen dimensions
try:
    from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    from config import COLORS
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

class StatusSystem:
    """Professional status message system"""
    
    def __init__(self):
        """Initialize status system"""
        self.messages = []
        self.max_messages = 5
        self.message_duration = 3.0
        self.fade_duration = 0.5
        
        # Fonts
        self.message_font = pygame.font.Font(None, 18)
        self.priority_font = pygame.font.Font(None, 20)
        
        # Animation
        self.animation_timer = 0
        
        print("💬 Status System initialized")
    
    def add_message(self, text, message_type="info", priority=0):
        """Add status message"""
        message = {
            "text": text,
            "type": message_type,
            "priority": priority,
            "time": time.time(),
            "alpha": 255,
            "y_offset": 0
        }
        
        # Add to messages
        self.messages.append(message)
        
        # Sort by priority
        self.messages.sort(key=lambda m: m["priority"], reverse=True)
        
        # Limit message count
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[:self.max_messages]
    
    def update(self, dt):
        """Update status system"""
        self.animation_timer += dt
        current_time = time.time()
        
        # Update message states
        for message in self.messages[:]:
            age = current_time - message["time"]
            
            # Calculate fade
            if age > self.message_duration - self.fade_duration:
                fade_progress = (age - (self.message_duration - self.fade_duration)) / self.fade_duration
                message["alpha"] = max(0, int(255 * (1 - fade_progress)))
            
            # Remove expired messages
            if age > self.message_duration:
                self.messages.remove(message)
    
    def render(self, screen):
        """Render status messages"""
        if not self.messages:
            return
        
        # Message area
        message_x = 20
        message_y = 80
        
        for i, message in enumerate(self.messages):
            # Message colors by type
            type_colors = {
                "info": COLORS['INFO_BLUE'],
                "success": COLORS['SUCCESS_GREEN'],
                "warning": COLORS['WARNING_ORANGE'],
                "error": COLORS['ERROR_RED'],
                "neutral": COLORS['TEXT_WHITE']
            }
            
            color = type_colors.get(message["type"], COLORS['TEXT_WHITE'])
            
            # Create message surface with alpha
            font = self.priority_font if message["priority"] > 0 else self.message_font
            text_surface = font.render(message["text"], True, color)
            
            # Apply alpha
            if message["alpha"] < 255:
                text_surface.set_alpha(message["alpha"])
            
            # Position
            y_pos = message_y + i * 25
            
            # Background for important messages
            if message["priority"] > 0:
                bg_rect = pygame.Rect(message_x - 5, y_pos - 2, text_surface.get_width() + 10, text_surface.get_height() + 4)
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                bg_surface.fill((0, 0, 0, 100))
                screen.blit(bg_surface, bg_rect.topleft)
            
            # Render message
            screen.blit(text_surface, (message_x, y_pos))
"""
===============================
ENHANCED RENDERER
===============================
Enhanced graphics rendering system
"""

import pygame
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT

class EnhancedRenderer:
    """
    ENHANCED RENDERER CLASS
    Improved graphics rendering
    """
    
    def __init__(self):
        """Initialize enhanced renderer"""
        self.animation_time = 0
        print("🎨 Enhanced Renderer initialized")
    
    def update(self, dt):
        """Update renderer"""
        self.animation_time += dt
    
    def render_nerv_headquarters(self, screen):
        """Render NERV headquarters background"""
        # Dark tech background
        screen.fill((30, 30, 50))
        
        # Animated grid pattern
        import math
        grid_color = (60, 60, 80)
        grid_alpha = int(50 + 25 * math.sin(self.animation_time))
        
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(screen, (*grid_color, grid_alpha), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(screen, (*grid_color, grid_alpha), (0, y), (SCREEN_WIDTH, y))
        
        # Central command displays
        for i in range(3):
            display_x = 150 + i * 200
            display_y = 100
            display_rect = pygame.Rect(display_x, display_y, 150, 80)
            
            # Display background
            pygame.draw.rect(screen, (10, 30, 60), display_rect)
            pygame.draw.rect(screen, COLORS['HANGAR_BLUE'], display_rect, 2)
            
            # Display content
            font = pygame.font.Font(None, 16)
            texts = ["MAGI-01", "MAGI-02", "MAGI-03"]
            text_surface = font.render(texts[i], True, COLORS['TERMINAL_GREEN'])
            text_rect = text_surface.get_rect(center=display_rect.center)
            screen.blit(text_surface, text_rect)
        
        # Status panels
        for i in range(6):
            panel_x = 50 + i * 120
            panel_y = SCREEN_HEIGHT - 120
            panel_rect = pygame.Rect(panel_x, panel_y, 100, 60)
            
            pygame.draw.rect(screen, (20, 40, 60), panel_rect)
            pygame.draw.rect(screen, COLORS['TERMINAL_GREEN'], panel_rect, 1)
            
            # Panel details
            detail_text = f"SYS-{i+1:02d}"
            detail_surface = pygame.font.Font(None, 14).render(detail_text, True, COLORS['TERMINAL_GREEN'])
            screen.blit(detail_surface, (panel_x + 5, panel_y + 5))
            
            # Status indicator
            status_color = COLORS['TERMINAL_GREEN'] if i % 2 == 0 else COLORS['WARNING_ORANGE']
            pygame.draw.circle(screen, status_color, (panel_x + 85, panel_y + 45), 5)
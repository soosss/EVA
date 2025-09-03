"""
===============================
NPC ENTITY - BASIC VERSION
===============================
Simple NPC class for dialogue and interaction
"""

import pygame
from config import COLORS

class NPC:
    """Basic NPC class for character interactions"""
    
    def __init__(self, name, x, y, description=""):
        self.name = name
        self.x = x
        self.y = y
        self.description = description
        self.dialogue_lines = []
        self.width = 25
        self.height = 35
        
    def add_dialogue(self, line):
        """Add dialogue line"""
        self.dialogue_lines.append(line)
    
    def update(self, dt):
        """Update NPC"""
        pass
    
    def render(self, screen):
        """Render NPC"""
        # Simple rectangle representation
        rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        pygame.draw.rect(screen, COLORS['WARNING_ORANGE'], rect)
        pygame.draw.rect(screen, COLORS['TEXT_WHITE'], rect, 2)
        
        # Name label
        font = pygame.font.Font(None, 16)
        name_surface = font.render(self.name.split()[0], True, COLORS['TEXT_WHITE'])
        name_rect = name_surface.get_rect(center=(self.x, self.y - 25))
        screen.blit(name_surface, name_rect)
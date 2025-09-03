"""
===============================
DIALOGUE SYSTEM
===============================
Handles dialogue display and management
"""

import pygame
from config import COLORS

class DialogueManager:
    """
    DIALOGUE MANAGER CLASS
    Manages dialogue display and progression
    """
    
    def __init__(self):
        """Initialize dialogue manager"""
        self.active = False
        self.current_text = ""
        self.current_speaker = ""
        self.display_timer = 0
        self.auto_hide_time = 5.0
        
        self.font = pygame.font.Font(None, 24)
        self.speaker_font = pygame.font.Font(None, 20)
    
    def show_dialogue(self, text, speaker="System"):
        """Show dialogue text"""
        self.current_text = text
        self.current_speaker = speaker
        self.active = True
        self.display_timer = 0
    
    def show_dialogue_with_options(self, text, speaker, options):
        """Show dialogue with multiple choice options"""
        self.show_dialogue(text, speaker)
        # Options would be handled by the calling scene
    
    def hide_dialogue(self):
        """Hide dialogue"""
        self.active = False
    
    def update(self, dt):
        """Update dialogue system"""
        if self.active:
            self.display_timer += dt
            if self.display_timer >= self.auto_hide_time:
                self.hide_dialogue()
    
    def render(self, screen):
        """Render dialogue if active"""
        if not self.active:
            return
        
        # Dialogue box
        box_height = 100
        box_rect = pygame.Rect(50, screen.get_height() - box_height - 50, 
                              screen.get_width() - 100, box_height)
        
        # Background
        pygame.draw.rect(screen, (20, 20, 40), box_rect)
        pygame.draw.rect(screen, COLORS['HANGAR_BLUE'], box_rect, 2)
        
        # Speaker
        if self.current_speaker != "System":
            speaker_surface = self.speaker_font.render(self.current_speaker, True, COLORS['SCHOOL_YELLOW'])
            screen.blit(speaker_surface, (box_rect.left + 10, box_rect.top + 5))
        
        # Text
        text_y = box_rect.top + 30 if self.current_speaker != "System" else box_rect.top + 10
        text_surface = self.font.render(self.current_text, True, COLORS['TEXT_WHITE'])
        screen.blit(text_surface, (box_rect.left + 10, text_y))
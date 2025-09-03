"""
===============================
ANGEL ENTITY (WITH ART SUPPORT)
===============================
Angel enemies with custom art integration
"""

import pygame
import math
from config import COLORS

class Angel:
    """
    ANGEL CLASS
    Enemy angels with art manager integration
    """
    
    def __init__(self, name, x, y, art_manager=None):
        """Initialize Angel with art support"""
        self.name = name
        self.x = x
        self.y = y
        self.art_manager = art_manager
        
        # Size varies by Angel type
        if name.lower() == "ramiel":
            self.width = 120
            self.height = 120
        elif "tutorial" in name.lower():
            self.width = 60
            self.height = 80
        else:
            self.width = 80
            self.height = 120
        
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)
        
        # Stats
        self.hp = 200
        self.max_hp = 200
        self.attack_power = 25
        
        # Tutorial Angel is weaker
        if "tutorial" in name.lower():
            self.hp = 100
            self.max_hp = 100
            self.attack_power = 15
        
        # Animation
        self.animation_timer = 0
        self.pulse_intensity = 0
        
        # Attack
        self.last_attack_time = 0
        self.attack_cooldown = 3.0
        
        # AT Field
        self.at_field_active = True
        self.at_field_strength = 100
    
    def update(self, dt):
        """Update Angel"""
        self.animation_timer += dt
        self.pulse_intensity = 0.5 + 0.5 * math.sin(self.animation_timer * 2)
        
        # Update rect position
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
    
    def render(self, screen):
        """Render Angel with custom art"""
        if self.art_manager:
            # Try to get custom Angel sprite
            angel_sprite_name = self.name.lower().replace(" ", "_")
            angel_sprite = self.art_manager.get_asset(angel_sprite_name)
            
            if angel_sprite:
                # Scale sprite to Angel size
                sprite_scaled = pygame.transform.scale(angel_sprite, (self.width, self.height))
                sprite_rect = sprite_scaled.get_rect(center=(self.x, self.y))
                screen.blit(sprite_scaled, sprite_rect)
                
                # Add pulsing effect overlay
                if self.pulse_intensity > 0.7:
                    pulse_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                    pulse_alpha = int((self.pulse_intensity - 0.7) * 200)
                    pulse_surface.fill((255, 100, 100, pulse_alpha))
                    screen.blit(pulse_surface, sprite_rect.topleft)
                
                # AT Field effect
                if self.at_field_active:
                    self._render_at_field_with_art(screen)
                
                # Health bar
                self._render_health_bar(screen)
                
                return
        
        # Fallback to original rendering
        self._render_fallback(screen)
    
    def _render_at_field_with_art(self, screen):
        """Render AT Field with custom art"""
        if self.art_manager:
            at_field_effect = self.art_manager.get_asset('at_field')
            if at_field_effect:
                # Scale and position AT Field effect
                field_size = int(self.width * 1.5)
                at_field_scaled = pygame.transform.scale(at_field_effect, (field_size, field_size))
                
                # Add pulsing alpha
                alpha = int(100 + 50 * self.pulse_intensity)
                at_field_scaled.set_alpha(alpha)
                
                field_rect = at_field_scaled.get_rect(center=(self.x, self.y))
                screen.blit(at_field_scaled, field_rect)
                return
        
        # Fallback AT Field
        at_field_radius = int(self.width//2 + 10 + 10 * self.pulse_intensity)
        pygame.draw.circle(screen, (*COLORS['EVA_PURPLE'], 100), 
                         (int(self.x), int(self.y)), at_field_radius, 2)
    
    def _render_health_bar(self, screen):
        """Render Angel health bar"""
        bar_width = self.width + 20
        bar_height = 8
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.height // 2 - 20
        
        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, (40, 40, 40), bg_rect)
        pygame.draw.rect(screen, COLORS['NERV_RED'], bg_rect, 1)
        
        # Health fill
        health_ratio = self.hp / self.max_hp
        health_width = int(bar_width * health_ratio)
        if health_width > 0:
            health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
            pygame.draw.rect(screen, COLORS['NERV_RED'], health_rect)
        
        # Name label
        font = pygame.font.Font(None, 16)
        name_surface = font.render(f"Angel: {self.name}", True, COLORS['TEXT_WHITE'])
        name_rect = name_surface.get_rect(center=(self.x, bar_y - 15))
        
        # Name background
        bg_rect = name_rect.inflate(6, 3)
        pygame.draw.rect(screen, (0, 0, 0, 150), bg_rect)
        screen.blit(name_surface, name_rect)
    
    def _render_fallback(self, screen):
        """Fallback rendering without art manager"""
        # Original rendering code
        base_color = COLORS['NERV_RED']
        pulse_color = (
            min(255, int(base_color[0] * (0.5 + self.pulse_intensity * 0.5))),
            min(255, int(base_color[1] * (0.5 + self.pulse_intensity * 0.5))),
            min(255, int(base_color[2] * (0.5 + self.pulse_intensity * 0.5)))
        )
        
        # Main body
        pygame.draw.rect(screen, pulse_color, self.rect)
        
        # AT Field
        at_field_radius = int(40 + 10 * self.pulse_intensity)
        pygame.draw.circle(screen, (*COLORS['EVA_PURPLE'], 100), 
                         (int(self.x), int(self.y)), at_field_radius, 2)
        
        # Core
        core_rect = pygame.Rect(self.x - 10, self.y - 10, 20, 20)
        pygame.draw.rect(screen, COLORS['WARNING_ORANGE'], core_rect)
        
        # Border
        pygame.draw.rect(screen, COLORS['TEXT_WHITE'], self.rect, 2)
        
        # Health bar
        self._render_health_bar(screen)
    
    def take_damage(self, damage):
        """Angel takes damage"""
        if self.at_field_active:
            # AT Field reduces damage
            damage = int(damage * 0.7)
        
        self.hp -= damage
        
        # AT Field breaks if severely damaged
        if self.hp < self.max_hp * 0.3:
            self.at_field_active = False
        
        return self.hp <= 0  # Returns True if defeated
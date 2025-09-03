"""
===============================
ACTION BATTLE SCENE - COMPLETE
===============================
Enhanced battle scene with Angel combat
"""

import pygame
import math
import random

# Add proper imports for screen dimensions
try:
    from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    from config import COLORS
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

class ActionBattleScene:
    """Complete enhanced action battle scene"""
    
    def __init__(self, game_manager, scene_manager, angel_name="Sachiel"):
        """Initialize battle scene"""
        self.game_manager = game_manager
        self.scene_manager = scene_manager
        self.angel_name = angel_name
        
        # Battle state
        self.battle_phase = "approach"  # approach, combat, victory, defeat
        self.eva_health = 100
        self.angel_health = 100
        self.sync_ratio = 75.0
        self.at_field_active = False
        
        # Animation
        self.animation_timer = 0
        self.explosion_effects = []
        
        # UI
        self.fonts = {
            "title": pygame.font.Font(None, 36),
            "ui": pygame.font.Font(None, 20),
            "status": pygame.font.Font(None, 18)
        }
        
        # Controls
        self.controls_help = [
            "SPACE: Attack",
            "A: AT Field",
            "S: Special Attack",
            "ESC: Emergency Exit"
        ]
        
        print(f"⚔️ Battle Scene initialized - Angel: {angel_name}")
    
    def handle_event(self, event):
        """Handle battle events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._player_attack()
            elif event.key == pygame.K_a:
                self._activate_at_field()
            elif event.key == pygame.K_s:
                self._special_attack()
            elif event.key == pygame.K_ESCAPE:
                self._emergency_exit()
    
    def _player_attack(self):
        """Execute player attack"""
        if self.battle_phase == "combat":
            damage = random.randint(15, 25)
            self.angel_health = max(0, self.angel_health - damage)
            self._add_explosion_effect(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2)
            
            if self.angel_health <= 0:
                self.battle_phase = "victory"
    
    def _activate_at_field(self):
        """Activate AT Field defense"""
        self.at_field_active = True
        self.sync_ratio = min(100, self.sync_ratio + 5)
    
    def _special_attack(self):
        """Execute special attack"""
        if self.sync_ratio >= 80:
            damage = random.randint(30, 40)
            self.angel_health = max(0, self.angel_health - damage)
            self.sync_ratio -= 20
            self._add_explosion_effect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def _emergency_exit(self):
        """Emergency retreat"""
        self.battle_phase = "defeat"
        self.scene_manager.change_scene("hub")
    
    def _add_explosion_effect(self, x, y):
        """Add explosion visual effect"""
        self.explosion_effects.append({
            "x": x, "y": y, "timer": 0.5, "size": 20
        })
    
    def update(self, dt):
        """Update battle scene"""
        self.animation_timer += dt
        
        # Update explosion effects
        for effect in self.explosion_effects[:]:
            effect["timer"] -= dt
            effect["size"] += dt * 50
            if effect["timer"] <= 0:
                self.explosion_effects.remove(effect)
        
        # Angel AI
        if self.battle_phase == "combat" and random.random() < 0.02:
            self._angel_attack()
        
        # Battle phase transitions
        if self.battle_phase == "approach" and self.animation_timer > 3:
            self.battle_phase = "combat"
        elif self.battle_phase == "victory" and self.animation_timer > 10:
            self._victory_sequence()
        elif self.battle_phase == "defeat":
            self.scene_manager.change_scene("hub")
    
    def _angel_attack(self):
        """Angel attacks player"""
        if not self.at_field_active:
            damage = random.randint(10, 20)
            self.eva_health = max(0, self.eva_health - damage)
            if self.eva_health <= 0:
                self.battle_phase = "defeat"
        else:
            self.at_field_active = False
    
    def _victory_sequence(self):
        """Handle victory"""
        self.game_manager.modify_relationship("Misato", 5)
        self.scene_manager.change_scene("hub")
    
    def render(self, screen):
        """Render battle scene"""
        # Background
        screen.fill((10, 10, 20))
        
        # City background
        self._render_city_background(screen)
        
        # EVA Unit
        self._render_eva_unit(screen)
        
        # Angel
        self._render_angel(screen)
        
        # Effects
        self._render_effects(screen)
        
        # UI
        self._render_battle_ui(screen)
        
        # Phase-specific rendering
        if self.battle_phase == "approach":
            self._render_approach_sequence(screen)
        elif self.battle_phase == "victory":
            self._render_victory_sequence(screen)
    
    def _render_city_background(self, screen):
        """Render city background"""
        # Simple city silhouette
        for i in range(0, SCREEN_WIDTH, 60):
            height = random.randint(100, 200)
            building_rect = pygame.Rect(i, SCREEN_HEIGHT - height, 50, height)
            pygame.draw.rect(screen, (30, 30, 40), building_rect)
            pygame.draw.rect(screen, (50, 50, 60), building_rect, 1)
    
    def _render_eva_unit(self, screen):
        """Render EVA unit"""
        eva_x = SCREEN_WIDTH // 4
        eva_y = SCREEN_HEIGHT // 2
        
        # EVA body (simplified)
        eva_rect = pygame.Rect(eva_x - 30, eva_y - 50, 60, 100)
        pygame.draw.rect(screen, COLORS['EVA_PURPLE'], eva_rect)
        pygame.draw.rect(screen, COLORS['TEXT_WHITE'], eva_rect, 2)
        
        # AT Field effect
        if self.at_field_active:
            at_field_radius = 80 + 10 * math.sin(self.animation_timer * 10)
            pygame.draw.circle(screen, (*COLORS['TERMINAL_GREEN'], 100), 
                             (eva_x, eva_y), int(at_field_radius), 3)
    
    def _render_angel(self, screen):
        """Render Angel"""
        angel_x = 3 * SCREEN_WIDTH // 4
        angel_y = SCREEN_HEIGHT // 2
        
        # Angel shape (geometric)
        angel_size = 40 + 5 * math.sin(self.animation_timer * 3)
        angel_rect = pygame.Rect(angel_x - angel_size//2, angel_y - angel_size//2, 
                                angel_size, angel_size)
        pygame.draw.rect(screen, COLORS['NERV_RED'], angel_rect)
        pygame.draw.rect(screen, COLORS['WARNING_ORANGE'], angel_rect, 3)
    
    def _render_effects(self, screen):
        """Render visual effects"""
        for effect in self.explosion_effects:
            alpha = int(255 * (effect["timer"] / 0.5))
            explosion_surface = pygame.Surface((effect["size"] * 2, effect["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(explosion_surface, (*COLORS['WARNING_ORANGE'], alpha), 
                             (effect["size"], effect["size"]), effect["size"])
            screen.blit(explosion_surface, (effect["x"] - effect["size"], effect["y"] - effect["size"]))
    
    def _render_battle_ui(self, screen):
        """Render battle UI"""
        # Health bars
        self._render_health_bar(screen, "EVA", self.eva_health, 50, 50, COLORS['SUCCESS_GREEN'])
        self._render_health_bar(screen, "ANGEL", self.angel_health, 50, 90, COLORS['NERV_RED'])
        
        # Sync ratio
        sync_text = f"Sync Ratio: {self.sync_ratio:.1f}%"
        sync_surface = self.fonts["ui"].render(sync_text, True, COLORS['EVA_PURPLE'])
        screen.blit(sync_surface, (50, 130))
        
        # Controls
        for i, control in enumerate(self.controls_help):
            control_surface = self.fonts["status"].render(control, True, COLORS['UI_GRAY'])
            screen.blit(control_surface, (SCREEN_WIDTH - 200, 50 + i * 20))
    
    def _render_health_bar(self, screen, label, health, x, y, color):
        """Render health bar"""
        bar_width = 200
        bar_height = 20
        
        # Background
        bg_rect = pygame.Rect(x + 80, y, bar_width, bar_height)
        pygame.draw.rect(screen, (60, 60, 60), bg_rect)
        
        # Health fill
        fill_width = int(bar_width * (health / 100))
        if fill_width > 0:
            fill_rect = pygame.Rect(x + 80, y, fill_width, bar_height)
            pygame.draw.rect(screen, color, fill_rect)
        
        # Border
        pygame.draw.rect(screen, COLORS['TEXT_WHITE'], bg_rect, 2)
        
        # Label
        label_surface = self.fonts["ui"].render(f"{label}:", True, COLORS['TEXT_WHITE'])
        screen.blit(label_surface, (x, y))
    
    def _render_approach_sequence(self, screen):
        """Render approach sequence"""
        approach_text = f"Angel {self.angel_name} Detected!"
        text_surface = self.fonts["title"].render(approach_text, True, COLORS['WARNING_ORANGE'])
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(text_surface, text_rect)
    
    def _render_victory_sequence(self, screen):
        """Render victory sequence"""
        victory_text = "ANGEL DEFEATED!"
        text_surface = self.fonts["title"].render(victory_text, True, COLORS['SUCCESS_GREEN'])
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(text_surface, text_rect)
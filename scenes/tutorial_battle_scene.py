"""
===============================
TUTORIAL BATTLE SCENE
===============================
First combat simulation tutorial with correct class name
"""

import pygame
import math
import random
from entities.player import Player
from entities.angel import Angel
from ui.hud import HUD
from ui.status_popup import StatusManager
from input.mouse_controller import MouseController
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT

class TutorialBattleScene:
    """
    TUTORIAL BATTLE SCENE CLASS
    First combat simulation tutorial
    """
    
    def __init__(self, game_manager, scene_manager, angel_name="Tutorial Angel"):
        """Initialize tutorial battle"""
        self.game_manager = game_manager
        self.scene_manager = scene_manager
        self.angel_name = angel_name
        
        print(f"🎓 Initializing Tutorial Battle Scene against {angel_name}")
        
        # === PLAYER INITIALIZATION ===
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        # === MOUSE CONTROLLER (COMBAT MODE) ===
        self.mouse_controller = MouseController(game_manager)
        self.mouse_controller.set_combat_mode(True)
        
        # === TUTORIAL ANGEL ===
        self.angel = Angel(angel_name, SCREEN_WIDTH // 2, 200)
        self.angel.hp = 100  # Weaker for tutorial
        
        # === UI SYSTEMS ===
        self.hud = HUD(game_manager)
        self.status_manager = StatusManager()
        
        # === TUTORIAL STATE ===
        self.tutorial_active = True
        self.tutorial_step = 0
        self.battle_active = False
        
        # === COMBAT STATE ===
        self.player_hp = 100
        self.angel_hp = 100
        self.tutorial_complete = False
        
        # === TUTORIAL STEPS ===
        self.tutorial_steps = [
            {
                "title": "EVA Unit-01 Startup",
                "instruction": "Welcome to EVA combat simulation. Systems are initializing...",
                "action": None
            },
            {
                "title": "Movement Tutorial", 
                "instruction": "Use WASD keys to move your EVA unit around the battlefield.",
                "action": "move"
            },
            {
                "title": "Attack Tutorial",
                "instruction": "Left click to attack toward your mouse cursor. Try attacking now!",
                "action": "attack"
            },
            {
                "title": "Parry Tutorial",
                "instruction": "Right click to parry incoming attacks. This reduces damage significantly.",
                "action": "parry"
            },
            {
                "title": "Combat Ready",
                "instruction": "Tutorial complete! Now engage the simulated Angel threat!",
                "action": "combat"
            }
        ]
        
        # === ATTACK EFFECTS ===
        self.attack_effects = []
        self.parry_active = False
        self.parry_timer = 0
        
        # === AUDIO ===
        self.game_manager.audio_manager.play_music("tutorial_battle")
        
        # === INITIAL MESSAGES ===
        self.status_manager.show_status("EVA Unit-01 Combat Simulation - Tutorial Mode", "info", 4.0)
        
        print("✅ Tutorial battle initialized successfully")
    
    def handle_event(self, event):
        """Handle tutorial battle events"""
        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.tutorial_active:
                current_step = self.tutorial_steps[self.tutorial_step]
                if current_step["action"] not in ["move", "attack", "parry"]:
                    self._advance_tutorial()
                    return
            else:
                self.mouse_controller.handle_event(event, self)
        
        # Handle other mouse events when not in tutorial dialogue
        if not (self.tutorial_active and self.tutorial_steps[self.tutorial_step]["action"] is None):
            self.mouse_controller.handle_event(event, self)
        
        # Handle keyboard events
        if event.type == pygame.KEYDOWN:
            if self.tutorial_active:
                if event.key == pygame.K_SPACE:
                    current_step = self.tutorial_steps[self.tutorial_step]
                    if current_step["action"] not in ["move", "attack", "parry"]:
                        self._advance_tutorial()
            else:
                if event.key == pygame.K_ESCAPE:
                    self._end_tutorial()
    
    def _advance_tutorial(self):
        """Advance to next tutorial step"""
        if self.tutorial_step < len(self.tutorial_steps) - 1:
            self.tutorial_step += 1
            
            current_step = self.tutorial_steps[self.tutorial_step]
            self.status_manager.show_status(current_step["instruction"], "info", 5.0)
            
            if current_step["action"] == "combat":
                self.tutorial_active = False
                self.battle_active = True
                self.status_manager.show_status("Angel simulation activated! Engage target!", "warning", 3.0)
    
    def player_attack(self, target_pos):
        """Handle player attack (tutorial version)"""
        # Calculate attack direction
        dx = target_pos[0] - self.player.x
        dy = target_pos[1] - self.player.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Create attack effect
            attack_effect = {
                'start_pos': (self.player.x, self.player.y),
                'direction': (dx, dy),
                'distance': 0,
                'max_distance': min(250, distance),
                'timer': 0.4,
                'type': 'slash'
            }
            self.attack_effects.append(attack_effect)
            
            # Tutorial feedback
            if self.tutorial_active:
                current_step = self.tutorial_steps[self.tutorial_step]
                if current_step["action"] == "attack":
                    self.status_manager.show_status("Good! Attack executed successfully!", "success", 2.0)
                    self._advance_tutorial()
            
            # Combat damage
            elif self.battle_active and distance <= 180:
                damage = 30
                self.angel_hp -= damage
                self.status_manager.show_status(f"Hit! Angel takes {damage} damage!", "success", 2.0)
                
                if self.angel_hp <= 0:
                    self._tutorial_victory()
    
    def player_parry(self):
        """Handle player parry (tutorial version)"""
        self.parry_active = True
        self.parry_timer = 1.2
        
        # Tutorial feedback
        if self.tutorial_active:
            current_step = self.tutorial_steps[self.tutorial_step]
            if current_step["action"] == "parry":
                self.status_manager.show_status("Perfect! Parry stance activated!", "success", 2.0)
                self._advance_tutorial()
        else:
            self.status_manager.show_status("Parrying - incoming damage reduced!", "info", 1.5)
    
    def _tutorial_victory(self):
        """Handle tutorial completion"""
        self.battle_active = False
        self.tutorial_complete = True
        
        # Mark tutorial as complete in scene manager
        self.scene_manager.complete_tutorial()
        
        self.status_manager.show_status("Tutorial Complete! Angel simulation defeated!", "success", 4.0)
        self.status_manager.show_status("Combat training successful - returning to NERV", "info", 6.0)
        
        # Experience reward
        exp_gain = 50
        self.game_manager.get_player_data().gain_experience(exp_gain)
        self.status_manager.show_experience_gain(exp_gain)
        
        # Sync ratio improvement
        player_data = self.game_manager.get_player_data()
        player_data.sync_ratio = min(100, player_data.sync_ratio + 10)
        
        # Return to hub after delay
        pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
    
    def _end_tutorial(self):
        """End tutorial and return to hub"""
        self.status_manager.show_status("Tutorial ended - returning to NERV HQ", "info", 2.0)
        self.scene_manager.change_scene("hub")
    
    def update(self, dt):
        """Update tutorial battle"""
        # === UPDATE MOUSE CONTROLLER ===
        self.mouse_controller.update(dt)
        
        # === UPDATE PLAYER ===
        keys_pressed = pygame.key.get_pressed()
        
        # Tutorial movement check
        if self.tutorial_active:
            current_step = self.tutorial_steps[self.tutorial_step]
            if current_step["action"] == "move":
                if any(keys_pressed[key] for key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]):
                    self.status_manager.show_status("Excellent! Movement systems responding!", "success", 2.0)
                    self._advance_tutorial()
        
        self.player.handle_input(keys_pressed)
        self.player.update(dt)
        
        # === UPDATE ANGEL ===
        if self.battle_active:
            self.angel.update(dt)
            
            # Simple Angel AI for tutorial
            if random.random() < 0.01:  # 1% chance per frame
                self._angel_tutorial_attack()
        
        # === UPDATE ATTACK EFFECTS ===
        for effect in self.attack_effects[:]:
            effect['timer'] -= dt
            effect['distance'] += 400 * dt
            
            if effect['timer'] <= 0 or effect['distance'] >= effect['max_distance']:
                self.attack_effects.remove(effect)
        
        # === UPDATE PARRY ===
        if self.parry_active:
            self.parry_timer -= dt
            if self.parry_timer <= 0:
                self.parry_active = False
        
        # === UPDATE UI ===
        self.status_manager.update(dt)
        
        # === CHECK FOR SCENE TRANSITION ===
        for event in pygame.event.get([pygame.USEREVENT + 1]):
            if event.type == pygame.USEREVENT + 1:
                self.scene_manager.change_scene("hub")
    
    def _angel_tutorial_attack(self):
        """Angel attacks in tutorial (weaker)"""
        damage = 10
        
        if self.parry_active:
            damage = 3
            self.status_manager.show_status(f"Parried! Damage reduced to {damage}!", "success", 2.0)
        else:
            self.status_manager.show_status(f"Angel attack! {damage} damage taken!", "warning", 2.0)
        
        self.player_hp -= damage
        
        if self.player_hp <= 0:
            self._tutorial_defeat()
    
    def _tutorial_defeat(self):
        """Handle tutorial defeat"""
        self.battle_active = False
        self.status_manager.show_status("Simulation ended - practice more to improve!", "warning", 3.0)
        
        # Reset for retry
        self.player_hp = 100
        self.angel_hp = 100
        pygame.time.set_timer(pygame.USEREVENT + 2, 3000)
    
    def render(self, screen):
        """Render tutorial battle"""
        # === SIMULATION BACKGROUND ===
        self._render_simulation_background(screen)
        
        # === ENTITIES ===
        if self.battle_active or self.tutorial_complete:
            self.angel.render(screen)
        
        self.player.render(screen)
        
        # === EFFECTS ===
        for effect in self.attack_effects:
            self._render_attack_effect(screen, effect)
        
        if self.parry_active:
            self._render_parry_effect(screen)
        
        # === TUTORIAL OVERLAY ===
        if self.tutorial_active:
            self._render_tutorial_overlay(screen)
        
        # === HEALTH BARS ===
        self._render_health_bars(screen)
        
        # === UI ===
        self.hud.render(screen)
        self.status_manager.render(screen)
        
        # === MOUSE UI ===
        self.mouse_controller.render_mouse_ui(screen)
        
        # === SCENE INFO ===
        self._render_scene_info(screen)
    
    def _render_simulation_background(self, screen):
        """Render simulation chamber background"""
        # === BASE BACKGROUND ===
        screen.fill((20, 40, 60))
        
        # === SIMULATION GRID ===
        grid_color = (40, 80, 120)
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(screen, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(screen, grid_color, (0, y), (SCREEN_WIDTH, y), 1)
        
        # === SIMULATION INDICATORS ===
        indicator_size = 20
        pygame.draw.rect(screen, COLORS['TERMINAL_GREEN'], 
                        (10, 10, indicator_size, indicator_size))
        pygame.draw.rect(screen, COLORS['TERMINAL_GREEN'], 
                        (SCREEN_WIDTH - indicator_size - 10, 10, indicator_size, indicator_size))
        pygame.draw.rect(screen, COLORS['TERMINAL_GREEN'], 
                        (10, SCREEN_HEIGHT - indicator_size - 10, indicator_size, indicator_size))
        pygame.draw.rect(screen, COLORS['TERMINAL_GREEN'], 
                        (SCREEN_WIDTH - indicator_size - 10, SCREEN_HEIGHT - indicator_size - 10, indicator_size, indicator_size))
    
    def _render_tutorial_overlay(self, screen):
        """Render tutorial instruction overlay"""
        current_step = self.tutorial_steps[self.tutorial_step]
        
        # === TUTORIAL PANEL ===
        panel_height = 120
        panel_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, panel_height)
        
        # Panel background
        panel_surface = pygame.Surface((panel_rect.width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((20, 20, 40, 200))
        screen.blit(panel_surface, panel_rect.topleft)
        
        # Panel border
        pygame.draw.rect(screen, COLORS['SCHOOL_YELLOW'], panel_rect, 3)
        
        # === TITLE ===
        title_font = pygame.font.Font(None, 24)
        title_text = title_font.render(current_step["title"], True, COLORS['SCHOOL_YELLOW'])
        title_rect = title_text.get_rect(center=(panel_rect.centerx, panel_rect.top + 20))
        screen.blit(title_text, title_rect)
        
        # === INSTRUCTION ===
        instruction_font = pygame.font.Font(None, 18)
        instruction_lines = self._wrap_text(current_step["instruction"], instruction_font, panel_rect.width - 20)
        
        for i, line in enumerate(instruction_lines):
            line_surface = instruction_font.render(line, True, COLORS['TEXT_WHITE'])
            line_rect = line_surface.get_rect(center=(panel_rect.centerx, panel_rect.top + 45 + i * 20))
            screen.blit(line_surface, line_rect)
        
        # === PROGRESS ===
        progress_text = f"Step {self.tutorial_step + 1}/{len(self.tutorial_steps)}"
        progress_surface = pygame.font.Font(None, 16).render(progress_text, True, COLORS['UI_GRAY'])
        screen.blit(progress_surface, (panel_rect.right - 100, panel_rect.bottom + 5))
        
        # === MANUAL ADVANCEMENT PROMPT ===
        if current_step["action"] not in ["move", "attack", "parry", "combat"]:
            import math
            blink_alpha = int(255 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.005)))
            
            prompt_font = pygame.font.Font(None, 16)
            prompt_text = "Press SPACEBAR or LEFT CLICK to continue..."
            
            prompt_surface = pygame.Surface(prompt_font.size(prompt_text), pygame.SRCALPHA)
            prompt_rendered = prompt_font.render(prompt_text, True, COLORS['SCHOOL_YELLOW'])
            prompt_surface.blit(prompt_rendered, (0, 0))
            prompt_surface.set_alpha(blink_alpha)
            
            prompt_rect = prompt_surface.get_rect(center=(panel_rect.centerx, panel_rect.bottom + 20))
            screen.blit(prompt_surface, prompt_rect)
    
    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit width"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
    
    def _render_attack_effect(self, screen, effect):
        """Render attack effect"""
        start_x, start_y = effect['start_pos']
        dx, dy = effect['direction']
        
        current_x = start_x + dx * effect['distance']
        current_y = start_y + dy * effect['distance']
        
        # Attack line with glow
        end_x = current_x + dx * 40
        end_y = current_y + dy * 40
        
        pygame.draw.line(screen, (150, 255, 150), 
                        (int(current_x), int(current_y)), 
                        (int(end_x), int(end_y)), 6)
        pygame.draw.line(screen, COLORS['TERMINAL_GREEN'], 
                        (int(current_x), int(current_y)), 
                        (int(end_x), int(end_y)), 3)
    
    def _render_parry_effect(self, screen):
        """Render parry shield effect"""
        shield_radius = 35 + int(8 * math.sin(self.parry_timer * 12))
        
        pygame.draw.circle(screen, (*COLORS['HANGAR_BLUE'], 120), 
                         (int(self.player.x), int(self.player.y)), shield_radius)
        pygame.draw.circle(screen, COLORS['HANGAR_BLUE'], 
                         (int(self.player.x), int(self.player.y)), shield_radius, 3)
    
    def _render_health_bars(self, screen):
        """Render health bars"""
        # Player health
        player_bar_rect = pygame.Rect(50, SCREEN_HEIGHT - 80, 200, 20)
        pygame.draw.rect(screen, (40, 40, 40), player_bar_rect)
        pygame.draw.rect(screen, COLORS['HANGAR_BLUE'], player_bar_rect, 2)
        
        player_health_width = int((self.player_hp / 100) * 196)
        if player_health_width > 0:
            health_rect = pygame.Rect(52, SCREEN_HEIGHT - 78, player_health_width, 16)
            pygame.draw.rect(screen, COLORS['TERMINAL_GREEN'], health_rect)
        
        player_text = f"EVA Unit-01: {self.player_hp}/100"
        player_surface = pygame.font.Font(None, 18).render(player_text, True, COLORS['TEXT_WHITE'])
        screen.blit(player_surface, (50, SCREEN_HEIGHT - 100))
        
        # Angel health (if in combat)
        if self.battle_active:
            angel_bar_rect = pygame.Rect(SCREEN_WIDTH - 250, 30, 200, 20)
            pygame.draw.rect(screen, (40, 40, 40), angel_bar_rect)
            pygame.draw.rect(screen, COLORS['NERV_RED'], angel_bar_rect, 2)
            
            angel_health_width = int((self.angel_hp / 100) * 196)
            if angel_health_width > 0:
                angel_health_rect = pygame.Rect(SCREEN_WIDTH - 248, 32, angel_health_width, 16)
                pygame.draw.rect(screen, COLORS['NERV_RED'], angel_health_rect)
            
            angel_text = f"Tutorial Angel: {max(0, self.angel_hp)}/100"
            angel_surface = pygame.font.Font(None, 18).render(angel_text, True, COLORS['TEXT_WHITE'])
            screen.blit(angel_surface, (SCREEN_WIDTH - 250, 10))
    
    def _render_scene_info(self, screen):
        """Render scene information"""
        if self.tutorial_active:
            return
        
        # Title
        title_font = pygame.font.Font(None, 28)
        title_text = title_font.render("COMBAT SIMULATION", True, COLORS['NERV_RED'])
        screen.blit(title_text, (20, 20))
        
        # Controls
        controls_font = pygame.font.Font(None, 12)
        controls_text = "WASD: Move | Left Click: Attack | Right Click: Parry | ESC: End Simulation"
        controls_surface = controls_font.render(controls_text, True, COLORS['UI_GRAY'])
        screen.blit(controls_surface, (20, SCREEN_HEIGHT - 25))
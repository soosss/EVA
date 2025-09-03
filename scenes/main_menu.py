"""
===============================
MAIN MENU SCENE - COMPLETE
===============================
Enhanced main menu with all features
"""

import pygame
import math

# Add proper imports for screen dimensions
try:
    from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    from config import COLORS
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

class MainMenuScene:
    """Complete enhanced main menu scene"""
    
    def __init__(self, game_manager, scene_manager):
        """Initialize main menu"""
        self.game_manager = game_manager
        self.scene_manager = scene_manager
        
        # Menu state
        self.selected_option = 0
        self.animation_timer = 0
        self.mouse_pos = (0, 0)
        
        # Menu options
        self.menu_options = [
            {"text": "New Game", "action": "new_game", "icon": "🎮"},
            {"text": "Continue", "action": "continue", "icon": "💾"},
            {"text": "Art Gallery", "action": "art_gallery", "icon": "🎨"},
            {"text": "Settings", "action": "settings", "icon": "⚙️"},
            {"text": "Exit", "action": "exit", "icon": "🚪"}
        ]
        
        # Layout
        self.menu_x = SCREEN_WIDTH // 2
        self.menu_y = SCREEN_HEIGHT // 2
        self.option_spacing = 60
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.menu_font = pygame.font.Font(None, 32)
        self.subtitle_font = pygame.font.Font(None, 20)
        
        # Background
        self.background = self._create_background()
        
        print("🏠 Main Menu Scene initialized")
    
    def _create_background(self):
        """Create animated background"""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            gradient_factor = y / SCREEN_HEIGHT
            color = (
                int(20 + gradient_factor * 20),
                int(20 + gradient_factor * 30),
                int(40 + gradient_factor * 40)
            )
            pygame.draw.line(background, color, (0, y), (SCREEN_WIDTH, y))
        
        return background
    
    def handle_event(self, event):
        """Handle main menu events"""
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self._update_selection_from_mouse()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._execute_selected_option()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._execute_selected_option()
            elif event.key == pygame.K_ESCAPE:
                self._execute_action("exit")
    
    def _update_selection_from_mouse(self):
        """Update selection based on mouse position"""
        for i, option in enumerate(self.menu_options):
            option_y = self.menu_y + (i - len(self.menu_options) // 2) * self.option_spacing
            option_rect = pygame.Rect(self.menu_x - 100, option_y - 20, 200, 40)
            
            if option_rect.collidepoint(self.mouse_pos):
                self.selected_option = i
                break
    
    def _execute_selected_option(self):
        """Execute the currently selected option"""
        option = self.menu_options[self.selected_option]
        self._execute_action(option["action"])
    
    def _execute_action(self, action):
        """Execute menu action"""
        if action == "new_game":
            self.scene_manager.change_scene("bedroom")
        elif action == "continue":
            # Check for save files
            if self.game_manager.has_save_files():
                self.game_manager.load_game()
            else:
                # No save files, start new game
                self.scene_manager.change_scene("bedroom")
        elif action == "art_gallery":
            self.scene_manager.change_scene("art_gallery")
        elif action == "settings":
            self.scene_manager.change_scene("settings")
        elif action == "exit":
            pygame.quit()
            exit()
    
    def update(self, dt):
        """Update main menu"""
        self.animation_timer += dt
    
    def render(self, screen):
        """Render main menu"""
        # Background
        screen.blit(self.background, (0, 0))
        
        # Animated background elements
        self._render_animated_background(screen)
        
        # Title
        title_text = "EVANGELION"
        title_pulse = 1.0 + 0.1 * math.sin(self.animation_timer * 2)
        title_font = pygame.font.Font(None, int(48 * title_pulse))
        title_surface = title_font.render(title_text, True, COLORS['NERV_RED'])
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "Visual Novel Experience"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, COLORS['UI_GRAY'])
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 180))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Menu options
        for i, option in enumerate(self.menu_options):
            self._render_menu_option(screen, i, option)
        
        # Version info
        version_text = "Version 1.0.0 - Enhanced Edition"
        version_surface = pygame.font.Font(None, 16).render(version_text, True, COLORS['UI_GRAY'])
        screen.blit(version_surface, (20, SCREEN_HEIGHT - 25))
    
    def _render_animated_background(self, screen):
        """Render animated background elements"""
        # Floating particles
        for i in range(10):
            x = (self.animation_timer * 20 + i * 80) % (SCREEN_WIDTH + 50) - 25
            y = 100 + math.sin(self.animation_timer + i) * 50
            particle_rect = pygame.Rect(x, y, 4, 4)
            pygame.draw.rect(screen, COLORS['TERMINAL_GREEN'], particle_rect)
    
    def _render_menu_option(self, screen, index, option):
        """Render individual menu option"""
        is_selected = index == self.selected_option
        
        # Position
        option_y = self.menu_y + (index - len(self.menu_options) // 2) * self.option_spacing
        
        # Colors and effects
        if is_selected:
            color = COLORS['SCHOOL_YELLOW']
            scale = 1.1 + 0.05 * math.sin(self.animation_timer * 8)
        else:
            color = COLORS['TEXT_WHITE']
            scale = 1.0
        
        # Render option text
        font = pygame.font.Font(None, int(32 * scale))
        option_text = f"{option['icon']} {option['text']}"
        text_surface = font.render(option_text, True, color)
        text_rect = text_surface.get_rect(center=(self.menu_x, option_y))
        
        # Selection highlight
        if is_selected:
            highlight_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(screen, (*COLORS['SCHOOL_YELLOW'], 50), highlight_rect)
            pygame.draw.rect(screen, COLORS['SCHOOL_YELLOW'], highlight_rect, 2)
        
        screen.blit(text_surface, text_rect)


# Backward compatibility
class MainMenuScene(MainMenuScene):
    """Ensure proper class name"""
    pass
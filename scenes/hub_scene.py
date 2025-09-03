"""
===============================
HUB SCENE - COMPLETE
===============================
Central hub for navigation and management
"""

import pygame

# Add proper imports for screen dimensions
try:
    from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    from config import COLORS
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

class HubScene:
    """Complete hub scene for game navigation"""
    
    def __init__(self, game_manager, scene_manager):
        """Initialize hub scene"""
        self.game_manager = game_manager
        self.scene_manager = scene_manager
        
        # Hub state
        self.selected_area = 0
        self.mouse_pos = (0, 0)
        
        # Available areas
        self.areas = [
            {"name": "Bedroom", "scene": "bedroom", "icon": "🏠", "pos": (150, 200)},
            {"name": "School", "scene": "town", "icon": "🏫", "pos": (400, 150)},
            {"name": "NERV HQ", "scene": "nerv_arrival", "icon": "🏢", "pos": (600, 300)},
            {"name": "Battle", "scene": "action_battle", "icon": "⚔️", "pos": (300, 400)},
            {"name": "Art Gallery", "scene": "art_gallery", "icon": "🎨", "pos": (500, 450)}
        ]
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.area_font = pygame.font.Font(None, 24)
        
        print("🏭 Hub Scene initialized")
    
    def handle_event(self, event):
        """Handle hub events"""
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self._update_selection_from_mouse()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._navigate_to_selected_area()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._navigate_to_selected_area()
            elif event.key == pygame.K_ESCAPE:
                self.scene_manager.change_scene("main_menu")
            elif event.key == pygame.K_TAB:
                self.selected_area = (self.selected_area + 1) % len(self.areas)
    
    def _update_selection_from_mouse(self):
        """Update selection based on mouse position"""
        for i, area in enumerate(self.areas):
            area_rect = pygame.Rect(area["pos"][0] - 40, area["pos"][1] - 40, 80, 80)
            if area_rect.collidepoint(self.mouse_pos):
                self.selected_area = i
                break
    
    def _navigate_to_selected_area(self):
        """Navigate to selected area"""
        area = self.areas[self.selected_area]
        if area["scene"] == "action_battle":
            self.scene_manager.change_scene(area["scene"], angel_name="Sachiel")
        else:
            self.scene_manager.change_scene(area["scene"])
    
    def update(self, dt):
        """Update hub scene"""
        pass
    
    def render(self, screen):
        """Render hub scene"""
        # Background
        screen.fill((30, 30, 50))
        
        # Title
        title_text = "TOKYO-3 HUB"
        title_surface = self.title_font.render(title_text, True, COLORS['NERV_RED'])
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)
        
        # Areas
        for i, area in enumerate(self.areas):
            self._render_area(screen, i, area)
        
        # Instructions
        instruction_text = "Click or press ENTER to navigate | ESC: Main Menu"
        instruction_surface = pygame.font.Font(None, 16).render(instruction_text, True, COLORS['UI_GRAY'])
        screen.blit(instruction_surface, (20, SCREEN_HEIGHT - 25))
    
    def _render_area(self, screen, index, area):
        """Render individual area"""
        is_selected = index == self.selected_area
        
        # Area circle
        color = COLORS['SCHOOL_YELLOW'] if is_selected else COLORS['UI_GRAY']
        pygame.draw.circle(screen, color, area["pos"], 40)
        pygame.draw.circle(screen, COLORS['TEXT_WHITE'], area["pos"], 40, 3)
        
        # Area icon
        icon_font = pygame.font.Font(None, 48)
        icon_surface = icon_font.render(area["icon"], True, COLORS['TEXT_WHITE'])
        icon_rect = icon_surface.get_rect(center=area["pos"])
        screen.blit(icon_surface, icon_rect)
        
        # Area name
        name_surface = self.area_font.render(area["name"], True, color)
        name_rect = name_surface.get_rect(center=(area["pos"][0], area["pos"][1] + 60))
        screen.blit(name_surface, name_rect)
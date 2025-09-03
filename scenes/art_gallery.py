"""
===============================
ART GALLERY - WORKING VERSION
===============================
Simplified but functional art gallery
"""

import pygame
import os

# Import screen dimensions
try:
    from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    from config import COLORS
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

class ArtGallery:
    """Simplified working Art Gallery"""
    
    def __init__(self, game_manager, scene_manager):
        """Initialize art gallery"""
        self.game_manager = game_manager
        self.scene_manager = scene_manager
        
        # Basic state
        self.current_category = "characters"
        self.selected_art_index = 0
        self.viewing_mode = "gallery"
        
        # Layout
        self.sidebar_width = 200
        self.mouse_pos = (0, 0)
        
        # Categories
        self.categories = [
            {"id": "characters", "name": "Characters", "icon": "👥"},
            {"id": "angels", "name": "Angels", "icon": "👹"},
            {"id": "eva_units", "name": "EVA Units", "icon": "🤖"},
            {"id": "backgrounds", "name": "Backgrounds", "icon": "🌆"}
        ]
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.category_font = pygame.font.Font(None, 22)
        self.info_font = pygame.font.Font(None, 18)
        
        # Sample art
        self.art_collections = {}
        self._create_sample_collections()
        
        print("🎨 Art Gallery initialized (simplified version)")
    
    def _create_sample_collections(self):
        """Create sample art collections"""
        for category in self.categories:
            self.art_collections[category["id"]] = [
                {
                    "title": f"Sample {category['name']} 1",
                    "description": f"Sample artwork for {category['name']} category",
                    "surface": self._create_sample_surface(category["name"], 1)
                },
                {
                    "title": f"Sample {category['name']} 2", 
                    "description": f"Another sample artwork for {category['name']}",
                    "surface": self._create_sample_surface(category["name"], 2)
                }
            ]
    
    def _create_sample_surface(self, category_name, index):
        """Create a sample art surface"""
        surface = pygame.Surface((300, 200))
        
        # Background gradient
        for y in range(200):
            color_value = int(50 + (y / 200) * 100)
            color = (color_value, color_value, color_value + 20)
            pygame.draw.line(surface, color, (0, y), (300, y))
        
        # Border
        pygame.draw.rect(surface, COLORS['NERV_RED'], surface.get_rect(), 3)
        
        # Title
        font = pygame.font.Font(None, 24)
        title_text = f"{category_name} {index}"
        title_surface = font.render(title_text, True, COLORS['TEXT_WHITE'])
        title_rect = title_surface.get_rect(center=(150, 100))
        surface.blit(title_surface, title_rect)
        
        return surface
    
    def handle_event(self, event):
        """Handle art gallery events"""
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._handle_left_click(event.pos)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scene_manager.change_scene("main_menu")
            elif event.key == pygame.K_LEFT:
                self._navigate_art(-1)
            elif event.key == pygame.K_RIGHT:
                self._navigate_art(1)
            elif event.key == pygame.K_TAB:
                self._next_category()
    
    def _handle_left_click(self, pos):
        """Handle left mouse click"""
        # Check category sidebar
        if pos[0] <= self.sidebar_width:
            self._handle_sidebar_click(pos)
    
    def _handle_sidebar_click(self, pos):
        """Handle clicks on category sidebar"""
        y_offset = 80
        for category in self.categories:
            category_rect = pygame.Rect(10, y_offset, self.sidebar_width - 20, 40)
            if category_rect.collidepoint(pos):
                self.current_category = category["id"]
                self.selected_art_index = 0
                break
            y_offset += 50
    
    def _navigate_art(self, direction):
        """Navigate between artworks"""
        current_collection = self.art_collections.get(self.current_category, [])
        if current_collection:
            new_index = self.selected_art_index + direction
            self.selected_art_index = max(0, min(len(current_collection) - 1, new_index))
    
    def _next_category(self):
        """Switch to next category"""
        current_index = next(i for i, cat in enumerate(self.categories) if cat["id"] == self.current_category)
        next_index = (current_index + 1) % len(self.categories)
        self.current_category = self.categories[next_index]["id"]
        self.selected_art_index = 0
    
    def update(self, dt):
        """Update art gallery"""
        pass
    
    def render(self, screen):
        """Render art gallery"""
        # Background
        screen.fill((20, 20, 30))
        
        # Title
        title_text = self.title_font.render("🎨 EVA ART GALLERY", True, COLORS['NERV_RED'])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(title_text, title_rect)
        
        # Sidebar
        self._render_sidebar(screen)
        
        # Main content
        self._render_main_content(screen)
        
        # Controls
        controls_text = "ESC: Back | ←→: Navigate | TAB: Next Category"
        controls_surface = pygame.font.Font(None, 16).render(controls_text, True, COLORS['UI_GRAY'])
        screen.blit(controls_surface, (20, SCREEN_HEIGHT - 30))
    
    def _render_sidebar(self, screen):
        """Render category sidebar"""
        # Sidebar background
        sidebar_rect = pygame.Rect(0, 60, self.sidebar_width, SCREEN_HEIGHT - 60)
        pygame.draw.rect(screen, (30, 30, 45), sidebar_rect)
        pygame.draw.rect(screen, COLORS['UI_GRAY'], sidebar_rect, 2)
        
        # Categories
        y_offset = 80
        for category in self.categories:
            category_rect = pygame.Rect(10, y_offset, self.sidebar_width - 20, 40)
            
            # Highlight current category
            if category["id"] == self.current_category:
                pygame.draw.rect(screen, COLORS['NERV_RED'], category_rect)
                text_color = COLORS['TEXT_WHITE']
            else:
                pygame.draw.rect(screen, (50, 50, 70), category_rect)
                text_color = COLORS['UI_GRAY']
            
            pygame.draw.rect(screen, COLORS['TEXT_WHITE'], category_rect, 1)
            
            # Category text
            category_text = f"{category['icon']} {category['name']}"
            text_surface = self.category_font.render(category_text, True, text_color)
            text_rect = text_surface.get_rect(left=category_rect.left + 10, centery=category_rect.centery)
            screen.blit(text_surface, text_rect)
            
            y_offset += 50
    
    def _render_main_content(self, screen):
        """Render main content area"""
        content_rect = pygame.Rect(self.sidebar_width + 20, 80, 
                                  SCREEN_WIDTH - self.sidebar_width - 40, 
                                  SCREEN_HEIGHT - 120)
        pygame.draw.rect(screen, (25, 25, 35), content_rect)
        pygame.draw.rect(screen, COLORS['UI_GRAY'], content_rect, 1)
        
        # Get current collection
        current_collection = self.art_collections.get(self.current_category, [])
        
        if not current_collection:
            # Empty message
            empty_text = "No artwork in this category"
            empty_surface = self.info_font.render(empty_text, True, COLORS['UI_GRAY'])
            empty_rect = empty_surface.get_rect(center=content_rect.center)
            screen.blit(empty_surface, empty_rect)
            return
        
        # Show selected artwork
        if 0 <= self.selected_art_index < len(current_collection):
            selected_art = current_collection[self.selected_art_index]
            
            # Art surface
            art_surface = selected_art["surface"]
            art_rect = art_surface.get_rect(center=(content_rect.centerx, content_rect.centery - 40))
            screen.blit(art_surface, art_rect)
            
            # Art info
            title_text = selected_art["title"]
            title_surface = self.info_font.render(title_text, True, COLORS['SCHOOL_YELLOW'])
            title_rect = title_surface.get_rect(center=(content_rect.centerx, art_rect.bottom + 20))
            screen.blit(title_surface, title_rect)
            
            desc_text = selected_art["description"]
            desc_surface = pygame.font.Font(None, 14).render(desc_text, True, COLORS['UI_GRAY'])
            desc_rect = desc_surface.get_rect(center=(content_rect.centerx, title_rect.bottom + 15))
            screen.blit(desc_surface, desc_rect)
            
            # Navigation info
            nav_text = f"{self.selected_art_index + 1} / {len(current_collection)}"
            nav_surface = pygame.font.Font(None, 16).render(nav_text, True, COLORS['UI_GRAY'])
            nav_rect = nav_surface.get_rect(center=(content_rect.centerx, desc_rect.bottom + 20))
            screen.blit(nav_surface, nav_rect)
"""
ENHANCED HUD - ALIGNMENT FIXED
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

class EnhancedHUD:
    """Enhanced HUD with proper alignment"""
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        
        # === FIXED LAYOUT DIMENSIONS ===
        self.hud_width = 220  # Fixed width
        self.hud_height = SCREEN_HEIGHT - 40  # Leave margin
        self.hud_x = SCREEN_WIDTH - self.hud_width - 10  # Right side with margin
        self.hud_y = 20  # Top margin
        
        # === SECTION LAYOUT ===
        self.section_height = (self.hud_height - 60) // 6  # 6 sections
        self.section_spacing = 5
        
        # === HUD SECTIONS (PROPERLY ALIGNED) ===
        self.sections = [
            {
                "name": "pilot_status", "title": "PILOT STATUS", "icon": "👤",
                "y_offset": 0, "height": self.section_height,
                "color": COLORS['EVA_PURPLE'], "expanded": True
            },
            {
                "name": "eva_status", "title": "EVA STATUS", "icon": "🤖", 
                "y_offset": self.section_height + self.section_spacing,
                "height": self.section_height, "color": COLORS['NERV_RED'], "expanded": True
            },
            {
                "name": "relationships", "title": "RELATIONSHIPS", "icon": "💕",
                "y_offset": 2 * (self.section_height + self.section_spacing),
                "height": self.section_height, "color": COLORS['SCHOOL_YELLOW'], "expanded": True
            },
            {
                "name": "objectives", "title": "OBJECTIVES", "icon": "🎯",
                "y_offset": 3 * (self.section_height + self.section_spacing),
                "height": self.section_height, "color": COLORS['TERMINAL_GREEN'], "expanded": True
            },
            {
                "name": "location", "title": "LOCATION", "icon": "📍",
                "y_offset": 4 * (self.section_height + self.section_spacing),
                "height": self.section_height, "color": COLORS['HANGAR_BLUE'], "expanded": True
            },
            {
                "name": "system", "title": "SYSTEM", "icon": "⚙️",
                "y_offset": 5 * (self.section_height + self.section_spacing),
                "height": self.section_height, "color": COLORS['UI_GRAY'], "expanded": False
            }
        ]
        
        # === FONTS ===
        self.title_font = pygame.font.Font(None, 16)
        self.section_font = pygame.font.Font(None, 14)
        self.data_font = pygame.font.Font(None, 12)
        self.small_font = pygame.font.Font(None, 10)
        
        # === HOVER SYSTEM (FIXED POSITIONING) ===
        self.hover_target = None
        self.hover_timer = 0
        self.hover_delay = 0.3
        self.tooltip_surface = None
        self.mouse_pos = (0, 0)
        
        # === ANIMATIONS ===
        self.animation_timer = 0
        self.pulse_sections = set()
        
        print("📊 Enhanced HUD initialized with fixed alignment")
    
    def update(self, dt):
        """Update HUD with proper alignment"""
        self.animation_timer += dt
        
        # Update hover system
        if self.hover_target:
            self.hover_timer += dt
            if self.hover_timer >= self.hover_delay:
                self._create_tooltip()
        else:
            self.hover_timer = 0
            self.tooltip_surface = None
    
    def handle_event(self, event):
        """Handle HUD events with proper hit detection"""
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self._update_hover_target(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._handle_section_click(event.pos)
    
    def _update_hover_target(self, mouse_pos):
        """Update hover target with corrected hit detection"""
        old_target = self.hover_target
        self.hover_target = None
        
        # Check if mouse is over HUD area
        hud_rect = pygame.Rect(self.hud_x, self.hud_y, self.hud_width, self.hud_height)
        if not hud_rect.collidepoint(mouse_pos):
            if old_target != self.hover_target:
                self.hover_timer = 0
            return
        
        # Check sections with corrected coordinates
        for section in self.sections:
            section_rect = pygame.Rect(
                self.hud_x + 5,  # Account for HUD padding
                self.hud_y + 30 + section["y_offset"],  # Account for title and padding
                self.hud_width - 10,  # Account for padding
                section["height"]
            )
            
            if section_rect.collidepoint(mouse_pos):
                self.hover_target = section["name"]
                break
        
        # Reset hover timer if target changed
        if old_target != self.hover_target:
            self.hover_timer = 0
    
    def _handle_section_click(self, pos):
        """Handle section clicks with corrected hit detection"""
        for section in self.sections:
            section_rect = pygame.Rect(
                self.hud_x + 5,
                self.hud_y + 30 + section["y_offset"],
                self.hud_width - 10,
                section["height"]
            )
            
            if section_rect.collidepoint(pos):
                section["expanded"] = not section["expanded"]
                break
    
    def _create_tooltip(self):
        """Create tooltip with proper positioning"""
        if not self.hover_target:
            return
        
        section = next((s for s in self.sections if s["name"] == self.hover_target), None)
        if not section:
            return
        
        # Get tooltip text
        tooltip_texts = {
            "pilot_status": ["Health, Sync Ratio, Stress Level", "Click to toggle details"],
            "eva_status": ["EVA Unit condition and specs", "Shows current EVA data"],
            "relationships": ["Character relationship levels", "Track social connections"],
            "objectives": ["Current goals and missions", "Story progress tracking"],
            "location": ["Current scene and area", "Navigation information"],
            "system": ["Game settings and info", "System controls"]
        }
        
        texts = tooltip_texts.get(self.hover_target, ["Information", "Details"])
        
        # Create tooltip surface
        tooltip_width = 200
        tooltip_height = len(texts) * 16 + 20
        self.tooltip_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
        
        # Tooltip background
        pygame.draw.rect(self.tooltip_surface, (20, 20, 40, 240), self.tooltip_surface.get_rect())
        pygame.draw.rect(self.tooltip_surface, section["color"], self.tooltip_surface.get_rect(), 2)
        
        # Tooltip text
        for i, text in enumerate(texts):
            color = COLORS['TEXT_WHITE'] if i == 0 else COLORS['UI_GRAY']
            text_surface = self.data_font.render(text, True, color)
            self.tooltip_surface.blit(text_surface, (10, 10 + i * 16))
    
    def render(self, screen):
        """Render HUD with proper alignment"""
        # === MAIN HUD BACKGROUND ===
        hud_rect = pygame.Rect(self.hud_x, self.hud_y, self.hud_width, self.hud_height)
        
        # Background with enhanced visual separation
        hud_surface = pygame.Surface((self.hud_width, self.hud_height), pygame.SRCALPHA)
        # More opaque background to clearly separate from game area
        pygame.draw.rect(hud_surface, (20, 20, 35, 240), hud_surface.get_rect())
        # Double border for better separation
        pygame.draw.rect(hud_surface, COLORS['NERV_RED'], hud_surface.get_rect(), 3)
        pygame.draw.rect(hud_surface, (100, 100, 120), hud_surface.get_rect(), 1)
        screen.blit(hud_surface, (self.hud_x, self.hud_y))
        
        # === HUD TITLE ===
        title_text = "NERV HUD"
        title_surface = self.title_font.render(title_text, True, COLORS['NERV_RED'])
        title_rect = title_surface.get_rect(center=(self.hud_x + self.hud_width // 2, self.hud_y + 15))
        screen.blit(title_surface, title_rect)
        
        # === RENDER SECTIONS ===
        for section in self.sections:
            self._render_section(screen, section)
        
        # === RENDER TOOLTIP ===
        if self.tooltip_surface and self.hover_timer >= self.hover_delay:
            # Position tooltip to the left of HUD
            tooltip_x = self.hud_x - self.tooltip_surface.get_width() - 10
            tooltip_y = self.mouse_pos[1] - self.tooltip_surface.get_height() // 2
            
            # Keep tooltip on screen
            tooltip_y = max(10, min(tooltip_y, SCREEN_HEIGHT - self.tooltip_surface.get_height() - 10))
            
            screen.blit(self.tooltip_surface, (tooltip_x, tooltip_y))
    
    def _render_section(self, screen, section):
        """Render individual section with proper alignment"""
        section_x = self.hud_x + 5
        section_y = self.hud_y + 30 + section["y_offset"]
        section_w = self.hud_width - 10
        section_h = section["height"]
        
        # Section background
        section_rect = pygame.Rect(section_x, section_y, section_w, section_h)
        
        # Hover highlight
        if self.hover_target == section["name"]:
            pygame.draw.rect(screen, (*section["color"], 60), section_rect)
        
        pygame.draw.rect(screen, section["color"], section_rect, 1)
        
        # Section header
        header_text = f"{section['icon']} {section['title']}"
        header_surface = self.section_font.render(header_text, True, section["color"])
        screen.blit(header_surface, (section_x + 5, section_y + 3))
        
        # Section content (only if expanded)
        if section["expanded"]:
            content_y = section_y + 20
            self._render_section_content(screen, section, section_x + 5, content_y, section_w - 10)
    
    def _render_section_content(self, screen, section, x, y, width):
        """Render section content"""
        if section["name"] == "pilot_status":
            self._render_pilot_status(screen, x, y)
        elif section["name"] == "eva_status":
            self._render_eva_status(screen, x, y)
        elif section["name"] == "relationships":
            self._render_relationships(screen, x, y)
        elif section["name"] == "objectives":
            self._render_objectives(screen, x, y)
        elif section["name"] == "location":
            self._render_location(screen, x, y)
        elif section["name"] == "system":
            self._render_system(screen, x, y)
    
    def _render_pilot_status(self, screen, x, y):
        """Render pilot status with proper spacing"""
        health = self.game_manager.get_player_health()
        sync_ratio = self.game_manager.get_sync_ratio()
        stress = self.game_manager.get_stress_level()
        
        status_data = [
            f"Health: {health}%",
            f"Sync: {sync_ratio:.1f}%", 
            f"Stress: {stress}%"
        ]
        
        for i, text in enumerate(status_data):
            color = COLORS['SUCCESS_GREEN'] if i == 0 else COLORS['TEXT_WHITE']
            text_surface = self.data_font.render(text, True, color)
            screen.blit(text_surface, (x, y + i * 14))
    
    def _render_eva_status(self, screen, x, y):
        """Render EVA status"""
        eva_data = [
            "Unit: EVA-01",
            "Power: 100%",
            "AT Field: Active"
        ]
        
        for i, text in enumerate(eva_data):
            text_surface = self.data_font.render(text, True, COLORS['TEXT_WHITE'])
            screen.blit(text_surface, (x, y + i * 14))
    
    def _render_relationships(self, screen, x, y):
        """Render relationships"""
        relationships = self.game_manager.get_relationships()
        sorted_relations = sorted(relationships.items(), key=lambda x: x[1], reverse=True)
        
        for i, (character, level) in enumerate(sorted_relations[:3]):
            if i * 14 + y > y + 40:  # Don't exceed section bounds
                break
            
            color = COLORS['SUCCESS_GREEN'] if level > 50 else COLORS['TEXT_WHITE']
            text = f"{character}: {level}"
            text_surface = self.data_font.render(text, True, color)
            screen.blit(text_surface, (x, y + i * 14))
    
    def _render_objectives(self, screen, x, y):
        """Render objectives"""
        objectives = [
            "Complete morning routine",
            "Report to NERV",
            "Angel threat assessment"
        ]
        
        for i, objective in enumerate(objectives[:3]):
            if i * 14 + y > y + 40:
                break
            
            text_surface = self.data_font.render(f"• {objective}", True, COLORS['TEXT_WHITE'])
            screen.blit(text_surface, (x, y + i * 14))
    
    def _render_location(self, screen, x, y):
        """Render location info"""
        current_scene = self.game_manager.scene_manager.get_current_scene_name()
        location_info = [
            f"Scene: {current_scene}",
            "Area: Residential",
            "Time: Morning"
        ]
        
        for i, info in enumerate(location_info):
            text_surface = self.data_font.render(info, True, COLORS['TEXT_WHITE'])
            screen.blit(text_surface, (x, y + i * 14))
    
    def _render_system(self, screen, x, y):
        """Render system info"""
        system_info = [
            "FPS: 60",
            "Version: 1.0", 
            "Status: OK"
        ]
        
        for i, info in enumerate(system_info):
            text_surface = self.data_font.render(info, True, COLORS['UI_GRAY'])
            screen.blit(text_surface, (x, y + i * 14))
"""
===============================
ENHANCED HUB SCENE (WITH ART)
===============================
Hub scene with integrated art system
"""

import pygame
from scenes.hub_scene import HubScene
from assets.art_manager import ArtManager

class EnhancedHubScene(HubScene):
    """
    ENHANCED HUB SCENE CLASS
    Hub scene with custom art support
    """
    
    def __init__(self, game_manager, scene_manager):
        """Initialize enhanced hub scene"""
        # Initialize art manager
        self.art_manager = ArtManager()
        
        # Call parent initialization
        super().__init__(game_manager, scene_manager)
        
        print("🎨 Enhanced Hub Scene with art support initialized")
    
    def render(self, screen):
        """Render hub scene with custom art"""
        # === CUSTOM BACKGROUND ===
        bg_art = self.art_manager.get_asset('nerv_hq_bg')
        if bg_art:
            # Scale background to screen size
            bg_scaled = pygame.transform.scale(bg_art, (screen.get_width(), screen.get_height()))
            screen.blit(bg_scaled, (0, 0))
        else:
            # Fallback to original rendering
            self.enhanced_renderer.render_nerv_headquarters(screen)
        
        # === RENDER AREAS WITH CUSTOM ICONS ===
        self._render_areas_with_art(screen)
        
        # === RENDER NPCS WITH CUSTOM SPRITES ===
        self._render_npcs_with_art(screen)
        
        # === RENDER PLAYER WITH CUSTOM SPRITE ===
        self._render_player_with_art(screen)
        
        # === UI WITH CUSTOM ART ===
        if not self.in_dialogue:
            self._render_hud_with_art(screen)
            self.mouse_controller.render_mouse_ui(screen)
        
        self.status_manager.render(screen)
        
        # === DIALOGUE SYSTEM ===
        if self.in_dialogue:
            self._render_dialogue_with_art(screen)
        
        # === SCENE INFO ===
        self._render_adjusted_scene_info(screen)
    
    def _render_npcs_with_art(self, screen):
        """Render NPCs with custom sprites"""
        for npc in self.npcs:
            # Get custom sprite
            character_name = npc.name.lower().replace(' ', '_').replace('.', '')
            sprite = self.art_manager.get_asset(character_name)
            
            if sprite:
                # Scale sprite appropriately
                sprite_scaled = pygame.transform.scale(sprite, (40, 60))
                sprite_rect = sprite_scaled.get_rect(center=(npc.x, npc.y))
                screen.blit(sprite_scaled, sprite_rect)
                
                # Name label
                font = pygame.font.Font(None, 16)
                name_surface = font.render(npc.name.split()[0], True, COLORS['TEXT_WHITE'])
                name_rect = name_surface.get_rect(center=(npc.x, npc.y - 40))
                
                # Name background
                bg_rect = name_rect.inflate(4, 2)
                pygame.draw.rect(screen, (0, 0, 0, 120), bg_rect)
                screen.blit(name_surface, name_rect)
            else:
                # Fallback to original rendering
                npc.render(screen)
    
    def _render_player_with_art(self, screen):
        """Render player with custom sprite"""
        sprite = self.art_manager.get_asset('shinji')
        
        if sprite:
            sprite_scaled = pygame.transform.scale(sprite, (32, 48))
            sprite_rect = sprite_scaled.get_rect(center=(self.player.x, self.player.y))
            screen.blit(sprite_scaled, sprite_rect)
        else:
            # Fallback to original rendering
            self.player.render(screen)
    
    def _render_dialogue_with_art(self, screen):
        """Render dialogue system with character portraits"""
        if not self.current_npc:
            return
        
        # === CUSTOM DIALOGUE BOX ===
        dialogue_bg = self.art_manager.get_asset('dialogue_box')
        dialogue_height = 250
        dialogue_rect = pygame.Rect(0, screen.get_height() - dialogue_height, screen.get_width(), dialogue_height)
        
        if dialogue_bg:
            dialogue_scaled = pygame.transform.scale(dialogue_bg, (dialogue_rect.width, dialogue_rect.height))
            screen.blit(dialogue_scaled, dialogue_rect.topleft)
        else:
            # Fallback
            dialogue_surface = pygame.Surface((screen.get_width(), dialogue_height), pygame.SRCALPHA)
            dialogue_surface.fill((20, 20, 30, 220))
            screen.blit(dialogue_surface, dialogue_rect.topleft)
            pygame.draw.rect(screen, COLORS['NERV_RED'], dialogue_rect, 3)
        
        # === CHARACTER PORTRAIT ===
        character_name = self.current_npc.name.lower().replace(' ', '_').replace('.', '')
        portrait = self.art_manager.get_asset(f"{character_name}_portrait")
        
        if portrait:
            portrait_size = 80
            portrait_scaled = pygame.transform.scale(portrait, (portrait_size, portrait_size))
            portrait_rect = pygame.Rect(dialogue_rect.left + 20, dialogue_rect.top + 20, portrait_size, portrait_size)
            screen.blit(portrait_scaled, portrait_rect)
        
        # === CHARACTER NAME ===
        name_font = pygame.font.Font(None, 28)
        name_text = name_font.render(self.current_npc.name, True, COLORS['NERV_RED'])
        name_x = dialogue_rect.left + (120 if portrait else 50)
        name_rect = pygame.Rect(name_x, dialogue_rect.top + 10, 300, 35)
        
        pygame.draw.rect(screen, (40, 20, 20), name_rect)
        pygame.draw.rect(screen, COLORS['NERV_RED'], name_rect, 2)
        
        name_pos = name_text.get_rect(center=name_rect.center)
        screen.blit(name_text, name_pos)
        
        # === DIALOGUE OPTIONS ===
        option_font = pygame.font.Font(None, 20)
        option_start_y = dialogue_rect.top + 60
        
        for i, dialogue_line in enumerate(self.current_npc.dialogue_lines):
            if i >= 5:
                break
            
            option_y = option_start_y + i * 35
            option_rect = pygame.Rect(name_x, option_y, screen.get_width() - name_x - 20, 30)
            
            option_bg_color = (60, 40, 80) if i % 2 == 0 else (50, 30, 70)
            pygame.draw.rect(screen, option_bg_color, option_rect)
            pygame.draw.rect(screen, COLORS['TERMINAL_GREEN'], option_rect, 1)
            
            number_text = f"{i + 1}."
            number_surface = option_font.render(number_text, True, COLORS['SCHOOL_YELLOW'])
            screen.blit(number_surface, (option_rect.left + 10, option_rect.top + 6))
            
            option_surface = option_font.render(dialogue_line, True, COLORS['TEXT_WHITE'])
            screen.blit(option_surface, (option_rect.left + 40, option_rect.top + 6))
        
        # === INSTRUCTIONS ===
        instruction_font = pygame.font.Font(None, 16)
        instruction_text = "Left click options or press 1-5 | ESC to close"
        instruction_surface = instruction_font.render(instruction_text, True, COLORS['UI_GRAY'])
        instruction_rect = instruction_surface.get_rect(center=(screen.get_width() // 2, dialogue_rect.bottom - 15))
        screen.blit(instruction_surface, instruction_rect)
    
    def _render_hud_with_art(self, screen):
        """Render HUD with custom art elements"""
        # Custom HUD panel
        hud_bg = self.art_manager.get_asset('hud_panel')
        if hud_bg:
            hud_scaled = pygame.transform.scale(hud_bg, (200, 500))
            screen.blit(hud_scaled, (screen.get_width() - 210, 10))
        
        # Render HUD with custom icons
        self.hud.render_with_custom_art(screen, self.art_manager)
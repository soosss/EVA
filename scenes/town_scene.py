"""
===============================
TOWN SCENE - COMPLETE
===============================
School and town exploration scene
"""

import pygame

# Add proper imports for screen dimensions
try:
    from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    from config import COLORS
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

class TownScene:
    """Complete town exploration scene"""
    
    def __init__(self, game_manager, scene_manager):
        """Initialize town scene"""
        self.game_manager = game_manager
        self.scene_manager = scene_manager
        
        # Scene state
        self.current_location = "school"
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        
        # NPCs
        self.npcs = [
            {"name": "Classmate", "pos": (200, 300), "dialogue": ["Just another day at school..."]},
            {"name": "Teacher", "pos": (500, 200), "dialogue": ["Study hard for the exams!"]}
        ]
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        
        print("🏫 Town Scene initialized")
    
    def handle_event(self, event):
        """Handle town events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.scene_manager.change_scene("hub")
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.player_x = max(20, self.player_x - 20)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.player_x = min(SCREEN_WIDTH - 20, self.player_x + 20)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.player_y = max(20, self.player_y - 20)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.player_y = min(SCREEN_HEIGHT - 20, self.player_y + 20)
    
    def update(self, dt):
        """Update town scene"""
        pass
    
    def render(self, screen):
        """Render town scene"""
        # Background
        screen.fill((100, 150, 100))  # Green for outdoors
        
        # School building
        school_rect = pygame.Rect(300, 100, 200, 150)
        pygame.draw.rect(screen, (150, 100, 50), school_rect)
        pygame.draw.rect(screen, COLORS['TEXT_WHITE'], school_rect, 2)
        
        # Title
        title_text = "TOKYO-3 SCHOOL"
        title_surface = self.title_font.render(title_text, True, COLORS['TEXT_WHITE'])
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(title_surface, title_rect)
        
        # NPCs
        for npc in self.npcs:
            pygame.draw.circle(screen, COLORS['SCHOOL_YELLOW'], npc["pos"], 15)
            pygame.draw.circle(screen, COLORS['TEXT_WHITE'], npc["pos"], 15, 2)
        
        # Player
        player_rect = pygame.Rect(self.player_x - 10, self.player_y - 15, 20, 30)
        pygame.draw.rect(screen, COLORS['EVA_PURPLE'], player_rect)
        pygame.draw.rect(screen, COLORS['TEXT_WHITE'], player_rect, 2)
        
        # Instructions
        instruction_text = "Use WASD or Arrow Keys to move | ESC: Return to Hub"
        instruction_surface = pygame.font.Font(None, 16).render(instruction_text, True, COLORS['TEXT_WHITE'])
        screen.blit(instruction_surface, (20, SCREEN_HEIGHT - 25))
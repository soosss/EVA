"""
===============================
NERV ARRIVAL SCENE - FIXED IMPORTS
===============================
"""

import pygame
import random

# Add proper imports for screen dimensions
try:
    from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    from config import COLORS
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

# Import enhanced systems with correct names and fallbacks
try:
    from ui.hud import EnhancedHUD as HUD
except ImportError:
    print("⚠️ EnhancedHUD not available, using fallback")
    HUD = None

try:
    from entities.player import EnhancedPlayer as Player
except ImportError:
    print("⚠️ EnhancedPlayer not available, using fallback")
    Player = None

try:
    from ui.status_system import StatusSystem
except ImportError:
    print("⚠️ StatusSystem not available, using fallback")
    StatusSystem = None

class NervArrivalScene:
    """NERV Arrival Scene with enhanced systems"""
    
    def __init__(self, game_manager, scene_manager):
        self.game_manager = game_manager
        self.scene_manager = scene_manager
        
        # Enhanced systems (with fallbacks)
        self.hud = HUD(game_manager) if HUD else None
        self.player = Player(400, 300, game_manager) if Player else None
        self.status_system = StatusSystem() if StatusSystem else None
        
        # Basic player fallback
        if not self.player:
            self.player_x = 400
            self.player_y = 300
            self.player_speed = 180
        
        # Scene state
        self.scene_state = "arrival"
        self.briefing_started = False
        self.briefing_complete = False
        self.elevator_available = False
        
        # NERV personnel
        self.personnel = [
            {"name": "Misato", "pos": (200, 250), "talked": False, "dialogue": [
                "Misato: Welcome to NERV, Shinji.",
                "Misato: This is where we fight the Angels.",
                "Misato: Are you ready for your first briefing?"
            ]},
            {"name": "Maya", "pos": (500, 200), "talked": False, "dialogue": [
                "Maya: The EVA units are incredible machines.",
                "Maya: Your sync rate will determine compatibility.",
                "Maya: Good luck, pilot!"
            ]},
            {"name": "Ritsuko", "pos": (350, 180), "talked": False, "dialogue": [
                "Ritsuko: The science behind EVA is complex.",
                "Ritsuko: But you don't need to understand it all.",
                "Ritsuko: Just focus on syncing with your unit."
            ]}
        ]
        
        # Interactive areas
        self.interactive_areas = [
            {"name": "Elevator", "pos": (100, 400), "size": (60, 40), "requires_briefing": True},
            {"name": "Command Center", "pos": (300, 100), "size": (200, 80), "requires_briefing": False},
            {"name": "EVA Bay Access", "pos": (600, 350), "size": (100, 50), "requires_briefing": True}
        ]
        
        # Conversation system
        self.in_conversation = False
        self.current_npc = None
        self.dialogue_index = 0
        
        # Visual elements
        self.background_scroll = 0
        self.animation_timer = 0
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 24)
        self.dialogue_font = pygame.font.Font(None, 20)
        
        # Background
        self.background = self._create_nerv_background()
        
        print("🏢 NERV Arrival Scene initialized")
    
    def _create_nerv_background(self):
        """Create NERV facility background"""
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Base facility color
        background.fill((40, 40, 50))
        
        # Floor pattern
        floor_rect = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(background, (60, 60, 70), floor_rect)
        
        # Grid pattern on floor
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(background, (80, 80, 90), (x, SCREEN_HEIGHT - 80), (x, SCREEN_HEIGHT), 1)
        
        # NERV logo area
        logo_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, 50, 100, 60)
        pygame.draw.rect(background, COLORS['NERV_RED'], logo_rect)
        pygame.draw.rect(background, COLORS['TEXT_WHITE'], logo_rect, 3)
        
        # Command center outline
        command_rect = pygame.Rect(300, 100, 200, 80)
        pygame.draw.rect(background, (70, 70, 80), command_rect)
        pygame.draw.rect(background, COLORS['TERMINAL_GREEN'], command_rect, 2)
        
        return background
    
    def handle_event(self, event):
        """Handle NERV arrival events"""
        if self.in_conversation:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self._advance_dialogue()
                elif event.key == pygame.K_ESCAPE:
                    self._end_conversation()
        else:
            # Enhanced player handles movement if available
            if self.player:
                self.player.handle_event(event)
            else:
                # Basic movement fallback
                self._handle_basic_movement(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._check_interactions()
                elif event.key == pygame.K_ESCAPE:
                    if self.briefing_complete:
                        self.scene_manager.change_scene("hub")
                    else:
                        self.scene_manager.change_scene("bedroom")
    
    def _handle_basic_movement(self, event):
        """Basic movement fallback"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.player_x = max(20, self.player_x - 20)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.player_x = min(SCREEN_WIDTH - 240, self.player_x + 20)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.player_y = max(20, self.player_y - 20)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.player_y = min(SCREEN_HEIGHT - 40, self.player_y + 20)
    
    def _check_interactions(self):
        """Check for nearby interactions"""
        if self.player:
            player_rect = self.player.get_rect()
        else:
            player_rect = pygame.Rect(self.player_x - 10, self.player_y - 10, 20, 20)
        
        # Check NPC interactions
        for npc in self.personnel:
            npc_rect = pygame.Rect(npc["pos"][0] - 20, npc["pos"][1] - 20, 40, 40)
            if player_rect.colliderect(npc_rect) and not npc["talked"]:
                self._start_npc_conversation(npc)
                return
        
        # Check area interactions
        for area in self.interactive_areas:
            area_rect = pygame.Rect(area["pos"][0], area["pos"][1], area["size"][0], area["size"][1])
            if player_rect.colliderect(area_rect):
                self._interact_with_area(area)
                return
    
    def _start_npc_conversation(self, npc):
        """Start conversation with NPC"""
        self.in_conversation = True
        self.current_npc = npc
        self.dialogue_index = 0
        
        if self.status_system:
            self.status_system.add_message(f"Talking to {npc['name']}", "info")
    
    def _advance_dialogue(self):
        """Advance to next dialogue line"""
        if self.current_npc and self.dialogue_index < len(self.current_npc["dialogue"]) - 1:
            self.dialogue_index += 1
        else:
            self._end_conversation()
    
    def _end_conversation(self):
        """End current conversation"""
        if self.current_npc:
            self.current_npc["talked"] = True
            self.game_manager.modify_relationship(self.current_npc["name"], 3)
            
            if self.status_system:
                self.status_system.add_message(f"Conversation with {self.current_npc['name']} complete", "success")
        
        self.in_conversation = False
        self.current_npc = None
        self.dialogue_index = 0
        
        # Check if briefing should start
        self._check_briefing_status()
    
    def _interact_with_area(self, area):
        """Interact with facility area"""
        if area["requires_briefing"] and not self.briefing_complete:
            if self.status_system:
                self.status_system.add_message("Complete briefing first", "warning")
            return
        
        if area["name"] == "Elevator":
            if self.briefing_complete:
                if self.status_system:
                    self.status_system.add_message("Heading to EVA bays...", "success")
                self.scene_manager.change_scene("hub")
        
        elif area["name"] == "Command Center":
            if self.status_system:
                self.status_system.add_message("NERV command operations center", "info")
        
        elif area["name"] == "EVA Bay Access":
            if self.briefing_complete:
                if self.status_system:
                    self.status_system.add_message("EVA units are housed below", "info")
                self.scene_manager.change_scene("action_battle", angel_name="Tutorial Angel")
    
    def _check_briefing_status(self):
        """Check if briefing requirements are met"""
        if not self.briefing_started:
            talked_count = sum(1 for npc in self.personnel if npc["talked"])
            if talked_count >= 2:  # Need to talk to at least 2 people
                self.briefing_started = True
                if self.status_system:
                    self.status_system.add_message("Initial briefing complete!", "success")
        
        if self.briefing_started and not self.briefing_complete:
            all_talked = all(npc["talked"] for npc in self.personnel)
            if all_talked:
                self.briefing_complete = True
                self.elevator_available = True
                if self.status_system:
                    self.status_system.add_message("Full briefing complete - areas unlocked!", "success")
    
    def update(self, dt):
        """Update NERV arrival scene"""
        self.animation_timer += dt
        self.background_scroll += dt * 10
        
        # Update enhanced systems
        if self.player:
            self.player.update(dt)
        if self.hud:
            self.hud.update(dt)
        if self.status_system:
            self.status_system.update(dt)
        
        # Update scene state
        self._check_briefing_status()
    
    def render(self, screen):
        """Render NERV arrival scene"""
        # Background
        screen.blit(self.background, (0, 0))
        
        # Animated elements
        self._render_animated_elements(screen)
        
        # Interactive areas
        self._render_interactive_areas(screen)
        
        # NPCs
        self._render_npcs(screen)
        
        # Enhanced player or basic fallback
        if self.player:
            self.player.render(screen)
        else:
            # Basic player rectangle
            player_rect = pygame.Rect(self.player_x - 10, self.player_y - 15, 20, 30)
            pygame.draw.rect(screen, COLORS['EVA_PURPLE'], player_rect)
            pygame.draw.rect(screen, COLORS['TEXT_WHITE'], player_rect, 2)
        
        # Conversation overlay
        if self.in_conversation:
            self._render_conversation(screen)
        
        # Scene title
        title_text = "NERV HEADQUARTERS"
        title_surface = self.title_font.render(title_text, True, COLORS['NERV_RED'])
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(title_surface, title_rect)
        
        # Enhanced HUD (if available)
        if self.hud:
            self.hud.render(screen)
        
        # Status system (if available)
        if self.status_system:
            self.status_system.render(screen)
        
        # Instructions
        if not self.briefing_complete:
            instruction_text = "Talk to NERV personnel (SPACE to interact)"
            instruction_surface = pygame.font.Font(None, 18).render(instruction_text, True, COLORS['UI_GRAY'])
            screen.blit(instruction_surface, (20, SCREEN_HEIGHT - 25))
    
    def _render_animated_elements(self, screen):
        """Render animated background elements"""
        # Scrolling lights
        import math
        for i in range(5):
            x = (self.background_scroll + i * 100) % (SCREEN_WIDTH + 50) - 50
            y = 120 + math.sin(self.animation_timer + i) * 10
            light_rect = pygame.Rect(x, y, 8, 8)
            pygame.draw.rect(screen, COLORS['TERMINAL_GREEN'], light_rect)
    
    def _render_interactive_areas(self, screen):
        """Render interactive areas"""
        for area in self.interactive_areas:
            # Determine color based on availability
            if area["requires_briefing"] and not self.briefing_complete:
                color = COLORS['UI_GRAY']
                alpha = 100
            else:
                color = COLORS['HANGAR_BLUE']
                alpha = 200
            
            # Create area surface with alpha
            area_surface = pygame.Surface(area["size"], pygame.SRCALPHA)
            area_surface.fill((*color, alpha))
            screen.blit(area_surface, area["pos"])
            
            # Border
            area_rect = pygame.Rect(area["pos"][0], area["pos"][1], area["size"][0], area["size"][1])
            pygame.draw.rect(screen, color, area_rect, 2)
            
            # Label
            label_surface = pygame.font.Font(None, 16).render(area["name"], True, color)
            label_rect = label_surface.get_rect(center=area_rect.center)
            screen.blit(label_surface, label_rect)
    
    def _render_npcs(self, screen):
        """Render NPCs"""
        for npc in self.personnel:
            # NPC circle
            color = COLORS['UI_GRAY'] if npc["talked"] else COLORS['SCHOOL_YELLOW']
            pygame.draw.circle(screen, color, npc["pos"], 15)
            pygame.draw.circle(screen, COLORS['TEXT_WHITE'], npc["pos"], 15, 2)
            
            # Name label
            name_surface = pygame.font.Font(None, 14).render(npc["name"], True, color)
            name_rect = name_surface.get_rect(center=(npc["pos"][0], npc["pos"][1] - 25))
            screen.blit(name_surface, name_rect)
            
            # Interaction indicator
            if not npc["talked"]:
                indicator_surface = pygame.font.Font(None, 12).render("!", True, COLORS['WARNING_ORANGE'])
                indicator_rect = indicator_surface.get_rect(center=(npc["pos"][0] + 12, npc["pos"][1] - 12))
                screen.blit(indicator_surface, indicator_rect)
    
    def _render_conversation(self, screen):
        """Render conversation interface"""
        if not self.current_npc:
            return
        
        # Conversation background
        conv_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 100, 120)
        
        # Create conversation surface with alpha
        conv_surface = pygame.Surface((conv_rect.width, conv_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(conv_surface, (0, 0, 0, 180), conv_surface.get_rect())
        pygame.draw.rect(conv_surface, COLORS['NERV_RED'], conv_surface.get_rect(), 2)
        screen.blit(conv_surface, conv_rect.topleft)
        
        # Current dialogue
        current_dialogue = self.current_npc["dialogue"][self.dialogue_index]
        dialogue_text = self.dialogue_font.render(current_dialogue, True, COLORS['TEXT_WHITE'])
        dialogue_rect = dialogue_text.get_rect(left=conv_rect.left + 20, top=conv_rect.top + 20)
        screen.blit(dialogue_text, dialogue_rect)
        
        # Progress indicator
        progress_text = f"{self.dialogue_index + 1}/{len(self.current_npc['dialogue'])}"
        progress_surface = pygame.font.Font(None, 14).render(progress_text, True, COLORS['UI_GRAY'])
        progress_rect = progress_surface.get_rect(right=conv_rect.right - 20, top=conv_rect.top + 10)
        screen.blit(progress_surface, progress_rect)
        
        # Continue prompt
        prompt_text = "SPACE: Continue | ESC: End conversation"
        prompt_surface = pygame.font.Font(None, 16).render(prompt_text, True, COLORS['UI_GRAY'])
        prompt_rect = prompt_surface.get_rect(right=conv_rect.right - 20, bottom=conv_rect.bottom - 10)
        screen.blit(prompt_surface, prompt_rect)
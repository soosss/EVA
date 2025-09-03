"""
BEDROOM SCENE - SIMPLIFIED WORKING VERSION
"""

import pygame

# Add proper imports for screen dimensions
try:
    from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    from config import COLORS
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

# Import enhanced systems with fallbacks
try:
    from ui.hud import EnhancedHUD
except ImportError:
    print("⚠️ EnhancedHUD not available, using fallback")
    EnhancedHUD = None

try:
    from entities.player import EnhancedPlayer
except ImportError:
    print("⚠️ EnhancedPlayer not available, using fallback")
    EnhancedPlayer = None

try:
    from ui.status_system import StatusSystem
except ImportError:
    print("⚠️ StatusSystem not available, using fallback")
    StatusSystem = None

try:
    from input.mouse_controller import MouseController
except ImportError:
    print("⚠️ MouseController not available, using fallback")
    MouseController = None

class BedroomScene:
    def __init__(self, game_manager, scene_manager):
        self.game_manager = game_manager
        self.scene_manager = scene_manager
        
        # Enhanced systems (with fallbacks)
        self.enhanced_hud = EnhancedHUD(game_manager) if EnhancedHUD else None
        self.enhanced_player = EnhancedPlayer(400, 300, game_manager) if EnhancedPlayer else None
        self.status_system = StatusSystem() if StatusSystem else None
        
        # Mouse Controller
        self.mouse_controller = MouseController(game_manager) if MouseController else None
        if self.mouse_controller:
            self.mouse_controller.set_combat_mode(False)  # Normal movement mode
        
        # Basic player fallback
        if not self.enhanced_player:
            self.player_x = 400
            self.player_y = 300
            self.player_speed = 180
        
        # Room state
        self.room_state = "morning"
        self.interactions_completed = 0
        self.max_interactions = 3
        
        # Interactive objects
        self.interactive_objects = [
            {"name": "Mirror", "pos": (150, 200), "size": (40, 60), "interacted": False},
            {"name": "Desk", "pos": (500, 250), "size": (80, 40), "interacted": False},
            {"name": "Bed", "pos": (300, 350), "size": (120, 80), "interacted": False}
        ]
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.text_font = pygame.font.Font(None, 24)
        
        # Conversation system
        self.in_conversation = False
        self.conversation_partner = None
        self.dialogue_index = 0
        
        # Asuka conversation - Enhanced from dialogue editor
        self.asuka_dialogues = [
            "Asuka: Hey! Third Child! Wake up already!",
            "Asuka: We're supposed to be at NERV in 30 minutes!",
            "Asuka: Misato's waiting and you know how she gets...",
            "Asuka: Come ON! Get out of bed!"
        ]
        
        # Asuka visual representation
        self.asuka_present = False
        self.asuka_x = 100
        self.asuka_y = 150
        self.asuka_width = 25
        self.asuka_height = 35
        
        print("🏠 Bedroom Scene initialized")
        
        # Start Asuka conversation automatically on scene initialization
        self._start_asuka_conversation()
    
    def handle_event(self, event):
        """Handle bedroom events"""
        # Always pass mouse events to mouse controller (even during conversation for movement)
        if self.mouse_controller:
            self.mouse_controller.handle_event(event, self)
        
        if self.in_conversation:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self._advance_dialogue()
                elif event.key == pygame.K_ESCAPE:
                    self._end_conversation()
        else:
            # Enhanced player handles movement if available
            if self.enhanced_player:
                self.enhanced_player.handle_event(event)
            else:
                # Basic movement fallback
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player_x = max(20, self.player_x - 20)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player_x = min(SCREEN_WIDTH - 240, self.player_x + 20)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player_y = max(20, self.player_y - 20)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player_y = min(SCREEN_HEIGHT - 40, self.player_y + 20)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._check_interactions()
                elif event.key == pygame.K_ESCAPE:
                    if self.interactions_completed >= self.max_interactions:
                        self.scene_manager.change_scene("nerv_arrival")
                    else:
                        self.scene_manager.change_scene("main_menu")
    
    def _check_interactions(self):
        """Check for nearby interactions"""
        if self.enhanced_player:
            player_rect = self.enhanced_player.get_rect()
        else:
            player_rect = pygame.Rect(self.player_x - 10, self.player_y - 10, 20, 20)
        
        for obj in self.interactive_objects:
            obj_rect = pygame.Rect(obj["pos"][0], obj["pos"][1], obj["size"][0], obj["size"][1])
            if player_rect.colliderect(obj_rect) and not obj["interacted"]:
                self._interact_with_object(obj)
                break
    
    def _interact_with_object(self, obj):
        """Interact with an object"""
        obj["interacted"] = True
        self.interactions_completed += 1
        
        if obj["name"] == "Mirror":
            if self.status_system:
                self.status_system.add_message("You look tired but determined", "neutral")
            self._start_asuka_conversation()
        elif obj["name"] == "Desk":
            if self.status_system:
                self.status_system.add_message("Your homework is half-finished", "info")
        elif obj["name"] == "Bed":
            if self.status_system:
                self.status_system.add_message("You should make your bed", "neutral")
        
        # Update relationship if interacting with personal items
        if obj["name"] in ["Mirror", "Desk"]:
            self.game_manager.modify_relationship("Shinji", 1)
    
    def _start_asuka_conversation(self):
        """Start conversation with Asuka"""
        self.in_conversation = True
        self.conversation_partner = "Asuka"
        self.dialogue_index = 0
        self.asuka_present = True  # Make Asuka visible
        if self.status_system:
            self.status_system.add_message("Asuka appears in the doorway", "info")
    
    def _advance_dialogue(self):
        """Advance to next dialogue line"""
        if self.dialogue_index < len(self.asuka_dialogues) - 1:
            self.dialogue_index += 1
        else:
            self._end_conversation()
    
    def _end_conversation(self):
        """End current conversation"""
        self.in_conversation = False
        self.conversation_partner = None
        self.dialogue_index = 0
        self.game_manager.modify_relationship("Asuka", 2)
        if self.status_system:
            self.status_system.add_message("Asuka leaves", "neutral")
    
    def update(self, dt):
        """Update bedroom scene"""
        # Update mouse controller
        if self.mouse_controller:
            self.mouse_controller.update(dt)
            # Update player movement from mouse clicks
            if self.enhanced_player:
                self.mouse_controller.update_player_movement(self.enhanced_player, dt)
        
        # Update enhanced systems
        if self.enhanced_player:
            self.enhanced_player.update(dt)
        if self.enhanced_hud:
            self.enhanced_hud.update(dt)
        if self.status_system:
            self.status_system.update(dt)
        
        # Check for scene completion
        if self.interactions_completed >= self.max_interactions and not self.in_conversation:
            if self.status_system:
                self.status_system.add_message("Ready to head to NERV (Press ESC)", "success")
    
    def render(self, screen):
        """Render bedroom scene"""
        # Calculate HUD area to avoid rendering game content behind it
        hud_start_x = SCREEN_WIDTH - 220 - 10  # Match HUD positioning
        playable_width = hud_start_x
        
        # Background - only fill the playable area
        background_rect = pygame.Rect(0, 0, playable_width, SCREEN_HEIGHT)
        pygame.draw.rect(screen, (60, 45, 35), background_rect)
        
        # Simple room elements
        # Floor - constrained to playable area
        floor_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, playable_width, 100)
        pygame.draw.rect(screen, (80, 60, 45), floor_rect)
        
        # Window
        window_rect = pygame.Rect(50, 100, 100, 120)
        pygame.draw.rect(screen, (150, 200, 255), window_rect)
        pygame.draw.rect(screen, (100, 50, 25), window_rect, 5)
        
        # Interactive objects
        self._render_interactive_objects(screen)
        
        # Render Asuka if present
        if self.asuka_present:
            self._render_asuka(screen)
        
        # Enhanced player or basic fallback
        if self.enhanced_player:
            self.enhanced_player.render(screen)
        else:
            # Basic player rectangle
            player_rect = pygame.Rect(self.player_x - 10, self.player_y - 15, 20, 30)
            pygame.draw.rect(screen, COLORS['EVA_PURPLE'], player_rect)
            pygame.draw.rect(screen, COLORS['TEXT_WHITE'], player_rect, 2)
        
        # Mouse controller visual effects
        if self.mouse_controller:
            self.mouse_controller.render_mouse_ui(screen)
        
        # Conversation overlay
        if self.in_conversation:
            self._render_conversation(screen)
        
        # Enhanced HUD (if available)
        if self.enhanced_hud:
            self.enhanced_hud.render(screen)
        
        # Status system (if available)
        if self.status_system:
            self.status_system.render(screen)
    
    def _render_interactive_objects(self, screen):
        """Render interactive objects"""
        for obj in self.interactive_objects:
            color = COLORS['UI_GRAY'] if obj["interacted"] else COLORS['SCHOOL_YELLOW']
            obj_rect = pygame.Rect(obj["pos"][0], obj["pos"][1], obj["size"][0], obj["size"][1])
            pygame.draw.rect(screen, color, obj_rect, 2)
            
            # Object label
            font = pygame.font.Font(None, 16)
            text = font.render(obj["name"], True, color)
            text_rect = text.get_rect(center=(obj_rect.centerx, obj_rect.top - 10))
            screen.blit(text, text_rect)
    
    def _render_asuka(self, screen):
        """Render Asuka character"""
        # Asuka body (simplified representation)
        asuka_rect = pygame.Rect(self.asuka_x, self.asuka_y, self.asuka_width, self.asuka_height)
        
        # Body color (orange/red for Asuka's plugsuit)
        pygame.draw.rect(screen, COLORS['WARNING_ORANGE'], asuka_rect)
        pygame.draw.rect(screen, COLORS['NERV_RED'], asuka_rect, 2)
        
        # Hair (blonde/orange)
        hair_rect = pygame.Rect(self.asuka_x - 3, self.asuka_y - 8, self.asuka_width + 6, 10)
        pygame.draw.rect(screen, (255, 200, 100), hair_rect)
        
        # Name label
        font = pygame.font.Font(None, 16)
        name_text = font.render("Asuka", True, COLORS['TEXT_WHITE'])
        name_rect = name_text.get_rect(center=(self.asuka_x + self.asuka_width//2, self.asuka_y - 15))
        screen.blit(name_text, name_rect)
    
    def _render_conversation(self, screen):
        """Render conversation interface"""
        # Conversation background - adjusted to avoid HUD overlap
        # HUD starts at SCREEN_WIDTH - 220 - 10 = 570, so conversation should end before that
        hud_start_x = SCREEN_WIDTH - 220 - 10  # Match HUD positioning from ui/hud.py
        conv_width = hud_start_x - 50 - 20  # Leave 20px margin from HUD
        conv_rect = pygame.Rect(50, SCREEN_HEIGHT - 150, conv_width, 120)
        
        # Create conversation surface with alpha
        conv_surface = pygame.Surface((conv_rect.width, conv_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(conv_surface, (0, 0, 0, 180), conv_surface.get_rect())
        pygame.draw.rect(conv_surface, COLORS['NERV_RED'], conv_surface.get_rect(), 2)
        screen.blit(conv_surface, conv_rect.topleft)
        
        # Current dialogue
        current_dialogue = self.asuka_dialogues[self.dialogue_index]
        dialogue_font = pygame.font.Font(None, 20)
        dialogue_text = dialogue_font.render(current_dialogue, True, COLORS['TEXT_WHITE'])
        dialogue_rect = dialogue_text.get_rect(left=conv_rect.left + 20, top=conv_rect.top + 20)
        screen.blit(dialogue_text, dialogue_rect)
        
        # Continue prompt
        prompt_text = "SPACE: Continue | ESC: End conversation"
        prompt_font = pygame.font.Font(None, 16)
        prompt_surface = prompt_font.render(prompt_text, True, COLORS['UI_GRAY'])
        prompt_rect = prompt_surface.get_rect(right=conv_rect.right - 20, bottom=conv_rect.bottom - 10)
        screen.blit(prompt_surface, prompt_rect)
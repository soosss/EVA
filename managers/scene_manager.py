"""
===============================
SCENE MANAGER - IMPORT FIXED
===============================
"""

import pygame

# Import core scenes
from scenes.main_menu import MainMenuScene
from scenes.bedroom_scene import BedroomScene
from scenes.nerv_arrival_scene import NervArrivalScene
from scenes.hub_scene import HubScene
from scenes.town_scene import TownScene
from scenes.action_battle_scene import ActionBattleScene

# Import enhanced scenes with error handling
try:
    from scenes.pause_menu import PauseMenu
except ImportError as e:
    print(f"⚠️ Could not import PauseMenu: {e}")
    PauseMenu = None

try:
    from scenes.settings_menu import SettingsMenu
except ImportError as e:
    print(f"⚠️ Could not import SettingsMenu: {e}")
    SettingsMenu = None

try:
    from scenes.art_gallery import ArtGallery
except ImportError as e:
    print(f"⚠️ Could not import ArtGallery: {e}")
    ArtGallery = None

class SceneManager:
    """Scene Manager with error handling"""
    
    def __init__(self, game_manager):
        """Initialize scene manager"""
        self.game_manager = game_manager
        self.current_scene = None
        self.scene_stack = []
        
        # === SCENE REGISTRY ===
        self.scene_classes = {
            # Core gameplay scenes
            "main_menu": MainMenuScene,
            "bedroom": BedroomScene,
            "nerv_arrival": NervArrivalScene,
            "hub": HubScene,
            "town": TownScene,
            "action_battle": ActionBattleScene,
        }
        
        # Add enhanced scenes if available
        if PauseMenu:
            self.scene_classes["pause_menu"] = PauseMenu
        if SettingsMenu:
            self.scene_classes["settings"] = SettingsMenu
        if ArtGallery:
            self.scene_classes["art_gallery"] = ArtGallery
        
        # === STORY PROGRESS ===
        self.story_flags = {
            "tutorial_complete": False,
            "first_angel_defeated": False,
            "bedroom_complete": False,
            "nerv_briefing_complete": False
        }
        
        # === PAUSE MENU INTEGRATION ===
        self.pause_menu_previous_scene = None
        self.pause_menu_instance = None
        
        print(f"🎬 Scene Manager initialized with {len(self.scene_classes)} scenes")
    
    def change_scene(self, scene_name, **kwargs):
        """Change to new scene with enhanced handling"""
        if scene_name == "tutorial_battle":
            scene_name = "action_battle"
            kwargs['angel_name'] = "Tutorial Angel"
        
        if scene_name not in self.scene_classes:
            print(f"❌ Unknown scene: {scene_name}")
            return
        
        try:
            print(f"🎬 Changing to scene: {scene_name}")
            
            scene_class = self.scene_classes[scene_name]
            
            # Handle scenes with special parameters
            if scene_name == "action_battle":
                angel_name = kwargs.get('angel_name', 'Sachiel')
                self.current_scene = scene_class(self.game_manager, self, angel_name)
            
            elif scene_name == "pause_menu" and PauseMenu:
                previous_scene = kwargs.get('previous_scene', self.current_scene)
                self.current_scene = scene_class(self.game_manager, self, previous_scene)
            
            else:
                # Standard scenes
                self.current_scene = scene_class(self.game_manager, self)
            
            print(f"✅ Scene changed to: {scene_name}")
            
        except Exception as e:
            print(f"❌ Scene change error: {e}")
            import traceback
            traceback.print_exc()
    
    def handle_event(self, event):
        """Handle events with pause menu integration"""
        # Global pause key (only if pause menu is available)
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and 
            PauseMenu and not isinstance(self.current_scene, (type(None)))):
            
            # Check if current scene allows pausing
            scene_name = self.current_scene.__class__.__name__
            if scene_name not in ["PauseMenu", "SettingsMenu", "ArtGallery"]:
                # Open pause menu
                self.pause_menu_previous_scene = self.current_scene
                self.change_scene("pause_menu", previous_scene=self.current_scene)
                return
        
        # Delegate to current scene
        if self.current_scene:
            try:
                self.current_scene.handle_event(event)
            except Exception as e:
                print(f"❌ Scene event error: {e}")
    
    def update(self, dt):
        """Update current scene"""
        if self.current_scene:
            try:
                self.current_scene.update(dt)
            except Exception as e:
                print(f"❌ Scene update error: {e}")
    
    def render(self, screen):
        """Render current scene"""
        if self.current_scene:
            try:
                self.current_scene.render(screen)
            except Exception as e:
                print(f"❌ Scene render error: {e}")
                # Emergency fallback
                screen.fill((20, 20, 40))
                font = pygame.font.Font(None, 48)
                text = font.render("NERV", True, (255, 255, 255))
                text_rect = text.get_rect(center=(400, 300))
                screen.blit(text, text_rect)
        else:
            # No scene loaded
            screen.fill((20, 20, 40))
            font = pygame.font.Font(None, 48)
            text = font.render("Loading...", True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, 300))
            screen.blit(text, text_rect)
    
    # Rest of the methods remain the same...
    def complete_tutorial(self):
        """Mark tutorial as complete"""
        self.story_flags["tutorial_complete"] = True
        print("🎓 Tutorial completed")
    
    def start_angel_battle(self, angel_name="Sachiel"):
        """Start Angel battle"""
        self.change_scene("action_battle", angel_name=angel_name)
    
    def get_story_progress(self):
        """Get story progress"""
        return self.story_flags.copy()
    
    def get_current_scene_name(self):
        """Get current scene name"""
        if self.current_scene:
            return self.current_scene.__class__.__name__
        return "None"
    
    def cleanup(self):
        """Clean up scene manager"""
        self.current_scene = None
        self.scene_stack.clear()
        print("🧹 Scene Manager cleaned up")
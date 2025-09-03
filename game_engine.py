"""
===============================
GAME ENGINE - OPTIMIZED
===============================
Central game engine with all systems integrated

Features Managed:
- Scene management and transitions
- Input handling and processing  
- Rendering pipeline
- Audio management
- Performance monitoring
"""

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE, DEBUG_MODE
from managers.game_manager import GameManager
from managers.scene_manager import SceneManager

class GameEngine:
    """
    OPTIMIZED GAME ENGINE
    Manages all core game systems and the main loop
    """
    
    def __init__(self):
        """Initialize game engine with all systems"""
        print("🎮 Initializing Game Engine...")
        
        # === DISPLAY SETUP ===
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        
        # Set game icon (if available)
        self._set_game_icon()
        
        # === TIMING AND PERFORMANCE ===
        self.clock = pygame.time.Clock()
        self.running = True
        self.performance_stats = {
            'fps': 0,
            'frame_time': 0,
            'update_time': 0,
            'render_time': 0
        }
        
        # === CORE MANAGERS ===
        self.game_manager = GameManager()
        self.scene_manager = SceneManager(self.game_manager)
        
        # Link scene_manager to game_manager
        self.game_manager.scene_manager = self.scene_manager
        print("🔗 Scene manager linked to game manager")
        
        # === START WITH MAIN MENU ===
        self.scene_manager.change_scene("main_menu")
        
        print("✅ Game Engine initialized successfully")
    
    def _set_game_icon(self):
        """Set game window icon"""
        try:
            # Create simple EVA-themed icon
            icon = pygame.Surface((32, 32))
            icon.fill((128, 0, 128))  # EVA purple
            pygame.draw.circle(icon, (255, 255, 255), (16, 16), 12)
            pygame.draw.circle(icon, (128, 0, 128), (16, 16), 8)
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"⚠️ Could not set game icon: {e}")
    
    def run(self):
        """
        Main game loop with performance monitoring
        """
        print("🚀 Starting main game loop")
        
        while self.running:
            frame_start = pygame.time.get_ticks()
            
            # Calculate delta time
            dt = self.clock.tick(FPS) / 1000.0
            
            # === HANDLE EVENTS ===
            self._handle_events()
            
            # === UPDATE GAME STATE ===
            update_start = pygame.time.get_ticks()
            self._update(dt)
            update_time = pygame.time.get_ticks() - update_start
            
            # === RENDER EVERYTHING ===
            render_start = pygame.time.get_ticks()
            self._render()
            render_time = pygame.time.get_ticks() - render_start
            
            # === PERFORMANCE TRACKING ===
            if DEBUG_MODE:
                self._update_performance_stats(frame_start, update_time, render_time)
        
        print("🛑 Main game loop ended")
    
    def _handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            # === SYSTEM EVENTS ===
            if event.type == pygame.QUIT:
                self.running = False
            
            # === GLOBAL HOTKEYS ===
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self._toggle_fullscreen()
                elif event.key == pygame.K_F4 and pygame.key.get_pressed()[pygame.K_LALT]:
                    self.running = False
                elif event.key == pygame.K_F1 and DEBUG_MODE:
                    self._show_debug_info()
            
            # === PASS TO SCENE MANAGER ===
            try:
                self.scene_manager.handle_event(event)
            except Exception as e:
                print(f"⚠️ Event handling error: {e}")
    
    def _update(self, dt):
        """Update all game systems"""
        try:
            self.game_manager.update(dt)
            self.scene_manager.update(dt)
        except Exception as e:
            print(f"⚠️ Update error: {e}")
    
    def _render(self):
        """Render everything to screen"""
        try:
            # Clear screen
            self.screen.fill((0, 0, 0))
            
            # Render current scene
            self.scene_manager.render(self.screen)
            
            # Debug overlay
            if DEBUG_MODE:
                self._render_debug_overlay()
            
            # Update display
            pygame.display.flip()
            
        except Exception as e:
            print(f"⚠️ Render error: {e}")
            # Emergency fallback rendering
            self.screen.fill((20, 20, 40))
            font = pygame.font.Font(None, 48)
            text = font.render("NERV", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()
    
    def _toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        try:
            if self.screen.get_flags() & pygame.FULLSCREEN:
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                print("🖥️ Switched to windowed mode")
            else:
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                print("🖥️ Switched to fullscreen mode")
        except Exception as e:
            print(f"⚠️ Fullscreen toggle error: {e}")
    
    def _update_performance_stats(self, frame_start, update_time, render_time):
        """Update performance statistics"""
        frame_time = pygame.time.get_ticks() - frame_start
        
        self.performance_stats.update({
            'fps': self.clock.get_fps(),
            'frame_time': frame_time,
            'update_time': update_time,
            'render_time': render_time
        })
    
    def _render_debug_overlay(self):
        """Render debug information overlay"""
        if not DEBUG_MODE:
            return
        
        debug_font = pygame.font.Font(None, 16)
        y_offset = 10
        
        debug_info = [
            f"FPS: {self.performance_stats['fps']:.1f}",
            f"Frame: {self.performance_stats['frame_time']}ms",
            f"Update: {self.performance_stats['update_time']}ms",
            f"Render: {self.performance_stats['render_time']}ms",
            f"Scene: {self.scene_manager.get_current_scene_name()}"
        ]
        
        for info in debug_info:
            text = debug_font.render(info, True, (255, 255, 0))
            self.screen.blit(text, (10, y_offset))
            y_offset += 18
    
    def _show_debug_info(self):
        """Show detailed debug information"""
        print("🔍 DEBUG INFO:")
        print(f"   FPS: {self.performance_stats['fps']:.1f}")
        print(f"   Scene: {self.scene_manager.get_current_scene_name()}")
        print(f"   Player Data: Level {self.game_manager.get_player_data().level}")
    
    def shutdown(self):
        """Clean shutdown of all systems"""
        try:
            self.scene_manager.cleanup()
            self.game_manager.cleanup()
            print("🧹 Game systems cleaned up successfully")
        except Exception as e:
            print(f"⚠️ Shutdown error: {e}")
        
        self.running = False
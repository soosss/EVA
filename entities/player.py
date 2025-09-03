"""
===============================
ENHANCED PLAYER ENTITY - COMPLETE
===============================
Advanced player with all enhanced features
"""

import pygame
import math

# Add proper imports for screen dimensions
try:
    from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED
except ImportError:
    from config import COLORS
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PLAYER_SPEED = 180

class EnhancedPlayer:
    """
    ENHANCED PLAYER ENTITY
    Complete player system with all advanced features
    """
    
    def __init__(self, x, y, game_manager):
        """Initialize enhanced player"""
        self.game_manager = game_manager
        
        # === POSITION AND MOVEMENT ===
        self.x = float(x)
        self.y = float(y)
        self.target_x = self.x
        self.target_y = self.y
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = PLAYER_SPEED
        self.smooth_movement = True
        
        # === PLAYER DIMENSIONS ===
        self.width = 20
        self.height = 30
        self.collision_radius = 15
        
        # === MOVEMENT STATE ===
        self.moving = False
        self.facing_direction = "down"
        self.last_move_time = 0
        
        # === ANIMATION SYSTEM ===
        self.animation_timer = 0
        self.animation_frame = 0
        self.animation_speed = 8.0
        self.bob_offset = 0
        
        # === TRAIL EFFECT ===
        self.trail_points = []
        self.max_trail_length = 10
        self.trail_fade_time = 0.5
        
        # === BOUNDARIES ===
        self.boundary_padding = 10
        self.hud_boundary_x = SCREEN_WIDTH - 240  # Leave space for HUD
        
        # === INPUT STATE ===
        self.keys_pressed = {
            pygame.K_w: False, pygame.K_s: False,
            pygame.K_a: False, pygame.K_d: False,
            pygame.K_UP: False, pygame.K_DOWN: False,
            pygame.K_LEFT: False, pygame.K_RIGHT: False
        }
        
        # === VISUAL EFFECTS ===
        self.pulse_timer = 0
        self.pulse_intensity = 1.0
        self.interaction_highlight = False
        self.highlight_timer = 0
        
        print("👤 Enhanced Player initialized")
    
    def handle_event(self, event):
        """Handle player input events"""
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = True
        
        elif event.type == pygame.KEYUP:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = False
    
    def update(self, dt):
        """Update enhanced player with smooth movement"""
        # Update animation timers
        self.animation_timer += dt
        self.pulse_timer += dt
        self.highlight_timer += dt
        
        # Calculate movement
        dx, dy = self._calculate_movement()
        
        # Apply movement with boundary checking
        if dx != 0 or dy != 0:
            self._apply_movement(dx, dy, dt)
            self.moving = True
            self.last_move_time = 0
        else:
            self.moving = False
            self.last_move_time += dt
        
        # Update visual effects
        self._update_visual_effects(dt)
        
        # Update trail effect
        self._update_trail_effect()
    
    def _calculate_movement(self):
        """Calculate movement direction from input"""
        dx = 0
        dy = 0
        
        # Horizontal movement
        if (self.keys_pressed[pygame.K_a] or self.keys_pressed[pygame.K_LEFT]):
            dx -= 1
            self.facing_direction = "left"
        if (self.keys_pressed[pygame.K_d] or self.keys_pressed[pygame.K_RIGHT]):
            dx += 1
            self.facing_direction = "right"
        
        # Vertical movement
        if (self.keys_pressed[pygame.K_w] or self.keys_pressed[pygame.K_UP]):
            dy -= 1
            self.facing_direction = "up"
        if (self.keys_pressed[pygame.K_s] or self.keys_pressed[pygame.K_DOWN]):
            dy += 1
            self.facing_direction = "down"
        
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # sqrt(2)/2
            dy *= 0.707
        
        return dx, dy
    
    def _apply_movement(self, dx, dy, dt):
        """Apply movement with smooth interpolation and boundaries"""
        # Calculate new position
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt
        
        # Apply boundary constraints
        new_x = max(self.boundary_padding, 
                   min(new_x, self.hud_boundary_x - self.width - self.boundary_padding))
        new_y = max(self.boundary_padding, 
                   min(new_y, SCREEN_HEIGHT - self.height - self.boundary_padding))
        
        # Smooth movement interpolation
        if self.smooth_movement:
            lerp_factor = min(1.0, dt * 10)  # Smooth interpolation
            self.x += (new_x - self.x) * lerp_factor
            self.y += (new_y - self.y) * lerp_factor
        else:
            self.x = new_x
            self.y = new_y
        
        # Update velocity for effects
        self.velocity_x = dx * self.speed
        self.velocity_y = dy * self.speed
    
    def _update_visual_effects(self, dt):
        """Update visual effects"""
        # Pulse effect
        self.pulse_intensity = 1.0 + 0.1 * math.sin(self.pulse_timer * 4)
        
        # Animation frame for walking
        if self.moving:
            self.animation_frame = int(self.animation_timer * self.animation_speed) % 4
            self.bob_offset = math.sin(self.animation_timer * 10) * 2
        else:
            self.animation_frame = 0
            self.bob_offset = 0
        
        # Interaction highlight
        if self.highlight_timer > 3.0:  # Auto-disable after 3 seconds
            self.interaction_highlight = False
            self.highlight_timer = 0
    
    def _update_trail_effect(self):
        """Update trail effect"""
        # Add current position to trail
        current_time = pygame.time.get_ticks() / 1000.0
        self.trail_points.append({
            'x': self.x + self.width // 2,
            'y': self.y + self.height // 2,
            'time': current_time
        })
        
        # Remove old trail points
        cutoff_time = current_time - self.trail_fade_time
        self.trail_points = [point for point in self.trail_points if point['time'] > cutoff_time]
        
        # Limit trail length
        if len(self.trail_points) > self.max_trail_length:
            self.trail_points = self.trail_points[-self.max_trail_length:]
    
    def render(self, screen):
        """Render enhanced player with all effects"""
        # Render trail effect first
        self._render_trail_effect(screen)
        
        # Calculate render position with bob effect
        render_x = int(self.x)
        render_y = int(self.y + self.bob_offset)
        
        # Player body (main rectangle)
        player_rect = pygame.Rect(render_x, render_y, self.width, self.height)
        
        # Base color with pulse effect
        base_color = COLORS['EVA_PURPLE']
        pulse_color = tuple(min(255, int(c * self.pulse_intensity)) for c in base_color)
        
        # Interaction highlight
        if self.interaction_highlight:
            highlight_intensity = 0.5 + 0.5 * math.sin(self.highlight_timer * 8)
            highlight_color = tuple(min(255, int(c + 50 * highlight_intensity)) for c in pulse_color)
            pygame.draw.rect(screen, highlight_color, player_rect.inflate(6, 6))
        
        # Main player body
        pygame.draw.rect(screen, pulse_color, player_rect)
        pygame.draw.rect(screen, COLORS['TEXT_WHITE'], player_rect, 2)
        
        # Direction indicator
        self._render_direction_indicator(screen, render_x, render_y)
        
        # Movement animation effects
        if self.moving:
            self._render_movement_effects(screen, render_x, render_y)
        
        # Status indicators
        self._render_status_indicators(screen, render_x, render_y)
    
    def _render_trail_effect(self, screen):
        """Render player trail effect"""
        if len(self.trail_points) < 2:
            return
        
        current_time = pygame.time.get_ticks() / 1000.0
        
        for i, point in enumerate(self.trail_points):
            # Calculate fade based on age
            age = current_time - point['time']
            fade_factor = max(0, 1 - (age / self.trail_fade_time))
            
            if fade_factor > 0:
                # Trail point size decreases with age
                size = max(1, int(4 * fade_factor))
                alpha = int(100 * fade_factor)
                
                # Create trail surface with alpha
                trail_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                color = (*COLORS['EVA_PURPLE'], alpha)
                pygame.draw.circle(trail_surface, color, (size, size), size)
                
                screen.blit(trail_surface, (point['x'] - size, point['y'] - size))
    
    def _render_direction_indicator(self, screen, x, y):
        """Render direction indicator"""
        # Direction arrow
        arrow_size = 6
        center_x = x + self.width // 2
        center_y = y + self.height // 2
        
        if self.facing_direction == "up":
            points = [(center_x, center_y - arrow_size), 
                     (center_x - arrow_size//2, center_y), 
                     (center_x + arrow_size//2, center_y)]
        elif self.facing_direction == "down":
            points = [(center_x, center_y + arrow_size), 
                     (center_x - arrow_size//2, center_y), 
                     (center_x + arrow_size//2, center_y)]
        elif self.facing_direction == "left":
            points = [(center_x - arrow_size, center_y), 
                     (center_x, center_y - arrow_size//2), 
                     (center_x, center_y + arrow_size//2)]
        else:  # right
            points = [(center_x + arrow_size, center_y), 
                     (center_x, center_y - arrow_size//2), 
                     (center_x, center_y + arrow_size//2)]
        
        pygame.draw.polygon(screen, COLORS['SCHOOL_YELLOW'], points)
    
    def _render_movement_effects(self, screen, x, y):
        """Render movement animation effects"""
        # Speed lines
        if abs(self.velocity_x) > 50 or abs(self.velocity_y) > 50:
            num_lines = 3
            for i in range(num_lines):
                offset_x = -self.velocity_x * 0.02 * (i + 1)
                offset_y = -self.velocity_y * 0.02 * (i + 1)
                alpha = max(50, 150 - i * 50)
                
                line_surface = pygame.Surface((4, 2), pygame.SRCALPHA)
                color = (*COLORS['SCHOOL_YELLOW'], alpha)
                pygame.draw.rect(line_surface, color, line_surface.get_rect())
                
                screen.blit(line_surface, (x + self.width//2 + offset_x, 
                                         y + self.height//2 + offset_y))
    
    def _render_status_indicators(self, screen, x, y):
        """Render status indicators above player"""
        # Health/status indicator
        health_percentage = self.game_manager.get_player_health() / 100.0
        
        # Health bar above player
        bar_width = self.width
        bar_height = 3
        bar_x = x
        bar_y = y - 8
        
        # Background
        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        
        # Health fill
        fill_width = int(bar_width * health_percentage)
        if health_percentage > 0.6:
            health_color = COLORS['SUCCESS_GREEN']
        elif health_percentage > 0.3:
            health_color = COLORS['WARNING_YELLOW']
        else:
            health_color = COLORS['ERROR_RED']
        
        if fill_width > 0:
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, fill_width, bar_height))
    
    # === UTILITY METHODS ===
    
    def get_position(self):
        """Get current position"""
        return (self.x, self.y)
    
    def get_center_position(self):
        """Get center position"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def get_rect(self):
        """Get player rectangle for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def set_position(self, x, y):
        """Set player position"""
        self.x = float(x)
        self.y = float(y)
        self.target_x = self.x
        self.target_y = self.y
    
    def enable_interaction_highlight(self):
        """Enable interaction highlight effect"""
        self.interaction_highlight = True
        self.highlight_timer = 0
    
    def disable_interaction_highlight(self):
        """Disable interaction highlight effect"""
        self.interaction_highlight = False
    
    def is_moving(self):
        """Check if player is currently moving"""
        return self.moving
    
    def get_facing_direction(self):
        """Get current facing direction"""
        return self.facing_direction
    
    def can_interact_at(self, target_x, target_y, max_distance=50):
        """Check if player can interact with object at position"""
        player_center = self.get_center_position()
        distance = math.sqrt((player_center[0] - target_x)**2 + (player_center[1] - target_y)**2)
        return distance <= max_distance
    
    def stop_movement(self):
        """Stop all movement"""
        for key in self.keys_pressed:
            self.keys_pressed[key] = False
        self.velocity_x = 0
        self.velocity_y = 0
        self.moving = False


# Backward compatibility - create alias for any existing code
class Player(EnhancedPlayer):
    """Backward compatibility alias"""
    pass
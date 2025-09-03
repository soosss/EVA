"""
===============================
EVANGELION MAIN MENU BACKGROUND
===============================
Creates EVA-themed animated background for main menu

FEATURES:
- 🌆 Tokyo-3 skyline silhouette
- 🔮 Floating geometric patterns (Angel-inspired)
- ⚡ Animated energy fields
- 🏢 NERV logo integration
- 🌙 Dynamic lighting effects
"""

import pygame
import math
import random
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenuBackground:
    """
    EVANGELION-THEMED BACKGROUND
    Animated background with EVA visual elements
    """
    
    def __init__(self):
        """Initialize animated background"""
        self.time = 0
        
        # === ANIMATION PARTICLES ===
        self.particles = []
        self.geometric_shapes = []
        self.energy_fields = []
        
        # === BACKGROUND LAYERS ===
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.midground_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.foreground_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # === INITIALIZE ELEMENTS ===
        self._create_background_layer()
        self._create_tokyo3_skyline()
        self._create_geometric_shapes()
        self._create_energy_fields()
        self._create_floating_particles()
        
        print("🎨 EVA Main Menu Background initialized")
    
    def _create_background_layer(self):
        """Create static background gradient"""
        # Deep space gradient (night sky over Tokyo-3)
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            
            # Color transition from dark purple to deep blue
            r = int(20 + (40 - 20) * ratio)
            g = int(20 + (30 - 20) * ratio)
            b = int(50 + (80 - 50) * ratio)
            
            color = (r, g, b)
            pygame.draw.line(self.background_surface, color, (0, y), (SCREEN_WIDTH, y))
        
        # Add subtle texture/noise
        for _ in range(200):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(60, 100)
            star_color = (brightness, brightness, brightness + 20)
            pygame.draw.circle(self.background_surface, star_color, (x, y), 1)
    
    def _create_tokyo3_skyline(self):
        """Create Tokyo-3 city silhouette"""
        # Building silhouettes
        buildings = [
            {"x": 0, "width": 80, "height": 150},
            {"x": 100, "width": 60, "height": 200},
            {"x": 180, "width": 90, "height": 120},
            {"x": 290, "width": 70, "height": 180},
            {"x": 380, "width": 100, "height": 160},
            {"x": 500, "width": 80, "height": 140},
            {"x": 600, "width": 120, "height": 190},
            {"x": 740, "width": 60, "height": 130}
        ]
        
        for building in buildings:
            building_rect = pygame.Rect(
                building["x"],
                SCREEN_HEIGHT - building["height"],
                building["width"],
                building["height"]
            )
            
            # Building silhouette
            pygame.draw.rect(self.background_surface, (25, 25, 35), building_rect)
            
            # Building windows (some lit up)
            for window_y in range(building_rect.top + 10, building_rect.bottom - 10, 15):
                for window_x in range(building_rect.left + 5, building_rect.right - 5, 12):
                    if random.random() < 0.3:  # 30% chance of lit window
                        window_color = random.choice([
                            (100, 150, 200),  # Cool blue
                            (150, 100, 200),  # Purple (NERV color)
                            (200, 150, 100)   # Warm yellow
                        ])
                        pygame.draw.rect(self.background_surface, window_color, 
                                       (window_x, window_y, 8, 10))
        
        # NERV Pyramid (iconic building)
        pyramid_base = 200
        pyramid_height = 100
        pyramid_x = SCREEN_WIDTH // 2 - pyramid_base // 2
        pyramid_y = SCREEN_HEIGHT - pyramid_height - 50
        
        pyramid_points = [
            (pyramid_x + pyramid_base // 2, pyramid_y),  # Top
            (pyramid_x, pyramid_y + pyramid_height),     # Bottom left
            (pyramid_x + pyramid_base, pyramid_y + pyramid_height)  # Bottom right
        ]
        
        pygame.draw.polygon(self.background_surface, (40, 20, 60), pyramid_points)
        pygame.draw.polygon(self.background_surface, COLORS['NERV_PURPLE'], pyramid_points, 2)
        
        # NERV logo on pyramid
        logo_font = pygame.font.Font(None, 24)
        logo_text = logo_font.render("NERV", True, COLORS['NERV_RED'])
        logo_rect = logo_text.get_rect(center=(pyramid_x + pyramid_base // 2, pyramid_y + pyramid_height // 2))
        self.background_surface.blit(logo_text, logo_rect)
    
    def _create_geometric_shapes(self):
        """Create floating Angel-inspired geometric shapes"""
        for _ in range(5):
            shape = {
                "type": random.choice(["octahedron", "hexagon", "triangle"]),
                "x": random.randint(100, SCREEN_WIDTH - 100),
                "y": random.randint(50, SCREEN_HEIGHT - 200),
                "size": random.randint(30, 80),
                "rotation": random.uniform(0, 2 * math.pi),
                "rotation_speed": random.uniform(-0.5, 0.5),
                "float_offset": random.uniform(0, 2 * math.pi),
                "float_amplitude": random.randint(20, 50),
                "alpha": random.randint(30, 80)
            }
            self.geometric_shapes.append(shape)
    
    def _create_energy_fields(self):
        """Create animated energy field effects"""
        for _ in range(3):
            field = {
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(0, SCREEN_HEIGHT),
                "radius": random.randint(80, 150),
                "pulse_phase": random.uniform(0, 2 * math.pi),
                "pulse_speed": random.uniform(1.0, 3.0),
                "color": random.choice([
                    COLORS['EVA_PURPLE'],
                    COLORS['HANGAR_BLUE'],
                    COLORS['NERV_RED']
                ])
            }
            self.energy_fields.append(field)
    
    def _create_floating_particles(self):
        """Create floating particle effects"""
        for _ in range(50):
            particle = {
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(0, SCREEN_HEIGHT),
                "vx": random.uniform(-20, 20),
                "vy": random.uniform(-30, -10),
                "size": random.randint(1, 3),
                "color": random.choice([
                    COLORS['TEXT_WHITE'],
                    COLORS['TERMINAL_GREEN'],
                    COLORS['EVA_PURPLE']
                ]),
                "life": random.uniform(5, 15),
                "max_life": 0
            }
            particle["max_life"] = particle["life"]
            self.particles.append(particle)
    
    def update(self, dt):
        """Update animated background elements"""
        self.time += dt
        
        # === UPDATE GEOMETRIC SHAPES ===
        for shape in self.geometric_shapes:
            shape["rotation"] += shape["rotation_speed"] * dt
            shape["y"] = shape["y"] + math.sin(self.time + shape["float_offset"]) * shape["float_amplitude"] * dt
        
        # === UPDATE ENERGY FIELDS ===
        for field in self.energy_fields:
            field["pulse_phase"] += field["pulse_speed"] * dt
        
        # === UPDATE PARTICLES ===
        for particle in self.particles[:]:
            particle["x"] += particle["vx"] * dt
            particle["y"] += particle["vy"] * dt
            particle["life"] -= dt
            
            # Wrap around screen
            if particle["x"] < 0:
                particle["x"] = SCREEN_WIDTH
            elif particle["x"] > SCREEN_WIDTH:
                particle["x"] = 0
            
            if particle["y"] < 0:
                particle["y"] = SCREEN_HEIGHT
            
            # Remove dead particles
            if particle["life"] <= 0:
                self.particles.remove(particle)
        
        # === ADD NEW PARTICLES ===
        if len(self.particles) < 30:
            self._add_new_particle()
    
    def _add_new_particle(self):
        """Add a new particle to the system"""
        particle = {
            "x": random.randint(0, SCREEN_WIDTH),
            "y": SCREEN_HEIGHT + 10,
            "vx": random.uniform(-20, 20),
            "vy": random.uniform(-30, -10),
            "size": random.randint(1, 3),
            "color": random.choice([
                COLORS['TEXT_WHITE'],
                COLORS['TERMINAL_GREEN'],
                COLORS['EVA_PURPLE']
            ]),
            "life": random.uniform(5, 15),
            "max_life": 0
        }
        particle["max_life"] = particle["life"]
        self.particles.append(particle)
    
    def render(self, screen):
        """Render complete animated background"""
        # === STATIC BACKGROUND ===
        screen.blit(self.background_surface, (0, 0))
        
        # === ANIMATED ENERGY FIELDS ===
        self._render_energy_fields(screen)
        
        # === FLOATING GEOMETRIC SHAPES ===
        self._render_geometric_shapes(screen)
        
        # === FLOATING PARTICLES ===
        self._render_particles(screen)
        
        # === ATMOSPHERIC EFFECTS ===
        self._render_atmospheric_effects(screen)
    
    def _render_energy_fields(self, screen):
        """Render animated energy fields"""
        for field in self.energy_fields:
            pulse_intensity = 0.5 + 0.5 * math.sin(field["pulse_phase"])
            current_radius = int(field["radius"] * (0.8 + 0.4 * pulse_intensity))
            alpha = int(40 + 40 * pulse_intensity)
            
            # Create energy field surface
            field_surface = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
            
            # Draw concentric circles for energy effect
            for i in range(3):
                circle_radius = current_radius - i * 10
                circle_alpha = alpha - i * 10
                if circle_radius > 0 and circle_alpha > 0:
                    color_with_alpha = (*field["color"], circle_alpha)
                    pygame.draw.circle(field_surface, field["color"], 
                                     (current_radius, current_radius), circle_radius, 2)
            
            # Blit field to screen
            field_rect = field_surface.get_rect(center=(field["x"], field["y"]))
            field_surface.set_alpha(alpha)
            screen.blit(field_surface, field_rect)
    
    def _render_geometric_shapes(self, screen):
        """Render floating geometric shapes"""
        for shape in self.geometric_shapes:
            shape_surface = pygame.Surface((shape["size"] * 2, shape["size"] * 2), pygame.SRCALPHA)
            center = (shape["size"], shape["size"])
            
            if shape["type"] == "octahedron":
                # Draw diamond/octahedron
                points = []
                for i in range(8):
                    angle = i * math.pi / 4 + shape["rotation"]
                    x = center[0] + shape["size"] * 0.7 * math.cos(angle)
                    y = center[1] + shape["size"] * 0.7 * math.sin(angle)
                    points.append((x, y))
                
                pygame.draw.polygon(shape_surface, COLORS['EVA_PURPLE'], points)
                pygame.draw.polygon(shape_surface, COLORS['TEXT_WHITE'], points, 2)
            
            elif shape["type"] == "hexagon":
                # Draw hexagon
                points = []
                for i in range(6):
                    angle = i * math.pi / 3 + shape["rotation"]
                    x = center[0] + shape["size"] * 0.8 * math.cos(angle)
                    y = center[1] + shape["size"] * 0.8 * math.sin(angle)
                    points.append((x, y))
                
                pygame.draw.polygon(shape_surface, COLORS['HANGAR_BLUE'], points)
                pygame.draw.polygon(shape_surface, COLORS['TEXT_WHITE'], points, 2)
            
            elif shape["type"] == "triangle":
                # Draw triangle
                points = []
                for i in range(3):
                    angle = i * 2 * math.pi / 3 + shape["rotation"]
                    x = center[0] + shape["size"] * math.cos(angle)
                    y = center[1] + shape["size"] * math.sin(angle)
                    points.append((x, y))
                
                pygame.draw.polygon(shape_surface, COLORS['NERV_RED'], points)
                pygame.draw.polygon(shape_surface, COLORS['TEXT_WHITE'], points, 2)
            
            # Apply floating position
            float_y = shape["y"] + math.sin(self.time + shape["float_offset"]) * shape["float_amplitude"]
            
            # Blit shape to screen
            shape_surface.set_alpha(shape["alpha"])
            shape_rect = shape_surface.get_rect(center=(shape["x"], float_y))
            screen.blit(shape_surface, shape_rect)
    
    def _render_particles(self, screen):
        """Render floating particles"""
        for particle in self.particles:
            # Calculate alpha based on remaining life
            life_ratio = particle["life"] / particle["max_life"]
            alpha = int(255 * life_ratio)
            
            if alpha > 0:
                # Create particle surface with alpha
                particle_surface = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, particle["color"], 
                                 (particle["size"], particle["size"]), particle["size"])
                particle_surface.set_alpha(alpha)
                
                particle_rect = particle_surface.get_rect(center=(particle["x"], particle["y"]))
                screen.blit(particle_surface, particle_rect)
    
    def _render_atmospheric_effects(self, screen):
        """Render atmospheric lighting and effects"""
        # Subtle vignette effect
        vignette_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        for i in range(100):
            alpha = i * 2
            if alpha > 255:
                alpha = 255
            
            color = (20, 20, 40, alpha)
            pygame.draw.rect(vignette_surface, color, (i, i, SCREEN_WIDTH - i * 2, SCREEN_HEIGHT - i * 2), 1)
        
        vignette_surface.set_alpha(30)
        screen.blit(vignette_surface, (0, 0))
        
        # Subtle scan lines effect
        for y in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.line(screen, (40, 40, 60, 20), (0, y), (SCREEN_WIDTH, y))
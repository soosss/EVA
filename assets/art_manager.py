"""
===============================
ART ASSET MANAGER (WITH ANGELS)
===============================
Complete art system including Angel enemies
"""

import pygame
import os
import math
from config import COLORS

class ArtManager:
    """
    ART MANAGER CLASS
    Manages all game artwork including Angels
    """
    
    def __init__(self):
        """Initialize art manager"""
        self.assets = {}
        self.default_assets = {}
        self.asset_folders = {
            'characters': 'assets/art/characters/',
            'angels': 'assets/art/angels/',           # Added Angels folder
            'backgrounds': 'assets/art/backgrounds/',
            'ui': 'assets/art/ui/',
            'portraits': 'assets/art/portraits/',
            'icons': 'assets/art/icons/',
            'effects': 'assets/art/effects/',
            'eva_units': 'assets/art/eva_units/'       # Added EVA Units folder
        }
        
        # Create asset directories
        self._create_asset_directories()
        
        # Generate default pixel art (including Angels)
        self._generate_default_art()
        
        # Load custom art
        self._load_custom_art()
        
        print("🎨 Art Manager initialized with Angels and EVA Units")
    
    def _create_readme(self, path, folder_type):
        """Create README files for each asset folder"""
        instructions = {
            'characters': """
CHARACTER ART FOLDER
===================
Place character sprites here with these naming conventions:

- shinji.png (main character)
- asuka.png (Asuka Langley)
- rei.png (Rei Ayanami)  
- misato.png (Misato Katsuragi)
- gendo.png (Gendo Ikari)
- ritsuko.png (Dr. Ritsuko Akagi)
- maya.png (Maya Ibuki)
- kaji.png (Ryoji Kaji)

Recommended size: 64x64 pixels or 32x48 pixels
Supported formats: PNG, JPG, BMP
""",
            'angels': """
ANGEL ENEMIES FOLDER
===================
Place Angel enemy sprites here:

- sachiel.png (First Angel)
- shamshel.png (Second Angel)
- ramiel.png (Third Angel - geometric)
- gaghiel.png (Fourth Angel - aquatic)
- israfel.png (Fifth Angel - twin)
- sandalphon.png (Sixth Angel)
- matarael.png (Seventh Angel)
- sahaquiel.png (Eighth Angel)
- ireul.png (Ninth Angel)
- leliel.png (Tenth Angel)
- bardiel.png (Eleventh Angel)
- zeruel.png (Twelfth Angel)
- arael.png (Thirteenth Angel)
- armisael.png (Fourteenth Angel)
- tabris.png (Fifteenth Angel - Kaworu)

- tutorial_angel.png (for tutorial battles)
- angel_core.png (Angel core/weak point)
- at_field_effect.png (AT Field visual effect)

Recommended size: 80x120 pixels for humanoid Angels
                  120x120 pixels for geometric Angels
Special note: Angels should be larger than characters
""",
            'eva_units': """
EVA UNITS FOLDER
===============
Place Evangelion Unit sprites here:

- eva_01.png (EVA Unit-01 - Purple)
- eva_00.png (EVA Unit-00 - Blue/Orange)
- eva_02.png (EVA Unit-02 - Red)
- eva_03.png (EVA Unit-03 - Black)
- eva_04.png (EVA Unit-04)

- eva_01_berserk.png (Unit-01 Berserk mode)
- eva_01_damaged.png (Damaged state)

Combat poses:
- eva_01_attack.png (attacking pose)
- eva_01_defend.png (defensive pose)
- eva_01_idle.png (standing pose)

Recommended size: 64x96 pixels
Note: EVAs should be larger than human characters
""",
            'backgrounds': """
BACKGROUND ART FOLDER
====================
Place background images here:

- bedroom_bg.png (apartment bedroom)
- nerv_hq_bg.png (NERV headquarters)
- tokyo3_bg.png (city view)
- school_bg.png (school interior)
- combat_bg.png (battle scenes)
- angel_battle_bg.png (Angel combat arena)
- eva_hangar_bg.png (EVA storage hangar)
- command_center_bg.png (NERV command center)

Recommended size: 800x600 pixels (or your screen resolution)
""",
            'portraits': """
PORTRAIT ART FOLDER
==================
Place character portrait images here for dialogue:

Human Characters:
- shinji_portrait.png
- asuka_portrait.png  
- rei_portrait.png
- misato_portrait.png
- gendo_portrait.png
- ritsuko_portrait.png

Angel Portraits (for special encounters):
- tabris_portrait.png (Kaworu)
- adam_portrait.png (Adam)
- lilith_portrait.png (Lilith)

Recommended size: 128x128 pixels or 96x96 pixels
""",
            'effects': """
EFFECTS FOLDER
=============
Place visual effect images here:

Combat Effects:
- attack_effect.png
- parry_effect.png
- explosion.png
- progressive_knife.png
- positron_rifle_beam.png

Angel Effects:
- at_field.png (AT Field barrier)
- angel_beam.png (Angel energy attacks)
- cross_explosion.png (Angel death explosion)
- lance_of_longinus.png

EVA Effects:
- sync_effect.png (synchronization visual)
- berserk_aura.png (berserk mode effect)
- eva_roar_effect.png

These will be used for combat and special effects
Size: Various (effects can be any size needed)
""",
            'ui': """
UI ART FOLDER
============
Place UI elements here:

- hud_background.png
- dialogue_box.png
- menu_background.png
- button_normal.png
- button_hover.png
- sync_meter.png
- health_bar.png
- angel_detected_alert.png

Custom UI elements will automatically replace defaults
""",
            'icons': """
ICONS FOLDER
===========
Place small icon images here:

Character Stats:
- health_icon.png
- energy_icon.png
- sync_icon.png
- experience_icon.png
- stress_icon.png

Combat Icons:
- attack_icon.png
- defend_icon.png
- eva_icon.png
- angel_icon.png

Recommended size: 16x16 or 32x32 pixels
"""
        }
        
        with open(path, 'w') as f:
            f.write(instructions.get(folder_type, "Place your art files here."))
    
    def _generate_default_art(self):
        """Generate default pixel art including Angels"""
        print("🎨 Generating default pixel art (including Angels)...")
        
        # === CHARACTER SPRITES ===
        self.default_assets['shinji'] = self._create_character_sprite((101, 67, 33), (50, 50, 100))
        self.default_assets['asuka'] = self._create_character_sprite((255, 140, 0), (255, 0, 0))
        self.default_assets['rei'] = self._create_character_sprite((200, 200, 255), (255, 255, 255))
        self.default_assets['misato'] = self._create_character_sprite((75, 0, 130), (128, 0, 128))
        self.default_assets['gendo'] = self._create_character_sprite((101, 67, 33), (20, 20, 20))
        self.default_assets['ritsuko'] = self._create_character_sprite((255, 215, 0), (255, 255, 255))
        
        # === CHARACTER PORTRAITS ===
        self.default_assets['shinji_portrait'] = self._create_portrait((101, 67, 33), (50, 50, 100))
        self.default_assets['asuka_portrait'] = self._create_portrait((255, 140, 0), (255, 0, 0))
        self.default_assets['rei_portrait'] = self._create_portrait((200, 200, 255), (255, 255, 255))
        self.default_assets['misato_portrait'] = self._create_portrait((75, 0, 130), (128, 0, 128))
        
        # === ANGEL SPRITES ===
        self.default_assets['sachiel'] = self._create_angel_sachiel()
        self.default_assets['shamshel'] = self._create_angel_shamshel()
        self.default_assets['ramiel'] = self._create_angel_ramiel()
        self.default_assets['tutorial_angel'] = self._create_tutorial_angel()
        self.default_assets['angel_core'] = self._create_angel_core()
        
        # === EVA UNIT SPRITES ===
        self.default_assets['eva_01'] = self._create_eva_unit((128, 0, 128), "01")  # Purple
        self.default_assets['eva_00'] = self._create_eva_unit((0, 100, 200), "00")   # Blue
        self.default_assets['eva_02'] = self._create_eva_unit((200, 0, 0), "02")     # Red
        
        # === BACKGROUNDS ===
        self.default_assets['bedroom_bg'] = self._create_bedroom_background()
        self.default_assets['nerv_hq_bg'] = self._create_nerv_background()
        self.default_assets['tokyo3_bg'] = self._create_city_background()
        self.default_assets['combat_bg'] = self._create_combat_background()
        self.default_assets['angel_battle_bg'] = self._create_angel_battle_background()
        
        # === EFFECTS ===
        self.default_assets['at_field'] = self._create_at_field_effect()
        self.default_assets['attack_effect'] = self._create_attack_effect()
        self.default_assets['explosion'] = self._create_explosion_effect()
        
        # === UI ELEMENTS ===
        self.default_assets['dialogue_box'] = self._create_dialogue_box()
        self.default_assets['hud_panel'] = self._create_hud_panel()
        
        # === ICONS ===
        self.default_assets['health_icon'] = self._create_health_icon()
        self.default_assets['energy_icon'] = self._create_energy_icon()
        self.default_assets['sync_icon'] = self._create_sync_icon()
        self.default_assets['angel_icon'] = self._create_angel_icon()
        
        print("✅ Default pixel art generated (including Angels and EVAs)")
    
    def _create_angel_sachiel(self, size=(80, 120)):
        """Create Sachiel (First Angel) sprite"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Body (humanoid)
        body_color = (100, 50, 150)  # Dark purple
        body_rect = pygame.Rect(size[0]//2 - 20, size[1]//2 - 30, 40, 60)
        pygame.draw.ellipse(surface, body_color, body_rect)
        
        # Head/Face mask
        head_rect = pygame.Rect(size[0]//2 - 15, size[1]//2 - 50, 30, 30)
        pygame.draw.ellipse(surface, (80, 30, 120), head_rect)
        
        # Eyes (glowing)
        eye_color = (255, 100, 100)  # Red glow
        left_eye = pygame.Rect(head_rect.centerx - 8, head_rect.centery - 3, 6, 6)
        right_eye = pygame.Rect(head_rect.centerx + 2, head_rect.centery - 3, 6, 6)
        pygame.draw.ellipse(surface, eye_color, left_eye)
        pygame.draw.ellipse(surface, eye_color, right_eye)
        
        # Arms
        arm_width = 12
        arm_height = 40
        left_arm = pygame.Rect(body_rect.left - arm_width, body_rect.top + 10, arm_width, arm_height)
        right_arm = pygame.Rect(body_rect.right, body_rect.top + 10, arm_width, arm_height)
        pygame.draw.rect(surface, body_color, left_arm)
        pygame.draw.rect(surface, body_color, right_arm)
        
        # Legs
        leg_width = 15
        leg_height = 35
        left_leg = pygame.Rect(body_rect.left + 5, body_rect.bottom, leg_width, leg_height)
        right_leg = pygame.Rect(body_rect.right - leg_width - 5, body_rect.bottom, leg_width, leg_height)
        pygame.draw.rect(surface, body_color, left_leg)
        pygame.draw.rect(surface, body_color, right_leg)
        
        # AT Field outline
        pygame.draw.ellipse(surface, (200, 100, 255), body_rect.inflate(10, 10), 2)
        
        return surface
    
    def _create_angel_shamshel(self, size=(80, 120)):
        """Create Shamshel (Second Angel) sprite"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Central body
        body_color = (150, 100, 50)  # Brown/tan
        body_rect = pygame.Rect(size[0]//2 - 12, size[1]//2 - 20, 24, 40)
        pygame.draw.ellipse(surface, body_color, body_rect)
        
        # Whip-like arms
        whip_color = (200, 150, 100)
        
        # Left whip arm (curved)
        for i in range(8):
            segment_x = body_rect.left - 5 - i * 3
            segment_y = body_rect.centery + math.sin(i * 0.5) * 10
            segment_rect = pygame.Rect(segment_x, int(segment_y), 8, 6)
            pygame.draw.ellipse(surface, whip_color, segment_rect)
        
        # Right whip arm (curved)
        for i in range(8):
            segment_x = body_rect.right - 3 + i * 3
            segment_y = body_rect.centery + math.sin(i * 0.5 + math.pi) * 10
            segment_rect = pygame.Rect(segment_x, int(segment_y), 8, 6)
            pygame.draw.ellipse(surface, whip_color, segment_rect)
        
        # Core
        core_rect = pygame.Rect(body_rect.centerx - 4, body_rect.centery - 4, 8, 8)
        pygame.draw.ellipse(surface, (255, 100, 100), core_rect)
        
        return surface
    
    def _create_angel_ramiel(self, size=(120, 120)):
        """Create Ramiel (Third Angel) sprite - geometric"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Octahedral shape
        center_x, center_y = size[0]//2, size[1]//2
        
        # Main body (diamond/octahedron)
        points = [
            (center_x, center_y - 40),  # Top
            (center_x + 30, center_y),  # Right
            (center_x, center_y + 40),  # Bottom
            (center_x - 30, center_y)   # Left
        ]
        
        # Main body
        pygame.draw.polygon(surface, (100, 150, 255), points)
        
        # Inner structure
        inner_points = [
            (center_x, center_y - 20),
            (center_x + 15, center_y),
            (center_x, center_y + 20),
            (center_x - 15, center_y)
        ]
        pygame.draw.polygon(surface, (150, 200, 255), inner_points)
        
        # Core
        core_rect = pygame.Rect(center_x - 6, center_y - 6, 12, 12)
        pygame.draw.ellipse(surface, (255, 255, 100), core_rect)
        
        # Geometric details
        pygame.draw.polygon(surface, (200, 220, 255), points, 2)
        
        # Energy field
        for radius in [45, 50, 55]:
            pygame.draw.circle(surface, (100, 150, 255, 50), (center_x, center_y), radius, 1)
        
        return surface
    
    def _create_tutorial_angel(self, size=(60, 80)):
        """Create a smaller, simpler Angel for tutorial"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Simple humanoid shape
        body_color = (80, 80, 120)
        body_rect = pygame.Rect(size[0]//2 - 10, size[1]//2 - 15, 20, 30)
        pygame.draw.ellipse(surface, body_color, body_rect)
        
        # Head
        head_rect = pygame.Rect(size[0]//2 - 8, size[1]//2 - 35, 16, 16)
        pygame.draw.ellipse(surface, (100, 100, 140), head_rect)
        
        # Simple eyes
        eye_color = (255, 200, 200)
        pygame.draw.circle(surface, eye_color, (head_rect.centerx - 3, head_rect.centery), 2)
        pygame.draw.circle(surface, eye_color, (head_rect.centerx + 3, head_rect.centery), 2)
        
        # Arms
        pygame.draw.rect(surface, body_color, (body_rect.left - 6, body_rect.top + 5, 6, 20))
        pygame.draw.rect(surface, body_color, (body_rect.right, body_rect.top + 5, 6, 20))
        
        # Legs
        pygame.draw.rect(surface, body_color, (body_rect.left + 2, body_rect.bottom, 6, 15))
        pygame.draw.rect(surface, body_color, (body_rect.right - 8, body_rect.bottom, 6, 15))
        
        return surface
    
    def _create_angel_core(self, size=(24, 24)):
        """Create Angel core/weak point"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Pulsing red core
        center = (size[0]//2, size[1]//2)
        
        # Outer glow
        for radius in [12, 10, 8]:
            alpha = 100 - (radius - 8) * 20
            color = (255, 100, 100, alpha)
            pygame.draw.circle(surface, color[:3], center, radius)
        
        # Inner core
        pygame.draw.circle(surface, (255, 50, 50), center, 6)
        pygame.draw.circle(surface, (255, 200, 200), center, 3)
        
        return surface
    
    def _create_eva_unit(self, color, unit_number, size=(64, 96)):
        """Create EVA Unit sprite"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Body
        body_rect = pygame.Rect(size[0]//2 - 16, size[1]//2 - 20, 32, 50)
        pygame.draw.rect(surface, color, body_rect)
        
        # Head
        head_rect = pygame.Rect(size[0]//2 - 12, size[1]//2 - 45, 24, 24)
        pygame.draw.ellipse(surface, color, head_rect)
        
        # Eyes (EVA style)
        eye_color = (100, 255, 100)  # Green
        left_eye = pygame.Rect(head_rect.centerx - 6, head_rect.centery - 2, 4, 8)
        right_eye = pygame.Rect(head_rect.centerx + 2, head_rect.centery - 2, 4, 8)
        pygame.draw.ellipse(surface, eye_color, left_eye)
        pygame.draw.ellipse(surface, eye_color, right_eye)
        
        # Arms
        arm_width = 10
        arm_height = 35
        left_arm = pygame.Rect(body_rect.left - arm_width, body_rect.top + 5, arm_width, arm_height)
        right_arm = pygame.Rect(body_rect.right, body_rect.top + 5, arm_width, arm_height)
        pygame.draw.rect(surface, color, left_arm)
        pygame.draw.rect(surface, color, right_arm)
        
        # Legs
        leg_width = 12
        leg_height = 30
        left_leg = pygame.Rect(body_rect.left + 4, body_rect.bottom, leg_width, leg_height)
        right_leg = pygame.Rect(body_rect.right - leg_width - 4, body_rect.bottom, leg_width, leg_height)
        pygame.draw.rect(surface, color, left_leg)
        pygame.draw.rect(surface, color, right_leg)
        
        # Unit number
        font = pygame.font.Font(None, 16)
        number_text = font.render(f"EVA-{unit_number}", True, (255, 255, 255))
        number_rect = number_text.get_rect(center=(size[0]//2, body_rect.bottom + 10))
        surface.blit(number_text, number_rect)
        
        # Armor details
        pygame.draw.rect(surface, (255, 255, 255), body_rect, 2)
        
        return surface
    
    def _create_angel_battle_background(self, size=(800, 600)):
        """Create Angel battle background"""
        surface = pygame.Surface(size)
        
        # Dark, ominous sky
        for y in range(size[1]//2):
            ratio = y / (size[1]//2)
            color = (
                int(20 + (60 - 20) * ratio),
                int(20 + (40 - 20) * ratio),
                int(40 + (80 - 40) * ratio)
            )
            pygame.draw.line(surface, color, (0, y), (size[0], y))
        
        # Destroyed cityscape
        ground_rect = pygame.Rect(0, size[1]//2, size[0], size[1]//2)
        pygame.draw.rect(surface, (60, 40, 40), ground_rect)
        
        # Ruined buildings
        for i in range(6):
            building_x = i * 130 + 20
            building_height = 40 + (i % 3) * 20
            building_rect = pygame.Rect(building_x, size[1]//2 - building_height, 100, building_height)
            
            # Damaged building
            pygame.draw.rect(surface, (80, 60, 60), building_rect)
            pygame.draw.rect(surface, (100, 80, 80), building_rect, 1)
            
            # Damage/holes
            for j in range(3):
                hole_x = building_x + 10 + j * 30
                hole_y = building_rect.top + 10 + (j % 2) * 15
                hole_rect = pygame.Rect(hole_x, hole_y, 15, 15)
                pygame.draw.rect(surface, (40, 20, 20), hole_rect)
        
        # Smoke/clouds
        for i in range(8):
            cloud_x = i * 100
            cloud_y = 50 + (i % 3) * 30
            pygame.draw.circle(surface, (60, 60, 80, 100), (cloud_x, cloud_y), 30)
        
        return surface
    
    def _create_at_field_effect(self, size=(100, 100)):
        """Create AT Field visual effect"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        center = (size[0]//2, size[1]//2)
        
        # Hexagonal energy field
        radius = 40
        for i in range(6):
            angle1 = i * math.pi / 3
            angle2 = (i + 1) * math.pi / 3
            
            x1 = center[0] + radius * math.cos(angle1)
            y1 = center[1] + radius * math.sin(angle1)
            x2 = center[0] + radius * math.cos(angle2)
            y2 = center[1] + radius * math.sin(angle2)
            
            pygame.draw.line(surface, (255, 100, 255, 150), (x1, y1), (x2, y2), 3)
        
        # Inner energy
        pygame.draw.circle(surface, (255, 150, 255, 100), center, 25)
        
        return surface
    
    def _create_attack_effect(self, size=(60, 20)):
        """Create attack effect"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Energy slash
        for i in range(3):
            width = 6 - i * 2
            color_intensity = 255 - i * 60
            color = (100, color_intensity, 100)
            pygame.draw.rect(surface, color, (0, size[1]//2 - width//2, size[0], width))
        
        return surface
    
    def _create_explosion_effect(self, size=(80, 80)):
        """Create explosion effect"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        center = (size[0]//2, size[1]//2)
        
        # Multiple explosion rings
        for radius in [35, 25, 15]:
            alpha = 200 - radius * 4
            color = (255, 200 - radius * 3, 100 - radius * 2, alpha)
            pygame.draw.circle(surface, color[:3], center, radius)
        
        return surface
    
    def _create_angel_icon(self, size=(24, 24)):
        """Create Angel detection icon"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Warning triangle
        points = [
            (size[0]//2, 2),
            (2, size[1] - 2),
            (size[0] - 2, size[1] - 2)
        ]
        pygame.draw.polygon(surface, COLORS['NERV_RED'], points)
        
        # Exclamation mark
        pygame.draw.rect(surface, (255, 255, 255), (size[0]//2 - 1, 6, 2, 10))
        pygame.draw.rect(surface, (255, 255, 255), (size[0]//2 - 1, size[1] - 6, 2, 2))
        
        return surface
    
    # ... (keep all other existing methods from previous art manager)
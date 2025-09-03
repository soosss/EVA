"""
===============================
ENHANCED MOUSE CONTROLLER - RESTORED
===============================
Complete mouse control with all advanced features restored

FEATURES:
- ✅ Hover descriptions for all interactables
- ✅ Boundary-aware movement (no HUD overlap)
- ✅ Smooth hover detection with timing
- ✅ Visual feedback and highlighting
- ✅ Multiple interaction modes
- ✅ Combat mode support
"""

import pygame
import math
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT

class MouseController:
    """
    COMPLETE ENHANCED MOUSE CONTROLLER
    All advanced features restored and improved
    """
    
    def __init__(self, game_manager):
        """Initialize enhanced mouse controller"""
        self.game_manager = game_manager
        
        # Mouse state
        self.mouse_pos = (0, 0)
        self.left_clicked = False
        self.right_clicked = False
        
        # Movement
        self.target_position = None
        self.moving_to_target = False
        
        # Combat mode
        self.combat_mode = False
        
        # === ENHANCED HOVER SYSTEM ===
        self.hover_target = None
        self.hover_description = ""
        self.hover_timer = 0
        self.hover_delay = 0.6  # Show description after 0.6 seconds
        self.show_hover_description = False
        self.hover_fade_alpha = 0
        self.hover_animation_timer = 0
        
        # Interaction range
        self.interaction_range = 80
        
        # === PLAYABLE AREA (HUD boundary aware) ===
        self.hud_width = 220
        self.playable_left = 10
        self.playable_right = SCREEN_WIDTH - self.hud_width - 10
        self.playable_top = 10
        self.playable_bottom = SCREEN_HEIGHT - 10
        
        # === VISUAL FEEDBACK ===
        self.interaction_highlights = []
        self.cursor_animation_timer = 0
        self.last_interaction_time = 0
        
        print("🖱️ Enhanced Mouse Controller with all features restored")
    
    def set_combat_mode(self, combat_mode):
        """Set combat mode for mouse controller"""
        self.combat_mode = combat_mode
        print(f"🖱️ Combat mode: {'ON' if combat_mode else 'OFF'}")
    
    def handle_event(self, event, scene):
        """Handle mouse events with full feature set"""
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self._update_hover_target(scene)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.left_clicked = True
                # Check if clicking in HUD area
                if event.pos[0] > self.playable_right:
                    print("🖱️ Click in HUD area ignored")
                    return
                self._handle_left_click(event.pos, scene)
            elif event.button == 3:  # Right click
                self.right_clicked = True
                self._handle_right_click(event.pos, scene)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.left_clicked = False
            elif event.button == 3:
                self.right_clicked = False
    
    def _handle_left_click(self, pos, scene):
        """Handle left mouse click with enhanced interaction"""
        # Clamp position to playable area
        clamped_pos = (
            max(self.playable_left, min(self.playable_right, pos[0])),
            max(self.playable_top, min(self.playable_bottom, pos[1]))
        )
        
        if self.combat_mode:
            # Combat attack
            if hasattr(scene, 'player_attack'):
                scene.player_attack(clamped_pos)
        else:
            # Movement or interaction
            interacted = self._try_interact_at_position(clamped_pos, scene)
            if not interacted:
                self._move_to_position(clamped_pos)
                self._add_interaction_highlight(clamped_pos, "move")
    
    def _handle_right_click(self, pos, scene):
        """Handle right mouse click with examination"""
        if self.combat_mode:
            # Combat parry/defend
            if hasattr(scene, 'player_parry'):
                scene.player_parry()
        else:
            # Examine/inspect
            self._examine_at_position(pos, scene)
            self._add_interaction_highlight(pos, "examine")
    
    def _try_interact_at_position(self, pos, scene):
        """Try to interact with something at the clicked position"""
        # Check NPCs first
        if hasattr(scene, 'npcs'):
            for npc in scene.npcs:
                if self._is_position_near_npc(pos, npc):
                    self._interact_with_npc(npc, scene)
                    self._add_interaction_highlight(pos, "npc")
                    return True
        
        # Check single NPC (like Asuka in bedroom)
        if hasattr(scene, 'asuka') and scene.asuka_present and not scene.asuka_left_room:
            if self._is_position_near_npc(pos, scene.asuka):
                self._interact_with_npc(scene.asuka, scene)
                self._add_interaction_highlight(pos, "npc")
                return True
        
        # Check areas
        if hasattr(scene, 'hub_areas'):
            for area in scene.hub_areas:
                if area['rect'].collidepoint(pos):
                    self._interact_with_area(area, scene)
                    self._add_interaction_highlight(pos, "area")
                    return True
        
        # Check town areas
        if hasattr(scene, 'areas'):
            for area in scene.areas:
                if area['rect'].collidepoint(pos):
                    self._interact_with_area(area, scene)
                    self._add_interaction_highlight(pos, "area")
                    return True
        
        # Check furniture (bedroom scene)
        if hasattr(scene, 'furniture'):
            for item in scene.furniture:
                if item['rect'].collidepoint(pos):
                    self._interact_with_furniture(item, scene)
                    self._add_interaction_highlight(pos, "furniture")
                    return True
        
        # Check door (bedroom scene)
        if hasattr(scene, 'door_rect') and hasattr(scene, 'can_exit_room'):
            if scene.door_rect.collidepoint(pos):
                if scene.can_exit_room and hasattr(scene, '_exit_room'):
                    scene._exit_room()
                    self._add_interaction_highlight(pos, "door")
                    return True
                else:
                    scene.status_manager.show_status("Door is locked. Talk to Asuka first.", "warning", 2.0)
                    return True
        
        return False
    
    def _examine_at_position(self, pos, scene):
        """Examine something at the clicked position with detailed info"""
        examined = False
        
        # Check NPCs
        if hasattr(scene, 'npcs'):
            for npc in scene.npcs:
                if self._is_position_near_npc(pos, npc):
                    scene.status_manager.show_status(f"🔍 {npc.name}: {npc.description}", "info", 4.0)
                    examined = True
                    break
        
        # Check single NPCs
        if not examined and hasattr(scene, 'asuka') and scene.asuka_present:
            if self._is_position_near_npc(pos, scene.asuka):
                scene.status_manager.show_status(f"🔍 {scene.asuka.name}: {scene.asuka.description}", "info", 4.0)
                examined = True
        
        # Check areas
        if not examined and hasattr(scene, 'areas'):
            for area in scene.areas:
                if area['rect'].collidepoint(pos):
                    description = area.get('description', f"This is the {area['name']} area.")
                    scene.status_manager.show_status(f"🔍 {area['name']}: {description}", "info", 4.0)
                    examined = True
                    break
        
        # Check furniture
        if not examined and hasattr(scene, 'furniture'):
            for item in scene.furniture:
                if item['rect'].collidepoint(pos):
                    scene.status_manager.show_status(f"🔍 {item['name']}: {item['description']}", "info", 4.0)
                    examined = True
                    break
        
        # Check door
        if not examined and hasattr(scene, 'door_rect'):
            if scene.door_rect.collidepoint(pos):
                if hasattr(scene, 'can_exit_room') and scene.can_exit_room:
                    scene.status_manager.show_status("🔍 Exit Door: Leave the room and head to NERV headquarters.", "info", 3.0)
                else:
                    scene.status_manager.show_status("🔍 Exit Door: The door is locked. You need to talk to Asuka first.", "info", 3.0)
                examined = True
        
        if not examined:
            scene.status_manager.show_status("🔍 Nothing particularly interesting here.", "info", 2.0)
    
    def _move_to_position(self, pos):
        """Set movement target within playable area"""
        # Ensure target is within playable boundaries
        clamped_pos = (
            max(self.playable_left + 25, min(self.playable_right - 25, pos[0])),
            max(self.playable_top + 25, min(self.playable_bottom - 25, pos[1]))
        )
        
        self.target_position = clamped_pos
        self.moving_to_target = True
    
    def _update_hover_target(self, scene):
        """Update what we're hovering over with enhanced descriptions"""
        old_target = self.hover_target
        self.hover_target = None
        self.hover_description = ""
        
        # Check if mouse is in playable area
        if (self.mouse_pos[0] > self.playable_right or 
            self.mouse_pos[0] < self.playable_left or
            self.mouse_pos[1] < self.playable_top or 
            self.mouse_pos[1] > self.playable_bottom):
            self.show_hover_description = False
            self.hover_timer = 0
            return
        
        # Check NPCs with enhanced descriptions
        if hasattr(scene, 'npcs'):
            for npc in scene.npcs:
                if self._is_position_near_npc(self.mouse_pos, npc):
                    self.hover_target = ('npc', npc)
                    # Enhanced NPC descriptions with context
                    context = self._get_npc_context(npc, scene)
                    self.hover_description = f"💬 {npc.name}\n{npc.description}\n{context}"
                    break
        
        # Check single NPCs (bedroom Asuka)
        if not self.hover_target and hasattr(scene, 'asuka') and scene.asuka_present and not scene.asuka_left_room:
            if self._is_position_near_npc(self.mouse_pos, scene.asuka):
                self.hover_target = ('npc', scene.asuka)
                if not scene.talked_to_asuka:
                    self.hover_description = f"💬 {scene.asuka.name}\n{scene.asuka.description}\n💡 Click to wake up and talk"
                else:
                    self.hover_description = f"💬 {scene.asuka.name}\nShe's getting ready to leave."
        
        # Check areas with enhanced descriptions
        if not self.hover_target and hasattr(scene, 'areas'):
            for area in scene.areas:
                if area['rect'].collidepoint(self.mouse_pos):
                    self.hover_target = ('area', area)
                    description = area.get('description', f"Enter the {area['name']}")
                    self.hover_description = f"🏢 {area['name']}\n{description}\n💡 Click to enter"
                    break
        
        # Check furniture with enhanced descriptions
        if not self.hover_target and hasattr(scene, 'furniture'):
            for item in scene.furniture:
                if item['rect'].collidepoint(self.mouse_pos):
                    self.hover_target = ('furniture', item)
                    usage_hint = self._get_furniture_usage_hint(item)
                    self.hover_description = f"🛋️ {item['name']}\n{item['description']}\n{usage_hint}"
                    break
        
        # Check door with enhanced description
        if not self.hover_target and hasattr(scene, 'door_rect'):
            if scene.door_rect.collidepoint(self.mouse_pos):
                self.hover_target = ('door', None)
                if hasattr(scene, 'can_exit_room') and scene.can_exit_room:
                    self.hover_description = "🚪 Exit Door\nLeave for NERV headquarters\n💡 Click to exit"
                else:
                    self.hover_description = "🚪 Exit Door\nCurrently locked\n💡 Talk to Asuka first"
        
        # Reset hover timer if target changed
        if old_target != self.hover_target:
            self.hover_timer = 0
            self.show_hover_description = False
            self.hover_fade_alpha = 0
    
    def _get_npc_context(self, npc, scene):
        """Get contextual information about NPC"""
        if hasattr(scene, 'game_manager'):
            player_data = scene.game_manager.get_player_data()
            if hasattr(player_data, 'relationships') and npc.name in player_data.relationships:
                relationship = player_data.relationships[npc.name]
                return f"💝 Relationship: {relationship}/100"
        return "💡 Click to interact"
    
    def _get_furniture_usage_hint(self, item):
        """Get usage hint for furniture"""
        hints = {
            'Bed': "💡 Click to examine",
            'Study Desk': "💡 Click to study",
            'SDAT Player': "💡 Click to listen to music (-stress)",
            'Closet': "💡 Click to get dressed",
            'Bookshelf': "💡 Click to read"
        }
        return hints.get(item['name'], "💡 Click to interact")
    
    def _add_interaction_highlight(self, pos, interaction_type):
        """Add visual highlight for interactions"""
        colors = {
            "move": COLORS['TERMINAL_GREEN'],
            "npc": COLORS['SCHOOL_YELLOW'],
            "furniture": COLORS['HANGAR_BLUE'],
            "area": COLORS['EVA_PURPLE'],
            "door": COLORS['WARNING_ORANGE'],
            "examine": COLORS['TEXT_WHITE']
        }
        
        highlight = {
            "pos": pos,
            "color": colors.get(interaction_type, COLORS['TEXT_WHITE']),
            "timer": 1.0,
            "max_timer": 1.0,
            "type": interaction_type
        }
        
        self.interaction_highlights.append(highlight)
        self.last_interaction_time = pygame.time.get_ticks()
    
    def _interact_with_npc(self, npc, scene):
        """Interact with an NPC"""
        if hasattr(scene, '_start_dialogue'):
            scene._start_dialogue(npc)
        elif hasattr(scene, '_start_enhanced_dialogue'):
            scene._start_enhanced_dialogue(npc)
        elif hasattr(scene, '_talk_to_asuka') and npc == getattr(scene, 'asuka', None):
            scene._talk_to_asuka()
        else:
            scene.status_manager.show_status(f"💬 Talking to {npc.name}", "info", 2.0)
    
    def _interact_with_area(self, area, scene):
        """Interact with an area"""
        destination = area.get('destination')
        if destination and hasattr(scene, 'scene_manager'):
            scene.scene_manager.change_scene(destination)
        else:
            scene.status_manager.show_status(f"🏢 Accessing {area['name']}...", "info", 2.0)
    
    def _interact_with_furniture(self, item, scene):
        """Interact with furniture"""
        if hasattr(scene, '_try_interact_furniture'):
            scene._try_interact_furniture()
        else:
            scene.status_manager.show_status(f"🛋️ Using {item['name']}", "info", 2.0)
    
    def _is_position_near_npc(self, pos, npc):
        """Check if position is near an NPC"""
        distance = math.sqrt((pos[0] - npc.x)**2 + (pos[1] - npc.y)**2)
        return distance <= self.interaction_range
    
    def update_player_movement(self, player, dt):
        """Update player movement toward target with boundaries"""
        if not self.moving_to_target or not self.target_position:
            return
        
        # Use player's boundary-aware movement
        reached_target = player.move_to_position(self.target_position[0], self.target_position[1], dt)
        
        if reached_target:
            self.moving_to_target = False
            self.target_position = None
    
    def update(self, dt):
        """Update mouse controller including enhanced hover system"""
        # Update hover timer with fade effects
        if self.hover_target and not self.show_hover_description:
            self.hover_timer += dt
            if self.hover_timer >= self.hover_delay:
                self.show_hover_description = True
        elif not self.hover_target:
            self.hover_timer = 0
            self.show_hover_description = False
        
        # Update hover fade animation
        if self.show_hover_description:
            self.hover_fade_alpha = min(255, self.hover_fade_alpha + dt * 500)
        else:
            self.hover_fade_alpha = max(0, self.hover_fade_alpha - dt * 300)
        
        # Update hover animation
        self.hover_animation_timer += dt
        
        # Update cursor animation
        self.cursor_animation_timer += dt
        
        # Update interaction highlights
        for highlight in self.interaction_highlights[:]:
            highlight["timer"] -= dt
            if highlight["timer"] <= 0:
                self.interaction_highlights.remove(highlight)
    
    def render_mouse_ui(self, screen):
        """Render mouse UI elements with all enhancements"""
        # === INTERACTION HIGHLIGHTS ===
        self._render_interaction_highlights(screen)
        
        # === CURSOR ===
        self._render_enhanced_cursor(screen)
        
        # === HOVER INDICATOR ===
        if self.hover_target:
            self._render_hover_indicator(screen)
        
        # === MOVEMENT TARGET ===
        if self.moving_to_target and self.target_position:
            self._render_movement_target(screen)
        
        # === HOVER DESCRIPTION ===
        if self.show_hover_description and self.hover_description and self.hover_fade_alpha > 0:
            self._render_enhanced_hover_description(screen)
    
    def _render_interaction_highlights(self, screen):
        """Render interaction highlights"""
        for highlight in self.interaction_highlights:
            alpha_ratio = highlight["timer"] / highlight["max_timer"]
            alpha = int(255 * alpha_ratio)
            
            if alpha > 0:
                # Create highlight surface
                highlight_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
                color_with_alpha = (*highlight["color"], alpha)
                
                # Different shapes for different interactions
                if highlight["type"] == "move":
                    pygame.draw.circle(highlight_surface, color_with_alpha, (15, 15), 12, 3)
                elif highlight["type"] == "npc":
                    pygame.draw.rect(highlight_surface, color_with_alpha, (5, 5, 20, 20), 3)
                else:
                    pygame.draw.circle(highlight_surface, color_with_alpha, (15, 15), 10, 2)
                
                # Blit to screen
                highlight_rect = highlight_surface.get_rect(center=highlight["pos"])
                screen.blit(highlight_surface, highlight_rect)
    
    def _render_enhanced_cursor(self, screen):
        """Render enhanced cursor with animations"""
        import math
        
        if self.combat_mode:
            # Combat cursor
            pulse = 1.0 + 0.3 * math.sin(self.cursor_animation_timer * 8)
            size = int(10 * pulse)
            pygame.draw.circle(screen, COLORS['NERV_RED'], self.mouse_pos, size, 2)
            
            # Crosshairs
            offset = size + 5
            pygame.draw.line(screen, COLORS['NERV_RED'], 
                           (self.mouse_pos[0] - offset, self.mouse_pos[1]), 
                           (self.mouse_pos[0] + offset, self.mouse_pos[1]), 2)
            pygame.draw.line(screen, COLORS['NERV_RED'],
                           (self.mouse_pos[0], self.mouse_pos[1] - offset),
                           (self.mouse_pos[0], self.mouse_pos[1] + offset), 2)
        else:
            # Check if mouse is in playable area
            if (self.playable_left <= self.mouse_pos[0] <= self.playable_right and
                self.playable_top <= self.mouse_pos[1] <= self.playable_bottom):
                
                # Interactive cursor with pulse
                if self.hover_target:
                    pulse = 1.0 + 0.2 * math.sin(self.cursor_animation_timer * 6)
                    cursor_color = COLORS['SCHOOL_YELLOW']
                    cursor_size = int(8 * pulse)
                else:
                    cursor_color = COLORS['TERMINAL_GREEN']
                    cursor_size = 6
                
                pygame.draw.circle(screen, cursor_color, self.mouse_pos, cursor_size, 2)
                
                # Add small dot in center
                pygame.draw.circle(screen, cursor_color, self.mouse_pos, 2)
                
            else:
                # Outside playable area cursor
                cursor_color = COLORS['UI_GRAY']
                cursor_size = 4
                pygame.draw.circle(screen, cursor_color, self.mouse_pos, cursor_size, 2)
    
    def _render_hover_indicator(self, screen):
        """Render hover indicators with enhanced visuals"""
        target_type, target_obj = self.hover_target
        
        # Pulsing effect
        import math
        pulse = 1.0 + 0.3 * math.sin(self.hover_animation_timer * 4)
        
        if target_type == 'npc':
            # Highlight NPC with animated circle
            radius = int(40 * pulse)
            pygame.draw.circle(screen, COLORS['SCHOOL_YELLOW'], (int(target_obj.x), int(target_obj.y)), radius, 3)
            
            # Add sparkle effect
            for i in range(3):
                angle = self.hover_animation_timer * 2 + i * (math.pi * 2 / 3)
                sparkle_x = target_obj.x + math.cos(angle) * 50
                sparkle_y = target_obj.y + math.sin(angle) * 50
                pygame.draw.circle(screen, COLORS['SCHOOL_YELLOW'], (int(sparkle_x), int(sparkle_y)), 3)
        
        elif target_type == 'area':
            # Highlight area with animated border
            border_width = int(4 * pulse)
            pygame.draw.rect(screen, COLORS['HANGAR_BLUE'], target_obj['rect'], border_width)
        
        elif target_type == 'furniture':
            # Highlight furniture with glow effect
            glow_rect = target_obj['rect'].inflate(int(10 * pulse), int(10 * pulse))
            pygame.draw.rect(screen, COLORS['TERMINAL_GREEN'], glow_rect, 3)
        
        elif target_type == 'door':
            # Highlight door with special effect
            if hasattr(self, '_last_door_rect'):
                door_rect = self._last_door_rect
                for i in range(3):
                    glow_rect = door_rect.inflate(i * int(6 * pulse), i * int(6 * pulse))
                    alpha = 100 - i * 30
                    glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
                    pygame.draw.rect(glow_surface, (*COLORS['SCHOOL_YELLOW'], alpha), glow_surface.get_rect(), 2)
                    screen.blit(glow_surface, glow_rect.topleft)
    
    def _render_movement_target(self, screen):
        """Render movement target with enhanced animation"""
        import math
        
        # Animated target indicator
        pulse = 1.0 + 0.5 * math.sin(self.cursor_animation_timer * 6)
        
        # Outer ring
        outer_radius = int(12 * pulse)
        pygame.draw.circle(screen, COLORS['TERMINAL_GREEN'], self.target_position, outer_radius, 2)
        
        # Inner dot
        pygame.draw.circle(screen, COLORS['TERMINAL_GREEN'], self.target_position, 4)
        
        # Directional lines
        for i in range(4):
            angle = i * math.pi / 2 + self.cursor_animation_timer * 2
            line_start = (
                self.target_position[0] + math.cos(angle) * 8,
                self.target_position[1] + math.sin(angle) * 8
            )
            line_end = (
                self.target_position[0] + math.cos(angle) * 15,
                self.target_position[1] + math.sin(angle) * 15
            )
            pygame.draw.line(screen, COLORS['TERMINAL_GREEN'], line_start, line_end, 2)
    
    def _render_enhanced_hover_description(self, screen):
        """Render enhanced hover description with animations"""
        if not self.hover_description:
            return
        
        # Parse multi-line description
        lines = self.hover_description.split('\n')
        
        # Calculate box size
        description_font = pygame.font.Font(None, 16)
        line_height = 18
        max_width = 0
        
        for line in lines:
            line_width = description_font.size(line)[0]
            max_width = max(max_width, line_width)
        
        box_width = min(max_width + 20, 300)
        box_height = len(lines) * line_height + 20
        
        # Position box near mouse but keep it on screen and away from HUD
        box_x = self.mouse_pos[0] + 20
        box_y = self.mouse_pos[1] - box_height - 15
        
        # Keep box in playable area
        if box_x + box_width > self.playable_right:
            box_x = self.mouse_pos[0] - box_width - 20
        if box_y < self.playable_top:
            box_y = self.mouse_pos[1] + 25
        if box_x < self.playable_left:
            box_x = self.playable_left
        
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        # Create description surface with fade
        desc_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        
        # Background with transparency
        bg_alpha = int(self.hover_fade_alpha * 0.9)
        pygame.draw.rect(desc_surface, (25, 25, 45, bg_alpha), desc_surface.get_rect())
        pygame.draw.rect(desc_surface, (*COLORS['SCHOOL_YELLOW'], self.hover_fade_alpha), desc_surface.get_rect(), 2)
        
        # Add subtle gradient
        for i in range(box_height // 4):
            gradient_alpha = int(bg_alpha * (1 - i / (box_height // 4)) * 0.3)
            if gradient_alpha > 0:
                pygame.draw.line(desc_surface, (100, 100, 150, gradient_alpha), 
                               (0, i), (box_width, i))
        
        # Render text lines
        for i, line in enumerate(lines):
            text_alpha = int(self.hover_fade_alpha)
            
            # Different colors for different line types
            if line.startswith('💬') or line.startswith('🏢'):
                text_color = COLORS['SCHOOL_YELLOW']
            elif line.startswith('💡'):
                text_color = COLORS['TERMINAL_GREEN']
            elif line.startswith('💝'):
                text_color = COLORS['EVA_PURPLE']
            else:
                text_color = COLORS['TEXT_WHITE']
            
            text_surface = description_font.render(line, True, text_color)
            
            # Apply alpha to text
            if text_alpha < 255:
                alpha_text_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
                alpha_text_surface.blit(text_surface, (0, 0))
                alpha_text_surface.set_alpha(text_alpha)
                desc_surface.blit(alpha_text_surface, (10, 10 + i * line_height))
            else:
                desc_surface.blit(text_surface, (10, 10 + i * line_height))
        
        # Blit to screen
        screen.blit(desc_surface, box_rect.topleft)
        
        # Add subtle glow effect around box
        if self.hover_fade_alpha > 200:
            glow_rect = box_rect.inflate(6, 6)
            glow_alpha = int((self.hover_fade_alpha - 200) * 0.5)
            pygame.draw.rect(screen, (*COLORS['SCHOOL_YELLOW'], glow_alpha), glow_rect, 1)
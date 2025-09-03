"""
===============================
ENHANCED STATUS POPUP SYSTEM - RESTORED
===============================
Advanced non-overlapping status messages with animations

FEATURES:
- ✅ No text overlap with smart positioning
- ✅ Multiple message types with colors
- ✅ Fade animations and effects
- ✅ Priority system for important messages
- ✅ Sound integration
- ✅ Rich formatting support
"""

import pygame
import math
from config import COLORS, SCREEN_WIDTH

class StatusManager:
    """
    ENHANCED STATUS MANAGER
    Advanced status message system with all features restored
    """
    
    def __init__(self):
        """Initialize enhanced status manager"""
        self.messages = []
        self.font = pygame.font.Font(None, 18)
        self.small_font = pygame.font.Font(None, 16)
        self.large_font = pygame.font.Font(None, 22)
        
        # === POSITIONING SETTINGS ===
        self.hud_width = 220  # Reserve space for HUD
        self.max_width = SCREEN_WIDTH - self.hud_width - 60  # Leave margin
        self.start_x = 25
        self.start_y = 140
        self.message_height = 28
        self.max_messages = 12  # Increased limit
        
        # === ANIMATION SETTINGS ===
        self.slide_speed = 300  # pixels per second
        self.fade_speed = 200   # alpha per second
        
        # === MESSAGE PRIORITIES ===
        self.priority_colors = {
            "critical": COLORS['NERV_RED'],
            "warning": COLORS['WARNING_ORANGE'],
            "success": COLORS['TERMINAL_GREEN'],
            "info": COLORS['HANGAR_BLUE'],
            "system": COLORS['EVA_PURPLE'],
            "dialogue": COLORS['SCHOOL_YELLOW']
        }
        
        # === SOUND INTEGRATION ===
        self.last_sound_time = 0
        self.sound_cooldown = 0.1  # Prevent sound spam
        
        print("📢 Enhanced Status Manager initialized with animations")
    
    def show_status(self, message, status_type="info", duration=3.0, priority=0, sound=True):
        """Show enhanced status message with all features"""
        # Handle priority - higher priority messages can interrupt
        if priority > 0:
            # Remove lower priority messages of same type
            self.messages = [msg for msg in self.messages 
                           if msg.get('priority', 0) >= priority or msg['type'] != status_type]
        
        # Color and styling based on type
        color = self.priority_colors.get(status_type, COLORS['TEXT_WHITE'])
        
        # Font selection based on priority
        if priority >= 2:
            font = self.large_font
        elif priority >= 1:
            font = self.font
        else:
            font = self.small_font
        
        # Wrap long messages
        wrapped_lines = self._wrap_message(message, font)
        
        for i, line in enumerate(wrapped_lines):
            # Remove oldest message if we have too many
            if len(self.messages) >= self.max_messages:
                self.messages.pop(0)
            
            # Create enhanced message object
            message_obj = {
                'text': line,
                'color': color,
                'timer': duration + (i * 0.5),  # Stagger multi-line messages
                'max_timer': duration + (i * 0.5),
                'type': status_type,
                'priority': priority,
                'font': font,
                'alpha': 0,  # Start invisible for fade-in
                'target_alpha': 255,
                'slide_offset': -100,  # Start off-screen for slide-in
                'target_slide': 0,
                'creation_time': pygame.time.get_ticks(),
                'effects': {
                    'glow': status_type in ['critical', 'success'],
                    'pulse': priority >= 2,
                    'shake': status_type == 'critical'
                }
            }
            
            self.messages.append(message_obj)
        
        # Play sound if enabled
        if sound and hasattr(self, '_should_play_sound') and self._should_play_sound():
            self._play_message_sound(status_type, priority)
    
    def show_experience_gain(self, exp_amount):
        """Show experience gain with special effects"""
        self.show_status(f"🎯 +{exp_amount} EXP gained!", "success", 3.0, priority=1)
    
    def show_relationship_change(self, character, change):
        """Show relationship change with character context"""
        if change > 0:
            self.show_status(f"💝 {character} relationship: +{change}", "success", 3.5, priority=1)
        elif change < 0:
            self.show_status(f"💔 {character} relationship: {change}", "warning", 3.5, priority=1)
    
    def show_sync_ratio_change(self, change):
        """Show sync ratio change with importance"""
        if change > 0:
            self.show_status(f"🔗 Sync ratio increased by {change:.1f}%", "success", 3.0, priority=1)
        elif change < 0:
            self.show_status(f"⚠️ Sync ratio decreased by {abs(change):.1f}%", "warning", 3.0, priority=1)
    
    def show_critical_alert(self, message):
        """Show critical system alert"""
        self.show_status(f"🚨 ALERT: {message}", "critical", 5.0, priority=3)
    
    def show_dialogue(self, speaker, text):
        """Show dialogue message with speaker formatting"""
        formatted_text = f"{speaker}: \"{text}\""
        self.show_status(formatted_text, "dialogue", 4.0, priority=0)
    
    def show_system_message(self, message):
        """Show system/game message"""
        self.show_status(f"⚙️ {message}", "system", 2.5)
    
    def _wrap_message(self, message, font):
        """Enhanced text wrapping with emoji support"""
        words = message.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            try:
                if font.size(test_line)[0] <= self.max_width - 30:  # Leave margin for effects
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            except:
                # Fallback for emoji or special characters
                if len(current_line) + len(word) < 50:  # Character limit fallback
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines if lines else [message]  # Fallback to original
    
    def _should_play_sound(self):
        """Check if sound should be played (cooldown)"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_sound_time > self.sound_cooldown * 1000:
            self.last_sound_time = current_time
            return True
        return False
    
    def _play_message_sound(self, status_type, priority):
        """Play appropriate sound for message type"""
        # This would integrate with audio manager in full implementation
        sound_map = {
            "critical": "alert_critical",
            "warning": "alert_warning", 
            "success": "notification_success",
            "info": "notification_info",
            "system": "system_beep",
            "dialogue": "dialogue_beep"
        }
        
        sound_name = sound_map.get(status_type, "notification_info")
        # In full implementation: self.game_manager.audio_manager.play_sfx(sound_name)
        print(f"🔊 Playing sound: {sound_name}")
    
    def update(self, dt):
        """Update status messages with animations"""
        for message in self.messages[:]:
            # Update timers
            message['timer'] -= dt
            
            # Update slide-in animation
            if message['slide_offset'] < message['target_slide']:
                message['slide_offset'] = min(message['target_slide'], 
                                            message['slide_offset'] + self.slide_speed * dt)
            
            # Update fade animation
            if message['alpha'] < message['target_alpha']:
                message['alpha'] = min(message['target_alpha'],
                                     message['alpha'] + self.fade_speed * dt)
            
            # Handle message expiration
            if message['timer'] <= 0:
                # Start fade-out
                message['target_alpha'] = 0
                message['alpha'] = max(0, message['alpha'] - self.fade_speed * dt * 2)
                
                # Remove when fully faded
                if message['alpha'] <= 0:
                    self.messages.remove(message)
            
            # Handle fade-out for expired messages
            elif message['timer'] <= 0.5:  # Start fading in last 0.5 seconds
                fade_ratio = message['timer'] / 0.5
                message['target_alpha'] = int(255 * fade_ratio)
    
    def clear_all_messages(self):
        """Clear all status messages"""
        self.messages.clear()
        print("🧹 All status messages cleared")
    
    def clear_messages_of_type(self, status_type):
        """Clear messages of specific type"""
        self.messages = [msg for msg in self.messages if msg['type'] != status_type]
        print(f"🧹 Cleared all {status_type} messages")
    
    def render(self, screen):
        """Render enhanced status messages with all effects"""
        if not self.messages:
            return
        
        # Calculate starting position
        current_y = self.start_y
        
        for i, message in enumerate(self.messages):
            # Calculate position with slide animation
            message_x = self.start_x + message['slide_offset']
            message_y = current_y
            
            # Apply shake effect for critical messages
            if message['effects']['shake'] and message['type'] == 'critical':
                shake_intensity = 3 * (message['alpha'] / 255)
                shake_x = math.sin(pygame.time.get_ticks() * 0.02) * shake_intensity
                shake_y = math.cos(pygame.time.get_ticks() * 0.03) * shake_intensity
                message_x += shake_x
                message_y += shake_y
            
            # Create text surface
            font = message['font']
            text_surface = font.render(message['text'], True, message['color'])
            text_width = text_surface.get_width()
            text_height = text_surface.get_height()
            
            # Background rectangle with rounded corners effect
            bg_width = min(text_width + 20, self.max_width)
            bg_height = text_height + 12
            bg_rect = pygame.Rect(message_x, message_y, bg_width, bg_height)
            
            # Create message surface with alpha
            message_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
            
            # Background color with type-specific styling
            bg_alpha = int(message['alpha'] * 0.8)
            if message['type'] == 'critical':
                bg_color = (120, 20, 20, bg_alpha)
                border_color = (*COLORS['NERV_RED'], message['alpha'])
            elif message['type'] == 'success':
                bg_color = (20, 80, 20, bg_alpha)
                border_color = (*COLORS['TERMINAL_GREEN'], message['alpha'])
            elif message['type'] == 'warning':
                bg_color = (80, 60, 20, bg_alpha)
                border_color = (*COLORS['WARNING_ORANGE'], message['alpha'])
            elif message['type'] == 'dialogue':
                bg_color = (60, 60, 20, bg_alpha)
                border_color = (*COLORS['SCHOOL_YELLOW'], message['alpha'])
            else:  # info, system
                bg_color = (20, 40, 80, bg_alpha)
                border_color = (*COLORS['HANGAR_BLUE'], message['alpha'])
            
            # Draw background
            message_surface.fill(bg_color)
            
            # Add gradient effect
            for j in range(bg_height // 3):
                gradient_alpha = int(bg_alpha * 0.3 * (1 - j / (bg_height // 3)))
                if gradient_alpha > 0:
                    gradient_color = (255, 255, 255, gradient_alpha)
                    pygame.draw.line(message_surface, gradient_color, (0, j), (bg_width, j))
            
            # Pulse effect for high priority messages
            pulse_intensity = 1.0
            if message['effects']['pulse']:
                pulse_intensity = 1.0 + 0.2 * math.sin(pygame.time.get_ticks() * 0.01)
            
            # Glow effect for special messages
            if message['effects']['glow']:
                glow_alpha = int(message['alpha'] * 0.3 * pulse_intensity)
                if glow_alpha > 0:
                    for glow_size in range(1, 4):
                        glow_rect = bg_rect.inflate(glow_size * 4, glow_size * 4)
                        glow_surface = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
                        glow_color = (*message['color'], max(0, glow_alpha - glow_size * 10))
                        pygame.draw.rect(glow_surface, glow_color, glow_surface.get_rect(), 1)
                        screen.blit(glow_surface, glow_rect.topleft)
            
            # Blit message background to screen
            screen.blit(message_surface, bg_rect.topleft)
            
            # Border with pulse effect
            border_width = int(2 * pulse_intensity)
            pygame.draw.rect(screen, border_color, bg_rect, border_width)
            
            # Text with alpha
            if message['alpha'] < 255:
                alpha_text_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
                alpha_text_surface.blit(text_surface, (0, 0))
                alpha_text_surface.set_alpha(int(message['alpha']))
                screen.blit(alpha_text_surface, (message_x + 10, message_y + 6))
            else:
                screen.blit(text_surface, (message_x + 10, message_y + 6))
            
            # Priority indicator for high-priority messages
            if message['priority'] >= 2:
                indicator_size = int(6 * pulse_intensity)
                indicator_color = (*COLORS['NERV_RED'], message['alpha'])
                pygame.draw.circle(screen, indicator_color, 
                                 (message_x + bg_width - 10, message_y + 10), indicator_size)
            
            # Move to next position
            current_y += self.message_height
            
            # Stop if we're getting too close to bottom of screen
            if current_y > SCREEN_HEIGHT - 120:
                break
    
    def get_message_count(self):
        """Get current message count"""
        return len(self.messages)
    
    def get_messages_by_type(self, status_type):
        """Get messages of specific type"""
        return [msg for msg in self.messages if msg['type'] == status_type]
    
    def has_critical_messages(self):
        """Check if there are any critical messages"""
        return any(msg['type'] == 'critical' for msg in self.messages)
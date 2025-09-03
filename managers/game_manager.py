"""
===============================
GAME MANAGER - COMPLETE WITH ALL METHODS
===============================
Enhanced game manager with all required functionality
"""

import pygame
import json
import os
from datetime import datetime

# Add proper imports for screen dimensions and config
try:
    from config import (COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, 
                       PLAYER_START_HEALTH, PLAYER_START_SYNC_RATIO, 
                       PLAYER_START_STRESS, PLAYER_START_RELATIONSHIPS)
except ImportError:
    from config import COLORS
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PLAYER_START_HEALTH = 100
    PLAYER_START_SYNC_RATIO = 50.0
    PLAYER_START_STRESS = 30
    PLAYER_START_RELATIONSHIPS = {
        "Asuka": 30, "Rei": 20, "Misato": 50, "Gendo": 10, "Shinji": 40
    }

class GameManager:
    """
    COMPLETE ENHANCED GAME MANAGER
    All methods required by enhanced systems
    """
    
    def __init__(self):
        """Initialize enhanced game manager"""
        # === CORE GAME STATE ===
        self.game_running = True
        self.paused = False
        self.scene_manager = None  # Will be set by game engine
        
        # === PLAYER STATS ===
        self.player_stats = {
            "health": PLAYER_START_HEALTH,
            "sync_ratio": PLAYER_START_SYNC_RATIO,
            "stress_level": PLAYER_START_STRESS,
            "level": 1,
            "experience": 0,
            "mood": "neutral"
        }
        
        # === RELATIONSHIPS ===
        self.relationships = PLAYER_START_RELATIONSHIPS.copy()
        
        # === GAME PROGRESS ===
        self.story_flags = {
            "tutorial_complete": False,
            "first_angel_defeated": False,
            "bedroom_complete": False,
            "nerv_briefing_complete": False,
            "asuka_met": False,
            "rei_met": False,
            "gendo_confronted": False
        }
        
        # === SAVE SYSTEM ===
        self.save_directory = "saves"
        self.current_save_slot = 1
        self.auto_save_enabled = True
        
        # === GAME SETTINGS ===
        self.game_settings = {
            "difficulty": "normal",
            "text_speed": 50,
            "auto_advance": False,
            "skip_read_text": False,
            "music_volume": 80,
            "sfx_volume": 90
        }
        
        # === INVENTORY SYSTEM ===
        self.inventory = {
            "items": [],
            "key_items": [],
            "max_items": 50
        }
        
        # === TIME SYSTEM ===
        self.game_time = {
            "day": 1,
            "hour": 8,
            "period": "morning"  # morning, afternoon, evening, night
        }
        
        # === ACHIEVEMENTS ===
        self.achievements = {
            "first_conversation": False,
            "max_sync_achieved": False,
            "all_characters_met": False,
            "first_angel_defeated": False
        }
        
        # Ensure save directory exists
        self._ensure_save_directory()
        
        print("🎮 Enhanced Game Manager initialized with all methods")
    
    def _ensure_save_directory(self):
        """Ensure save directory exists"""
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
    
    # === PLAYER STAT METHODS (REQUIRED BY ENHANCED SYSTEMS) ===
    
    def get_player_health(self):
        """Get current player health (0-100)"""
        return self.player_stats["health"]
    
    def set_player_health(self, health):
        """Set player health"""
        self.player_stats["health"] = max(0, min(100, health))
    
    def modify_player_health(self, amount):
        """Modify player health by amount"""
        self.player_stats["health"] = max(0, min(100, self.player_stats["health"] + amount))
        return self.player_stats["health"]
    
    def get_sync_ratio(self):
        """Get current sync ratio (0.0-100.0)"""
        return self.player_stats["sync_ratio"]
    
    def set_sync_ratio(self, sync_ratio):
        """Set sync ratio"""
        self.player_stats["sync_ratio"] = max(0.0, min(100.0, sync_ratio))
    
    def modify_sync_ratio(self, amount):
        """Modify sync ratio by amount"""
        self.player_stats["sync_ratio"] = max(0.0, min(100.0, self.player_stats["sync_ratio"] + amount))
        return self.player_stats["sync_ratio"]
    
    def get_stress_level(self):
        """Get current stress level (0-100)"""
        return self.player_stats["stress_level"]
    
    def set_stress_level(self, stress):
        """Set stress level"""
        self.player_stats["stress_level"] = max(0, min(100, stress))
    
    def modify_stress_level(self, amount):
        """Modify stress level by amount"""
        self.player_stats["stress_level"] = max(0, min(100, self.player_stats["stress_level"] + amount))
        return self.player_stats["stress_level"]
    
    def get_player_level(self):
        """Get current player level"""
        return self.player_stats["level"]
    
    def get_player_experience(self):
        """Get current player experience"""
        return self.player_stats["experience"]
    
    def add_experience(self, amount):
        """Add experience and handle level ups"""
        self.player_stats["experience"] += amount
        
        # Check for level up (every 100 exp)
        while self.player_stats["experience"] >= self.player_stats["level"] * 100:
            self.player_stats["experience"] -= self.player_stats["level"] * 100
            self.player_stats["level"] += 1
            self._handle_level_up()
    
    def _handle_level_up(self):
        """Handle level up effects"""
        # Increase health and sync ratio
        self.modify_player_health(10)
        self.modify_sync_ratio(5)
        print(f"🆙 Level up! Now level {self.player_stats['level']}")
    
    # === RELATIONSHIP METHODS ===
    
    def get_relationships(self):
        """Get all relationships"""
        return self.relationships.copy()
    
    def get_relationship(self, character):
        """Get relationship level with specific character"""
        return self.relationships.get(character, 0)
    
    def set_relationship(self, character, level):
        """Set relationship level with character"""
        self.relationships[character] = max(0, min(100, level))
    
    def modify_relationship(self, character, amount):
        """Modify relationship with character"""
        current = self.relationships.get(character, 0)
        self.relationships[character] = max(0, min(100, current + amount))
        
        # Check for achievements
        if self.relationships[character] >= 80:
            self._trigger_achievement(f"close_bond_{character.lower()}")
        
        return self.relationships[character]
    
    # === STORY PROGRESS METHODS ===
    
    def get_story_flag(self, flag_name):
        """Get story flag value"""
        return self.story_flags.get(flag_name, False)
    
    def set_story_flag(self, flag_name, value):
        """Set story flag"""
        self.story_flags[flag_name] = value
        
        # Trigger related events
        if flag_name == "first_angel_defeated" and value:
            self.add_experience(50)
            self._trigger_achievement("first_angel_defeated")
    
    def complete_story_milestone(self, milestone):
        """Complete a story milestone"""
        milestone_flags = {
            "tutorial": "tutorial_complete",
            "bedroom": "bedroom_complete",
            "nerv_briefing": "nerv_briefing_complete"
        }
        
        if milestone in milestone_flags:
            self.set_story_flag(milestone_flags[milestone], True)
            self.add_experience(25)
    
    # === INVENTORY METHODS ===
    
    def add_item(self, item_name, quantity=1):
        """Add item to inventory"""
        for item in self.inventory["items"]:
            if item["name"] == item_name:
                item["quantity"] += quantity
                return True
        
        if len(self.inventory["items"]) < self.inventory["max_items"]:
            self.inventory["items"].append({"name": item_name, "quantity": quantity})
            return True
        
        return False  # Inventory full
    
    def remove_item(self, item_name, quantity=1):
        """Remove item from inventory"""
        for item in self.inventory["items"]:
            if item["name"] == item_name:
                if item["quantity"] <= quantity:
                    self.inventory["items"].remove(item)
                else:
                    item["quantity"] -= quantity
                return True
        return False
    
    def has_item(self, item_name):
        """Check if player has item"""
        return any(item["name"] == item_name for item in self.inventory["items"])
    
    def get_item_quantity(self, item_name):
        """Get quantity of specific item"""
        for item in self.inventory["items"]:
            if item["name"] == item_name:
                return item["quantity"]
        return 0
    
    # === TIME SYSTEM METHODS ===
    
    def advance_time(self, hours=1):
        """Advance game time"""
        self.game_time["hour"] += hours
        
        while self.game_time["hour"] >= 24:
            self.game_time["hour"] -= 24
            self.game_time["day"] += 1
        
        # Update time period
        if 6 <= self.game_time["hour"] < 12:
            self.game_time["period"] = "morning"
        elif 12 <= self.game_time["hour"] < 18:
            self.game_time["period"] = "afternoon"
        elif 18 <= self.game_time["hour"] < 22:
            self.game_time["period"] = "evening"
        else:
            self.game_time["period"] = "night"
    
    def get_current_time_string(self):
        """Get formatted time string"""
        return f"Day {self.game_time['day']} - {self.game_time['hour']:02d}:00 ({self.game_time['period'].title()})"
    
    # === ACHIEVEMENT METHODS ===
    
    def _trigger_achievement(self, achievement_name):
        """Trigger achievement"""
        if achievement_name not in self.achievements:
            self.achievements[achievement_name] = False
        
        if not self.achievements[achievement_name]:
            self.achievements[achievement_name] = True
            print(f"🏆 Achievement unlocked: {achievement_name}")
    
    def check_achievement(self, achievement_name):
        """Check if achievement is unlocked"""
        return self.achievements.get(achievement_name, False)
    
    # === SAVE/LOAD METHODS ===
    
    def save_game(self, slot=None):
        """Save game to file"""
        if slot is None:
            slot = self.current_save_slot
        
        save_data = {
            "player_stats": self.player_stats,
            "relationships": self.relationships,
            "story_flags": self.story_flags,
            "inventory": self.inventory,
            "game_time": self.game_time,
            "achievements": self.achievements,
            "game_settings": self.game_settings,
            "save_timestamp": datetime.now().isoformat(),
            "current_scene": self.scene_manager.get_current_scene_name() if self.scene_manager else "main_menu"
        }
        
        save_file = os.path.join(self.save_directory, f"save_slot_{slot}.json")
        
        try:
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=4)
            print(f"💾 Game saved to slot {slot}")
            return True
        except Exception as e:
            print(f"❌ Error saving game: {e}")
            return False
    
    def load_game(self, slot=None):
        """Load game from file"""
        if slot is None:
            slot = self.current_save_slot
        
        save_file = os.path.join(self.save_directory, f"save_slot_{slot}.json")
        
        try:
            if os.path.exists(save_file):
                with open(save_file, 'r') as f:
                    save_data = json.load(f)
                
                # Load all data
                self.player_stats = save_data.get("player_stats", self.player_stats)
                self.relationships = save_data.get("relationships", self.relationships)
                self.story_flags = save_data.get("story_flags", self.story_flags)
                self.inventory = save_data.get("inventory", self.inventory)
                self.game_time = save_data.get("game_time", self.game_time)
                self.achievements = save_data.get("achievements", self.achievements)
                self.game_settings = save_data.get("game_settings", self.game_settings)
                
                print(f"📁 Game loaded from slot {slot}")
                
                # Change to saved scene if scene manager exists
                saved_scene = save_data.get("current_scene", "main_menu")
                if self.scene_manager and saved_scene != "main_menu":
                    self.scene_manager.change_scene(saved_scene)
                
                return True
            else:
                print(f"❌ No save file found in slot {slot}")
                return False
        except Exception as e:
            print(f"❌ Error loading game: {e}")
            return False
    
    def has_save_files(self):
        """Check if any save files exist"""
        for i in range(1, 6):  # Check slots 1-5
            save_file = os.path.join(self.save_directory, f"save_slot_{i}.json")
            if os.path.exists(save_file):
                return True
        return False
    
    def get_save_info(self, slot):
        """Get save file information"""
        save_file = os.path.join(self.save_directory, f"save_slot_{slot}.json")
        
        if os.path.exists(save_file):
            try:
                with open(save_file, 'r') as f:
                    save_data = json.load(f)
                
                return {
                    "exists": True,
                    "timestamp": save_data.get("save_timestamp", "Unknown"),
                    "level": save_data.get("player_stats", {}).get("level", 1),
                    "scene": save_data.get("current_scene", "Unknown"),
                    "day": save_data.get("game_time", {}).get("day", 1)
                }
            except:
                return {"exists": False}
        else:
            return {"exists": False}
    
    # === AUTO SAVE ===
    
    def auto_save(self):
        """Perform auto save"""
        if self.auto_save_enabled:
            return self.save_game(slot=0)  # Use slot 0 for auto save
        return False
    
    # === UTILITY METHODS ===
    
    def reset_game(self):
        """Reset game to initial state"""
        self.player_stats = {
            "health": PLAYER_START_HEALTH,
            "sync_ratio": PLAYER_START_SYNC_RATIO,
            "stress_level": PLAYER_START_STRESS,
            "level": 1,
            "experience": 0,
            "mood": "neutral"
        }
        self.relationships = PLAYER_START_RELATIONSHIPS.copy()
        self.story_flags = {flag: False for flag in self.story_flags}
        self.inventory = {"items": [], "key_items": [], "max_items": 50}
        self.game_time = {"day": 1, "hour": 8, "period": "morning"}
        self.achievements = {achievement: False for achievement in self.achievements}
    
    def get_game_stats_summary(self):
        """Get summary of game statistics"""
        return {
            "level": self.player_stats["level"],
            "health": self.player_stats["health"],
            "sync_ratio": self.player_stats["sync_ratio"],
            "stress": self.player_stats["stress_level"],
            "day": self.game_time["day"],
            "relationships_count": len([r for r in self.relationships.values() if r > 50]),
            "achievements_count": len([a for a in self.achievements.values() if a]),
            "story_progress": len([f for f in self.story_flags.values() if f])
        }
    
    # === GAME FLOW METHODS ===
    
    def pause_game(self):
        """Pause the game"""
        self.paused = True
    
    def resume_game(self):
        """Resume the game"""
        self.paused = False
    
    def is_paused(self):
        """Check if game is paused"""
        return self.paused
    
    def quit_game(self):
        """Quit the game"""
        if self.auto_save_enabled:
            self.auto_save()
        self.game_running = False
    
    def is_running(self):
        """Check if game is running"""
        return self.game_running
    
    # === DEBUG METHODS ===
    
    def debug_print_stats(self):
        """Print debug information"""
        print("=== GAME MANAGER DEBUG ===")
        print(f"Health: {self.player_stats['health']}")
        print(f"Sync Ratio: {self.player_stats['sync_ratio']}")
        print(f"Stress: {self.player_stats['stress_level']}")
        print(f"Level: {self.player_stats['level']}")
        print(f"Relationships: {self.relationships}")
        print(f"Story Flags: {self.story_flags}")
        print("========================")
    
    def get_player_data(self):
        """Get comprehensive player data object for save/load operations"""
        class PlayerData:
            def __init__(self, game_manager):
                self.level = game_manager.player_stats['level']
                self.experience = game_manager.player_stats['experience']
                self.sync_ratio = game_manager.player_stats['sync_ratio']
                self.health = game_manager.player_stats['health']
                self.stress_level = game_manager.player_stats['stress_level']
                self.current_mood = game_manager.player_stats['mood']
                self.relationships = game_manager.relationships.copy()
                self.inventory = game_manager.inventory['items'].copy()
                self.story_flags = game_manager.story_flags.copy()
                self.position = [400, 300]  # Default position
                self.battles_won = 0  # Could be tracked separately
                self.missions_completed = 0  # Could be tracked separately
                self.playtime = "00:00:00"  # Could be tracked separately
                self.total_playtime = 0  # Could be tracked separately
                self.scenes_visited = []  # Could be tracked separately
                self.choices_made = {}  # Could be tracked separately
        
        return PlayerData(self)
    
    def update(self, dt):
        """Update game manager (called every frame)"""
        # Update time tracking
        self.advance_time(0)  # Just update internal time without advancing game time
        
        # Could add other periodic updates here like:
        # - Auto-save timer
        # - Achievement checks
        # - Status effects
        pass
    
    def cleanup(self):
        """Clean up game manager resources"""
        # Save any pending data
        if hasattr(self, 'auto_save_enabled') and self.auto_save_enabled:
            try:
                self.auto_save()
            except Exception as e:
                print(f"⚠️ Auto-save during cleanup failed: {e}")
        
        # Reset state
        self.game_running = False
        print("🧹 Game Manager cleaned up")
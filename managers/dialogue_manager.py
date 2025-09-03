"""
===============================
DIALOGUE MANAGER
===============================
Manages dialogue loading and processing
"""

from data.dialogue_editor import DialogueEditor
import random

class DialogueManager:
    """
    DIALOGUE MANAGER CLASS
    Handles dialogue loading and character interactions
    """
    
    def __init__(self, game_manager):
        """Initialize dialogue manager"""
        self.game_manager = game_manager
        self.dialogue_editor = DialogueEditor()
        self.loaded_dialogues = {}
        self.reload_dialogues()
        
        print("💬 Dialogue Manager initialized")
    
    def reload_dialogues(self):
        """Reload all dialogues from files"""
        self.loaded_dialogues = self.dialogue_editor.get_all_dialogues()
        print(f"🔄 Loaded {len(self.loaded_dialogues)} dialogue files")
    
    def get_character_dialogues(self, character_name, scene_name=None):
        """Get dialogues for a specific character"""
        matching_dialogues = []
        
        for dialogue_key, dialogue_data in self.loaded_dialogues.items():
            if not dialogue_data:
                continue
                
            # Check character match
            if dialogue_data.get("character", "").lower() == character_name.lower():
                # Check scene match if specified
                if scene_name is None or dialogue_data.get("scene", "") == scene_name:
                    matching_dialogues.append(dialogue_data)
        
        return matching_dialogues
    
    def get_available_dialogue_lines(self, character_name, scene_name=None):
        """Get available dialogue lines based on conditions"""
        character_dialogues = self.get_character_dialogues(character_name, scene_name)
        available_lines = []
        
        for dialogue_set in character_dialogues:
            for dialogue in dialogue_set.get("dialogues", []):
                if self._check_conditions(dialogue.get("conditions", {})):
                    available_lines.append(dialogue)
        
        return available_lines
    
    def get_interaction_options(self, character_name, scene_name=None):
        """Get player interaction options for a character"""
        character_dialogues = self.get_character_dialogues(character_name, scene_name)
        options = []
        
        for dialogue_set in character_dialogues:
            for option in dialogue_set.get("interaction_options", []):
                if self._check_conditions(option.get("conditions", {})):
                    options.append(option)
        
        return options
    
    def _check_conditions(self, conditions):
        """Check if dialogue conditions are met"""
        if not conditions:
            return True
        
        try:
            player_data = self.game_manager.get_player_data()
            
            for condition_key, condition_value in conditions.items():
                if condition_key == "level":
                    if not self._check_numeric_condition(player_data.level, condition_value):
                        return False
                
                elif condition_key == "sync_ratio":
                    if not self._check_numeric_condition(player_data.sync_ratio, condition_value):
                        return False
                
                elif condition_key == "mood":
                    if player_data.current_mood != condition_value:
                        return False
                
                elif condition_key == "story_flag":
                    # Check story flags from scene manager
                    story_flags = self.game_manager.scene_manager.get_story_progress()
                    if not story_flags.get(condition_value, False):
                        return False
                
                elif condition_key == "time_of_day":
                    # Check time of day
                    current_hour = getattr(player_data, 'current_hour', 12)
                    time_of_day = self._get_time_of_day(current_hour)
                    if time_of_day != condition_value:
                        return False
        
        except Exception as e:
            print(f"⚠️ Condition check error: {e}")
            return False
        
        return True
    
    def _check_numeric_condition(self, value, condition):
        """Check numeric conditions like '>5', '=10', '<3'"""
        if condition.startswith('>'):
            return value > int(condition[1:])
        elif condition.startswith('<'):
            return value < int(condition[1:])
        elif condition.startswith('='):
            return value == int(condition[1:])
        else:
            return value == int(condition)
    
    def _get_time_of_day(self, hour):
        """Get time of day from hour"""
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        elif 18 <= hour < 22:
            return "evening"
        else:
            return "night"
    
    def apply_dialogue_effects(self, effects):
        """Apply effects from dialogue choices"""
        if not effects:
            return
        
        try:
            player_data = self.game_manager.get_player_data()
            
            for effect_key, effect_value in effects.items():
                if effect_key == "mood":
                    player_data.change_mood(effect_value, "Dialogue choice")
                
                elif effect_key == "stress":
                    player_data.stress_level = max(0, min(100, player_data.stress_level + effect_value))
                
                elif effect_key == "sync_ratio":
                    player_data.sync_ratio = max(0, min(100, player_data.sync_ratio + effect_value))
                
                elif effect_key == "experience":
                    player_data.gain_experience(effect_value)
                
                elif effect_key == "story_flag":
                    self.game_manager.scene_manager.set_story_flag(effect_value, True)
                
                elif effect_key == "advance_story":
                    if effect_value:
                        # Handle story advancement
                        print("📖 Story advanced through dialogue")
                
                elif effect_key == "relationship":
                    # Handle relationship changes
                    print(f"💝 Relationship changed by {effect_value}")
        
        except Exception as e:
            print(f"⚠️ Effect application error: {e}")
    
    def get_random_dialogue(self, character_name, scene_name=None):
        """Get a random dialogue line for a character"""
        available_lines = self.get_available_dialogue_lines(character_name, scene_name)
        if available_lines:
            return random.choice(available_lines)
        return None
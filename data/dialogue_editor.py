"""
===============================
DIALOGUE EDITOR SYSTEM
===============================
Easy system for editing and adding dialogue
"""

import json
import os
from datetime import datetime

class DialogueEditor:
    """
    DIALOGUE EDITOR CLASS
    Easy dialogue management and editing
    """
    
    def __init__(self):
        """Initialize dialogue editor"""
        self.data_folder = "data/dialogues/"
        self.backup_folder = "data/dialogues/backups/"
        
        # Create directories
        os.makedirs(self.data_folder, exist_ok=True)
        os.makedirs(self.backup_folder, exist_ok=True)
        
        # Initialize default dialogues
        self._create_default_dialogues()
        
        print("💬 Dialogue Editor initialized")
    
    def _create_default_dialogues(self):
        """Create default dialogue files"""
        default_dialogues = {
            "asuka_bedroom": {
                "character": "Asuka Langley Soryu",
                "scene": "bedroom",
                "mood": "energetic",
                "dialogues": [
                    {
                        "id": "wake_up_1",
                        "text": "Hey! Third Child! Wake up already!",
                        "conditions": {},
                        "effects": {"mood": "annoyed"}
                    },
                    {
                        "id": "wake_up_2", 
                        "text": "We're supposed to be at NERV in 30 minutes!",
                        "conditions": {},
                        "effects": {"stress": 5}
                    },
                    {
                        "id": "wake_up_3",
                        "text": "Misato's waiting and you know how she gets...",
                        "conditions": {},
                        "effects": {}
                    },
                    {
                        "id": "wake_up_4",
                        "text": "Come ON! Get out of bed!",
                        "conditions": {},
                        "effects": {"mood": "determined"}
                    }
                ],
                "interaction_options": [
                    {
                        "text": "I'm ready to go to NERV.",
                        "response": "Finally! Let's get going!",
                        "effects": {"advance_story": True}
                    },
                    {
                        "text": "What's the emergency about?",
                        "response": "Something about Angel detection. Misato will explain!",
                        "effects": {"info_gained": "angel_threat"}
                    },
                    {
                        "text": "Can I get dressed first?",
                        "response": "Make it quick! We're already late!",
                        "effects": {"time_pressure": True}
                    },
                    {
                        "text": "Why are you in my room?",
                        "response": "Misato sent me! Now stop asking questions and move!",
                        "effects": {"mood": "irritated"}
                    }
                ]
            },
            
            "misato_briefing": {
                "character": "Misato Katsuragi",
                "scene": "nerv_arrival",
                "mood": "serious",
                "dialogues": [
                    {
                        "id": "briefing_1",
                        "text": "Good, you're both here. We have a situation.",
                        "conditions": {},
                        "effects": {"tension": 10}
                    },
                    {
                        "id": "briefing_2",
                        "text": "Shinji, your sync rates have been improving, but we need to accelerate your training.",
                        "conditions": {},
                        "effects": {"confidence": 5}
                    },
                    {
                        "id": "briefing_3",
                        "text": "You'll be running combat simulations to master EVA Unit-01's systems.",
                        "conditions": {},
                        "effects": {"mission_unlocked": "tutorial_battle"}
                    }
                ]
            },
            
            "ritsuko_hub": {
                "character": "Dr. Ritsuko Akagi",
                "scene": "hub",
                "mood": "analytical",
                "dialogues": [
                    {
                        "id": "eva_data",
                        "text": "The EVA's performance data shows continuous improvement.",
                        "conditions": {},
                        "effects": {"info_gained": "eva_performance"}
                    },
                    {
                        "id": "at_field",
                        "text": "AT Field harmonics are stabilizing nicely.",
                        "conditions": {"sync_ratio": ">30"},
                        "effects": {"technical_knowledge": 5}
                    },
                    {
                        "id": "sync_tests",
                        "text": "We should review the sync test results.",
                        "conditions": {},
                        "effects": {"sync_ratio": 2}
                    },
                    {
                        "id": "upgrades",
                        "text": "The upgrade systems are ready for implementation.",
                        "conditions": {"level": ">5"},
                        "effects": {"upgrade_available": True}
                    }
                ]
            }
        }
        
        # Save default dialogues
        for filename, dialogue_data in default_dialogues.items():
            self.save_dialogue(filename, dialogue_data)
        
        # Create editing template
        self._create_editing_template()
    
    def _create_editing_template(self):
        """Create a template for easy dialogue editing"""
        template = {
            "character": "CHARACTER_NAME",
            "scene": "SCENE_NAME", 
            "mood": "neutral",
            "description": "Description of when this dialogue is used",
            "dialogues": [
                {
                    "id": "unique_dialogue_id",
                    "text": "What the character says",
                    "conditions": {
                        "level": ">5",
                        "sync_ratio": ">50",
                        "story_flag": "tutorial_complete",
                        "mood": "happy"
                    },
                    "effects": {
                        "mood": "happy",
                        "stress": -10,
                        "sync_ratio": 5,
                        "experience": 25,
                        "story_flag": "met_character",
                        "info_gained": "some_information"
                    }
                }
            ],
            "interaction_options": [
                {
                    "text": "Player dialogue option",
                    "response": "Character's response",
                    "conditions": {},
                    "effects": {
                        "relationship": 5,
                        "advance_story": True
                    }
                }
            ],
            "special_interactions": {
                "shop": {
                    "available": True,
                    "items": ["item1", "item2"]
                },
                "training": {
                    "available": True,
                    "cost": 50
                },
                "missions": {
                    "available": ["mission1", "mission2"]
                }
            }
        }
        
        template_path = os.path.join(self.data_folder, "TEMPLATE.json")
        with open(template_path, 'w') as f:
            json.dump(template, f, indent=4)
        
        # Create README
        readme_path = os.path.join(self.data_folder, "README.txt")
        with open(readme_path, 'w') as f:
            f.write("""
DIALOGUE EDITING GUIDE
=====================

HOW TO ADD/EDIT DIALOGUES:
1. Copy TEMPLATE.json and rename it (e.g., "new_character.json")
2. Edit the JSON file with your dialogue content
3. Restart the game or use reload_dialogues() to load changes

DIALOGUE STRUCTURE:
- character: Name of the speaking character
- scene: Which scene this dialogue belongs to
- mood: Character's emotional state
- dialogues: List of individual dialogue lines
- interaction_options: Player response choices

CONDITIONS (when dialogue appears):
- level: Player level (e.g., ">5", "=10", "<3")
- sync_ratio: EVA sync ratio percentage
- story_flag: Story progression flags
- mood: Player's current mood
- time_of_day: "morning", "afternoon", "evening", "night"

EFFECTS (what happens after dialogue):
- mood: Change player mood
- stress: Modify stress level (+/-)
- sync_ratio: Change sync ratio (+/-)
- experience: Give experience points
- story_flag: Set story progression flag
- relationship: Change relationship with character

SPECIAL CHARACTERS:
- shinji: Main character (player)
- asuka: Asuka Langley Soryu  
- rei: Rei Ayanami
- misato: Misato Katsuragi
- gendo: Gendo Ikari
- ritsuko: Dr. Ritsuko Akagi

EASY EDITING TIPS:
- Keep dialogue under 80 characters per line for readability
- Use meaningful IDs for dialogue tracking
- Test conditions with simple values first
- Back up your files before major changes
""")
    
    def save_dialogue(self, filename, dialogue_data):
        """Save dialogue data to file"""
        # Create backup
        self._create_backup(filename)
        
        # Save new version
        filepath = os.path.join(self.data_folder, f"{filename}.json")
        try:
            with open(filepath, 'w') as f:
                json.dump(dialogue_data, f, indent=4)
            print(f"💾 Saved dialogue: {filename}")
        except Exception as e:
            print(f"❌ Failed to save dialogue {filename}: {e}")
    
    def load_dialogue(self, filename):
        """Load dialogue data from file"""
        filepath = os.path.join(self.data_folder, f"{filename}.json")
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load dialogue {filename}: {e}")
            return None
    
    def _create_backup(self, filename):
        """Create backup of existing dialogue file"""
        filepath = os.path.join(self.data_folder, f"{filename}.json")
        if os.path.exists(filepath):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_folder, f"{filename}_{timestamp}.json")
            try:
                import shutil
                shutil.copy2(filepath, backup_path)
            except Exception as e:
                print(f"⚠️ Backup failed for {filename}: {e}")
    
    def get_all_dialogues(self):
        """Get all available dialogue files"""
        dialogues = {}
        if os.path.exists(self.data_folder):
            for filename in os.listdir(self.data_folder):
                if filename.endswith('.json') and filename != 'TEMPLATE.json':
                    dialogue_name = filename[:-5]  # Remove .json
                    dialogues[dialogue_name] = self.load_dialogue(dialogue_name)
        return dialogues
    
    def create_new_dialogue(self, character_name, scene_name):
        """Create a new dialogue file from template"""
        filename = f"{character_name.lower().replace(' ', '_')}_{scene_name}"
        
        template = {
            "character": character_name,
            "scene": scene_name,
            "mood": "neutral",
            "dialogues": [
                {
                    "id": f"{character_name.lower()}_greeting",
                    "text": f"Hello! I'm {character_name}.",
                    "conditions": {},
                    "effects": {}
                }
            ],
            "interaction_options": [
                {
                    "text": "Nice to meet you.",
                    "response": "Nice to meet you too!",
                    "effects": {"relationship": 5}
                }
            ]
        }
        
        self.save_dialogue(filename, template)
        return filename
    
    def validate_dialogue(self, dialogue_data):
        """Validate dialogue data structure"""
        required_fields = ["character", "scene", "dialogues"]
        errors = []
        
        for field in required_fields:
            if field not in dialogue_data:
                errors.append(f"Missing required field: {field}")
        
        if "dialogues" in dialogue_data:
            for i, dialogue in enumerate(dialogue_data["dialogues"]):
                if "text" not in dialogue:
                    errors.append(f"Dialogue {i} missing 'text' field")
                if "id" not in dialogue:
                    errors.append(f"Dialogue {i} missing 'id' field")
        
        return errors
    
    def reload_dialogues(self):
        """Reload all dialogue files (for live editing)"""
        return self.get_all_dialogues()
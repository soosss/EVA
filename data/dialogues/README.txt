
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

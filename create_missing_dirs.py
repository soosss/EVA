"""
Create any missing directories and files
"""

import os

# Create all necessary directories
directories = [
    "scenes",
    "entities", 
    "ui",
    "input",
    "managers",
    "graphics",
    "data",
    "assets/art/characters",
    "assets/art/angels",
    "assets/art/backgrounds",
    "assets/art/portraits",
    "assets/art/ui",
    "assets/art/effects",
    "assets/art/eva_units",
    "assets/art/fan_art",
    "saves"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"📁 Created directory: {directory}")

print("✅ All directories created")
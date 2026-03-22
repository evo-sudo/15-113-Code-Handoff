# Fireboy and Watergirl Starter Project

## Project Choice
I chose to build a starter version of **Fireboy and Watergirl** in Python using **pygame**.

## Project Goal
The goal of this project was not to fully complete the game, but to create a clean, readable, and well-documented starting point that another student could realistically inherit and continue.

## Current Features
- Two playable characters:
  - Fireboy uses **WASD**
  - Watergirl uses **arrow keys**
- Basic left/right movement
- Jumping and gravity
- Platform collision
- Players do **not** collide with or block each other
- Simple elemental hazards
- Player reset when touching the opposite element
- Matching fire and water exit doors
- On-screen timer that stops when both players finish

## File Structure
- `main.py`  
  Runs the main game loop and handles rendering.
- `player.py`  
  Contains the `Player` class and movement / collision behavior.
- `level.py`  
  Stores level platforms and hazard layout.
- `settings.py`  
  Stores constants like screen size, physics values, and colors.

## How to Run
1. Install Python
2. Install dependencies:

```bash
pip install -r requirements.txt
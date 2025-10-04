## How to Run

1. Activate a new Python virtual environment using **Python 3.12.X** (3.13+ not compatible yet!) 
2. Install PyGame in your virtual terminal:

``python3 -m pip install -U pygame==2.6.0``

3. Install other packages (random), then run.


*Note: Windows machines may act weird when moving the player because of line 42:*
``pygame.key.set_repeat(1, 3) ``

## Controls
**w** — move left

**d** — move right

**space** — shoot lasers

## Basic Structure

1. Check events
    - key strokes, mouse clicks, optional custom events
2. Update game
   - move objects and player, create new objects, game logic...
3. Draw to screen
    - draw next frame: Rect objects or imported images

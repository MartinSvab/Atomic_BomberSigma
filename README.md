Atomic BomberSigma
==================

Atomic BomberSigma is a small, local multiplayer Bomberman-style game prototype written in Python using Pygame. It’s a grid-based arena where players move tile-by-tile, place bombs that explode in a cross pattern, destroy obstacles and (temporarily) kill players. The project is organized into small, focused modules so you can read, tweak and extend gameplay systems easily.

Quick start — run it locally
============================

1.  Install Python (3.8+ recommended) and the required packages:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install pygame numpy   `

1.  Ensure the game asset images are available. The project expects image files to be reachable by the graphics loader (see game/assets/graphics.py) — by default the loader looks for an images folder relative to the package layout, so make sure your repo contains the expected images in the game/images (or adjust the path in game/assets/graphics.py).
    
2.  From the repository root run:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python launch.py   `

launch.py initializes assets, shows the main menu and then hands control over to the main game loop.

How it works — high level
=========================

*   launch.py performs one-time initialization (loads images) and loops between the main menu and the game loop.
    
*   The main menu and options screens are UI layers built with a simple Button class; they call into the options/menu modules and finally return control to the launcher.
    
*   The in-game core (game/core/game\_loop.py) creates a tile grid and player objects, then runs the main frame loop: input → update → draw → flip. The loop handles quitting and returning to the menu.
    
*   Grid and tiles: a tile grid is generated procedurally with a chance for obstacles; each tile knows its neighbours for simple propagation. Obstacles can be destroyed by explosions.
    
*   Players: a Player object keeps track of sprite, grid position, movement target, HUD and bomb cooldown. Movement is smooth per frame toward a target tile.
    
*   Bombs: placing a bomb appends a Bomb object which counts down, then explodes in a cross pattern, marking tiles as exploding, removing obstacles and setting player state to dead if caught. The bomb system handles animation frames and explosion lifetime.
    

Controls & options
==================

*   Default keybinds are declared in game/assets/keybinds.py; there are presets for up to 4 local players. You can change or rebind keys from the in-game options menu.
    
*   Movement input is read from Pygame’s key state and translated into tile movement; bombs are placed via key-down events handled in the bomb logic module.
    

Files you’ll want to look at (quick map)
========================================

*   launch.py — program entry point (initializes assets, runs menu ↔ game loop).
    
*   game/assets/graphics.py — image loader + small helpers (resize, hue shift). Make sure images are where this loader expects them.
    
*   game/assets/config.py — global settings: screen, tile sizes, grid size, FPS, local player count, etc. Edit this to change resolution, grid dimensions or gameplay constants.
    
*   game/core/game\_loop.py — main game loop: spawns grid, players, bombs and runs the per-frame update/draw.
    
*   game/objects/ — grid.py, tile.py, player.py, bomb.py — core game objects (map, tiles, players and bomb behaviour).
    
*   game/systems/ — input.py, movement.py, bomb\_logic.py — small systems that connect user input to game actions.
    
*   game/ui/ — main\_menu.py, options\_menu.py, button.py, player\_hud.py — UI components and HUD rendering.
    

Common gotchas / troubleshooting
================================

*   **Missing images** → game will crash when the image loader tries to open files. Ensure the images folder and required image files exist and are readable by the loader. See game/assets/graphics.py.
    
*   **Pygame not installed / wrong Python** → install pygame for the Python interpreter you run launch.py with.
    
*   **Fullscreen/scaling** → the default display mode is fullscreen and scaled (set in game/assets/config.py); if you prefer a windowed mode, edit the DISPLAY line in that file.
    
*   **Key rebinding** → use the Options menu in the main menu; it updates game/assets/keybinds.py at runtime.
    

How to modify basic settings
============================

*   Change grid size / tile size / FPS in game/assets/config.py.
    
*   Add or replace images in the images folder used by the loader (icons, sprites, explosion frames). The code resizes loaded images for tiles and sprites at runtime.
    
*   To change bomb behaviour (fuse, radius, animation), inspect game/objects/bomb.py.
    

Contributing / next ideas
=========================

*   Add networked multiplayer (separate server/client or peer-to-peer) (probably not happening xd)
    
*   Power-ups (larger explosion radius, more bombs)
    
*   Match/round logic and scoring, respawns or lives
    
*   Better obstacle generation or map presets

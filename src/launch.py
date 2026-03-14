from game.assets.graphics import initialize_images
from game.assets.sounds import initialize_sounds
from game.assets import config as cfg # Import config to initialize display settings

# One time loading of assets
initialize_images()
initialize_sounds()


import game.core.game_state_manager as game_state_manager
if __name__ == "__main__":
    game_state_manager.run()
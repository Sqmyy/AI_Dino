"""
Platformer Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 650
SCREEN_TITLE = "My AI-Dyno Jumper"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.3
TILE_SCALING = 0.5
TILE_BIRD_SCALING = 0.2


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "./assets/sprites/dino_player.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 112
        self.scene.add_sprite("Player", self.player_sprite)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[256, 150], [900, 90]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            bird = arcade.Sprite(
                "./assets/sprites/bird.png", TILE_BIRD_SCALING
            )
            bird.position = coordinate
            self.scene.add_sprite("Bird", bird)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.scene.draw()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
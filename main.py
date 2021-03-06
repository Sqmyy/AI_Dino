import copy

import arcade
import pathlib
from pyglet.gl import GL_NEAREST
from random import choice, randint
from enum import Enum

REWARD_JUMP_FOR_NOTHING = -1
REWARD_GOOD_JUMP = 5
REWARD_COLLISION = -10

JUMP = 'J'
NOTHING = 'N'
ACTIONS = [NOTHING, JUMP]

DEBUG = False
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 150
WINDOW_TITLE = "Dino Game"
BACKGROUND_COLOR = (247, 247, 247)  # Grey background
ASSETS_PATH = pathlib.Path(__file__).resolve().parent / "assets"
GROUND_WIDTH = 600
LEVEL_WIDTH_PIXELS = GROUND_WIDTH * ((SCREEN_WIDTH * 4) // GROUND_WIDTH)
ALL_TEXTURES = [
    "dino-run-1",
    "dino-run-2",
    "dino-crash-1",
    "dino-duck-1",
    "dino-duck-2",

]
PLAYER_SPEED = 2.0

DinoStates = Enum("DinoStates", "IDLING RUNNING JUMPING DUCKING CRASHING")
GameStates = Enum("GameStates", "PLAYING GAMEOVER")


class DinoGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        # initialize qtable
        self.state_ia = 0
        self.score_ia = 0
        self.learning_rate = 0.2
        self.discount_factor = 0.5
        self.qtable = {}
        for i in range(0, 200, 20):
            self.qtable[f"{i + 1}-{i + 20}"] = {}
            for a in ACTIONS:
                self.qtable[f"{i + 1}-{i + 20}"][a] = 0.0

        self.dino_state = DinoStates.RUNNING
        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.set_mouse_visible(False)
        arcade.set_background_color(BACKGROUND_COLOR)

    def setup(self):
        self.elapsed_time = 0.0
        self.score = 0
        self.textures = {
            tex: arcade.load_texture(ASSETS_PATH / f"{tex}.png") for tex in ALL_TEXTURES
        }
        self.game_state = GameStates.PLAYING

        # Scene setup
        self.scene = arcade.Scene()

        # Horizon setup
        self.horizon_list = arcade.SpriteList()
        for col in range(LEVEL_WIDTH_PIXELS // GROUND_WIDTH):
            horizon_type = choice(["1", "2"])
            horizon_sprite = arcade.Sprite(ASSETS_PATH / f"horizon-{horizon_type}.png")
            horizon_sprite.hit_box = [[-300, -10], [300, -10], [300, -6], [-300, -6]]
            horizon_sprite.left = GROUND_WIDTH * col
            horizon_sprite.bottom = 23
            self.horizon_list.append(horizon_sprite)
        self.scene.add_sprite_list("horizon", False, self.horizon_list)

        # Player setup
        self.player_sprite = arcade.Sprite()
        self.player_sprite.center_x = 200
        self.player_sprite.center_y = 44
        self.player_sprite.texture = self.textures["dino-run-1"]
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        self.scene.add_sprite("player", self.player_sprite)
        self.dino_state = DinoStates.RUNNING

        # Obstacles setup
        self.obstacles_list = arcade.SpriteList()
        self.add_obstacles(SCREEN_WIDTH * 0.8, LEVEL_WIDTH_PIXELS)
        self.scene.add_sprite_list("obstacles", True, self.obstacles_list)

        # Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.horizon_list, gravity_constant=0.4
        )

    def add_obstacles(self, xmin, xmax):
        xpos = xmin
        while xpos < xmax:
            cactus_size = choice(["large", "small"])
            variant = choice(["1", "2", "3"])
            obstacle_sprite = arcade.Sprite(
                ASSETS_PATH / f"cactus-{cactus_size}-{variant}.png"
            )
            obstacle_sprite.left = xpos
            obstacle_sprite.bottom = 20 if cactus_size == "large" else 24
            xpos += (
                    obstacle_sprite.width + randint(200, 400) + obstacle_sprite.width
            )
            self.obstacles_list.append(obstacle_sprite)

    def jump(self):
        self.dino_state = DinoStates.JUMPING
        if self.physics_engine.can_jump():
            self.player_sprite.change_y = 6
        self.dino_state = DinoStates.RUNNING

    def jump_or_not(self, action):
        if action == NOTHING:
            pass
        else:
            self.jump()

    def find_key(self, number):
        if 1 <= number <= 20:
            return "1-20"
        elif 21 <= number <= 40:
            return "21-40"
        elif 41 <= number <= 60:
            return "41-60"
        elif 61 <= number <= 80:
            return "61-80"
        elif 81 <= number <= 100:
            return "81-100"
        elif 101 <= number <= 120:
            return "101-120"
        elif 121 <= number <= 140:
            return "121-140"
        elif 141 <= number <= 160:
            return "141-160"
        elif 161 <= number <= 180:
            return "161-180"
        elif 181 <= number <= 200:
            return "181-200"

    def best_action(self):
        best = None
        if self.state_ia < 0:
            return NOTHING
        else:
            key = self.find_key(self.state_ia)
        for a in self.qtable[key]:
            if not best \
                    or self.qtable[key][a] > self.qtable[key][best]:
                best = a
        return best

    def update_qtable(self, state_ia, action, reward):
        if state_ia > 0:
            key = self.find_key(state_ia)
            maxQ = max(self.qtable[key].values())
            print("valeur a ajouter    {}", self.learning_rate * \
                  (reward + self.discount_factor * maxQ - self.qtable[key][action]))
            self.qtable[key][action] += self.learning_rate * \
                                        (reward + self.discount_factor * maxQ - self.qtable[key][action])
            self.state_ia = state_ia
            self.score_ia += reward
        print(self.qtable)

    def on_update(self, delta_time):
        if self.game_state == GameStates.GAMEOVER:
            self.player_sprite.change_x = 0
            self.player_sprite.texture = self.textures["dino-crash-1"]
            return
        self.elapsed_time += delta_time
        self.offset = int(self.elapsed_time * 10)
        dino_frame = 1 + self.offset % 2
        self.player_list.update()
        self.physics_engine.update()
        # Check for collisions
        collisions = self.player_sprite.collides_with_list(self.obstacles_list)
        if len(collisions) == 0:
            if self.obstacles_list[0].right < self.player_sprite.left:
                self.obstacles_list.pop(0)
        self.state_ia = self.obstacles_list[0].left - self.player_sprite.right
        if self.state_ia <= 200:
            action = self.best_action()
            print("voici mon action>>> {}", action)
            self.jump_or_not(action)
            if len(collisions) > 0:
                self.dino_state = DinoStates.CRASHING
                self.game_state = GameStates.GAMEOVER
            if self.dino_state == DinoStates.CRASHING or self.game_state == GameStates.GAMEOVER:
                self.update_qtable(self.state_ia, action, REWARD_COLLISION)
            elif self.dino_state == DinoStates.RUNNING:
                if self.state_ia > 0:
                    self.update_qtable(self.state_ia, action, REWARD_JUMP_FOR_NOTHING)
                else:
                    self.update_qtable(self.state_ia, action, REWARD_GOOD_JUMP)
                self.player_sprite.texture = self.textures[f"dino-run-{dino_frame}"]
        self.player_sprite.change_x = PLAYER_SPEED
        self.camera_sprites.move((self.player_sprite.left - 30, 0))
        self.score = int(self.player_sprite.left) // 10
        # Extend horizon if first horizon sprite goes off camera
        if self.horizon_list[0].right < self.camera_sprites.goal_position[0]:
            horizon_sprite = self.horizon_list.pop(0)
            horizon_sprite.left = self.horizon_list[-1].left + GROUND_WIDTH
            self.add_obstacles(self.horizon_list[-1].right, horizon_sprite.right)
            self.horizon_list.append(horizon_sprite)

    def on_draw(self):
        arcade.start_render()
        # GUI camera for parallax effect of clouds
        self.camera_gui.use()
        # Game camera
        self.camera_sprites.use()
        self.scene.draw(filter=GL_NEAREST)
        if DEBUG:
            self.player_list.draw_hit_boxes(arcade.color.BANGLADESH_GREEN)
            self.obstacles_list.draw_hit_boxes(arcade.color.BARN_RED)
            self.horizon_list.draw_hit_boxes(arcade.color.CATALINA_BLUE)
        # GUI camera
        self.camera_gui.use()
        arcade.draw_text(
            f"{self.score:05}",
            SCREEN_WIDTH - 2,
            SCREEN_HEIGHT - 10,
            arcade.color.BLACK,
            20,
            font_name="Kenney High",
            anchor_x="right",
            anchor_y="top",
        )
        if self.game_state == GameStates.GAMEOVER:
            self.score = 0
            self.setup()
            self.game_state == GameStates.GAMEOVER
            self.dino_state == DinoStates.RUNNING
            self.update(1 / 80)


def main():
    window = DinoGame(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE)
    window.setup()
    arcade.run()


main()

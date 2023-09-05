import arcade

## Constant defaults

# Window constants
GAME_WIDTH = 1600
GAME_HEIGHT = 800
GAME_TITLE = "Arcade Game"
# Text constants
LINE_HEIGHT = 40
FONT_SIZE = 20
# Player movement
PLAYER_MS = 5
PLAYER_JUMP_SPEED = 20
GRAVITY = 1

# Scaling
TILE_SCALING = 0.5
PLAYER_SCALING = 1
ITEM_SCALING = 0.5

class SomeGame (arcade.Window):

    def __init__(self): 

        super().__init__(GAME_WIDTH, GAME_HEIGHT, GAME_TITLE, fullscreen=False, center_window=True)

        self.scene = None
        # self.wall_list = None
        # self.player_list = None

        self.camera = None

        # GUI camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Score
        self.score = 0

        # Sounds
        self.collect_item_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump3.wav")

        self.tile_map = None

        arcade.set_background_color(arcade.color.BABY_BLUE_EYES)

    def setup(self):

        # Text
        text_x = 288
        text_y = LINE_HEIGHT / 2
        self.fullscreenText = arcade.Text(
            "Press F11 to togle fullscreen. Use WASD to move.",
            text_x,
            text_y,
            arcade.color.BLACK,
            FONT_SIZE * 1.5,
            width=GAME_WIDTH
        )

        # Tile map
        map_name = "Level_01.tmx"
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            }
        }
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options, )
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        # Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Character
        image_source = ":resources:images/animated_characters/robot/robot_idle.png"
        self.player_sprite = arcade.Sprite(image_source, PLAYER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        # self.player_list.append(self.player_sprite)

        # Physics Engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"])

    

    def on_draw(self):

        self.clear()
        
        self.scene.draw()

        self.fullscreenText.draw()

        # Setting up GUI
        self.gui_camera.use()
        score_text= f'Score: {self.score}'
        arcade.draw_text(score_text, start_x=10, start_y=10, color= arcade.color.BARN_RED, font_size=FONT_SIZE, bold=True)

        # Normal camera
        self.camera.use()

    def on_key_press(self, key, modifiers):

        # Fullscreen to Windowed
        if key == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)

        # Jumps
        if key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        
        # Player movement
        elif key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MS
        elif key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MS
    
    def on_key_release(self, key: int, modifiers):

        # Player movement
        if key == arcade.key.A:
            self.player_sprite.change_x = 0
        if key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):

        self.physics_engine.update()

        self.center_camera_to_player()

        # Item picking
        item_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Items"])
        for item in item_hit_list:
            item.remove_from_sprite_lists()
            arcade.play_sound(self.collect_item_sound)
            self.score += 1
            
            

    # Camera movement
    def center_camera_to_player(self):

        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)


def main():

    window = SomeGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":

    main()
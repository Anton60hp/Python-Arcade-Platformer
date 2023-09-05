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

class SomeGame (arcade.Window):

    def __init__(self): 

        super().__init__(GAME_WIDTH, GAME_HEIGHT, GAME_TITLE, fullscreen=False, center_window=True)

        self.scene = None
        # self.wall_list = None
        # self.player_list = None

        self.camera = None

        arcade.set_background_color(arcade.color.BABY_BLUE_EYES)

    def setup(self):

        text_x = LINE_HEIGHT / 2 
        text_y = GAME_HEIGHT - LINE_HEIGHT
        self.fullscreenText = arcade.Text(
            "Press F11 to togle fullscreen. Use WASD to move.",
            text_x,
            text_y,
            arcade.color.BLACK,
            FONT_SIZE * 1.5,
            width=GAME_WIDTH
        )

        # Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Scene
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        # self.wall_list = arcade.SpriteList()
        # self.player_list = arcade.SpriteList(use_spatial_hash=True)

        # Character
        image_source = ":resources:images/animated_characters/robot/robot_idle.png"
        self.player_sprite = arcade.Sprite(image_source, PLAYER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        # self.player_list.append(self.player_sprite)

        # Ground
        for x in range(0, 2048, 64):
            wall = arcade.Sprite(":resources:images/tiles/stoneMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)
            # self.wall_list.append(wall)

        # Chests
        coordinate_list = [[768,96], [320,224], [384,224], [352,288]]

        for x in range(256, 512, 64):
            coordinate_list.append([x,96])
            
        for x in range (288, 480, 64):
            coordinate_list.append([x,160])
        
        for coordinate in coordinate_list:
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        # Physics Engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"])

    

    def on_draw(self):

        self.clear()
        
        self.scene.draw()

        self.fullscreenText.draw()

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
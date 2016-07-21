import pygame
from pygame.locals import *

from Camera import Camera
from DiamondSquare import DiamondSquare
from EntityClasses import Player, Button, EnvironmentTile, Mouse
from ImageCache import ImageCache


class Game:
    def __init__(self, window_size, block_size):
        self.window_size = window_size
        self.block_size = block_size

        # Initialise the pygame variables
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        self.fps = 25

        # Initialize the image cache
        self.image_cache = ImageCache("data/images")

        # Create entity groups for PyGame
        self.environment_entities = pygame.sprite.Group()
        self.player_entities = pygame.sprite.Group()

        # Create the player
        self.player = Player(32, 32, self.image_cache)
        self.player_entities.add(self.player)

        # Create the level
        self.level = DiamondSquare(6, 0.05).get_grid_2D()  # Random map created using Diamond Square

    def run(self):
        self.start_menu()
        self.main_game()

    def start_menu(self):
        start_game = False

        half_screen_width = self.window_size[0] / 2
        half_screen_height = self.window_size[1] / 2

        # Create the buttons for the start menu
        new_game_button = Button("new_game",
                                 half_screen_width, half_screen_height - 50,
                                 self.image_cache.load_image("New_Game.png"),
                                 self.image_cache.load_image("New_Game_Hover.png"))
        quit_game_button = Button("exit_game",
                                  half_screen_width, half_screen_height + 10,
                                  self.image_cache.load_image("Quit_Game.png"),
                                  self.image_cache.load_image("Quit_Game_Hover.png"))

        button_entities = pygame.sprite.Group()
        button_entities.add((new_game_button, quit_game_button))

        # Load the start menu background
        background = self.image_cache.load_image("Menu_Background.png")
        self.screen.blit(background, (0, 0))

        # Load the credit image
        credit_image = self.image_cache.load_image("Credits.png")
        self.screen.blit(credit_image, (20, self.window_size[1] - 50))

        while not start_game:

            self.clock.tick(self.fps)
            current_fps = float(self.clock.get_fps())

            # Update the title and display the current FPS
            pygame.display.set_caption("The Forming | FPS: " + str(current_fps))

            mouse_clicked = False

            # Handle the events for the game
            for event in pygame.event.get():
                # Quit the game
                if event.type == QUIT:
                    pygame.quit()
                if event.type == MOUSEBUTTONDOWN:
                    mouse_clicked = True
                if event.type == KEYDOWN:
                    if event.key == K_F1:
                        # Take screenshot
                        pass

            # Reloading all images
            self.screen.blit(background, (0, 0))
            self.screen.blit(credit_image, (20, self.window_size[1] - 50))

            # Handle the buttons
            mouse_pos = pygame.mouse.get_pos()
            new_game_button.update(mouse_pos)
            quit_game_button.update(mouse_pos)

            if new_game_button.mouse_collision() and mouse_clicked:
                start_game = True

            if quit_game_button.mouse_collision() and mouse_clicked:
                pygame.quit()
            button_entities.draw(self.screen)

            pygame.display.update()

    def main_game(self):

        # Set the default control flags
        up = down = left = right = False
        exit_game = False
        walking = False

        self.load_level()  # Create the environment assets

        level_size = (len(self.level[0]) * self.block_size[0], len(self.level) * self.block_size[1])

        camera = Camera(level_size, self.window_size)
        mouse = Mouse(pygame.mouse.get_pos())
        mouse_clicked = False
        mosue_right_clicked = False

        while not exit_game:

            # Reset control flags each loop
            mouse_clicked = False
            mouse_right_clicked = False

            # Handle pygame
            self.clock.tick(self.fps)

            # Load title displaying true FPS
            current_fps = float(self.clock.get_fps())
            pygame.display.set_caption("The Forming | FPS: " + str(current_fps))

            # Event Handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                # Keydown events
                if event.type == KEYDOWN:
                    if event.key == K_UP or event.key == K_w:
                        up = True
                    elif event.key == K_DOWN or event.key == K_s:
                        down = True
                    elif event.key == K_LEFT or event.key == K_a:
                        left = True
                    elif event.key == K_RIGHT or event.key == K_d:
                        right = True
                if event.type == KEYUP:
                    if event.key == K_UP or event.key == K_w:
                        up = False
                    elif event.key == K_DOWN or event.key == K_s:
                        down = False
                    elif event.key == K_LEFT or event.key == K_a:
                        left = False
                    elif event.key == K_RIGHT or event.key == K_d:
                        right = False

                    # Mouse events
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_clicked = True
                        elif event.button == 3:
                            mouse_right_clicked = True
                    if event.type == MOUSEBUTTONUP:
                        if event.button == 1:
                            mouse_clicked = False
                        elif event.button == 3:
                            mouse_right_clicked = False

            # Update the entities
            camera.update(self.player)
            self.player.update(up, down, left, right, level_size)

            for tile in self.environment_entities:
                self.screen.blit(tile.image, camera.apply(tile))
            for player in self.player_entities:
                self.screen.blit(player.image, camera.apply(player))

            mouse.update(pygame.mouse.get_pos())

            pygame.display.update()

    def load_level(self):

        x = 0
        y = 0

        for y_tile in self.level:
            x = 0
            for x_tile in y_tile:
                print x_tile
                if 0 == x_tile <= 0.5:
                    tile = EnvironmentTile(x, y, self.block_size[0], self.block_size[1], "Water", "Water",
                                           self.image_cache.load_image("Water.png"))
                elif 0.5 < x_tile <= 0.55:
                    tile = EnvironmentTile(x, y, self.block_size[0], self.block_size[1], "Sand", "Sand",
                                           self.image_cache.load_image("Sand.png"))
                else:
                    tile = EnvironmentTile(x, y, self.block_size[0], self.block_size[1], "Grass", "Grass",
                                           self.image_cache.load_image("Grass1.png"))
                self.environment_entities.add(tile)
                x += 32
            y += 32


game = Game((640, 640), (32, 32))
game.run()

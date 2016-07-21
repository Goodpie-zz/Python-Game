import pygame

from ImageCache import ImageCache
from EntityClasses import Player, Button
from pygame.locals import *


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
        self.player = Player(32, 32, self.image_cache.get_cache())
        self.player_entities.add(self.player)

    def run(self):
        self.start_menu()

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


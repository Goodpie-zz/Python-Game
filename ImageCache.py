import glob
import pygame


class ImageCache:
    def __init__(self, dir):

        self.dir = dir
        self.image_cache = {}

    def populate_image_cache(self):

        all_images = glob.glob(self.dir + "/*.png")
        for image in all_images:
            self.load_image(image)

    def load_image(self, key):

        if key not in self.image_cache:
            self.image_cache[key] = pygame.image.load(self.dir + "/" + key).convert_alpha()

        return self.image_cache[key]

    def get_cache(self):
        return self.image_cache

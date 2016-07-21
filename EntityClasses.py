import pygame
from pygame.locals import *


# Main Entity Class
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(Entity):
    def __init__(self, x, y, image_cache):

        Entity.__init__(self)

        self.move_speed = 8
        self.image_cache = image_cache
        self.image = self.image_cache.load_image("Character.png")
        self.image.convert()
        self.anim_frame = 0
        self.rect = Rect(x, y, 32, 32)

    def update(self, up, down, left, right, level_size):
        # Handle player movement along the x and y axis and the walking animation
        y_move = 0
        x_move = 0

        if up:
            y_move += -self.move_speed
            if self.anim_frame == 0:
                self.image = self.image_cache.load_image("Character_Back_W.png")
                self.anim_frame += 1
            else:
                self.image = self.image_cache.load_image("Character_Back.png")
                self.anim_frame -= 1
        if down:
            y_move += self.move_speed
            if self.anim_frame == 0:
                self.image = self.image_cache.load_image("Character_W.png")
                self.anim_frame += 1
            else:
                self.image = self.image_cache.load_image("Character.png")
                self.anim_frame -= 1
        if left:
            x_move += -self.move_speed
            if self.anim_frame == 0:
                self.image = self.image_cache.load_image("Character_Left_W.png")
                self.anim_frame += 1
            else:
                self.image = self.image_cache.load_image("Character_Left.png")
                self.anim_frame -= 1
        if right:
            x_move += self.move_speed
            if self.anim_frame == 0:
                self.image = self.image_cache.load_image("Character_Right_W.png")
                self.anim_frame += 1
            else:
                self.image = self.image_cache.load_image("Character_Right.png")
                self.anim_frame -= 1

        # Update the rect to match the movement
        self.rect.left += x_move
        self.rect.top += y_move

        # Ensure the player doesn't go out of bounds of the level
        # Check bounds along y
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > level_size[1]:
            self.rect.bottom = level_size[1]

        # Check bounds along x
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > level_size[0]:
            self.rect.right = level_size[0]


# mouse Class
class Mouse(Entity):
    def __init__(self, pos):
        Entity.__init__(self)
        self.x = pos[0]
        self.y = pos[1]
        self.rect = Rect(pos[0], pos[1], 32, 32)

    def update(self, pos, check=False):
        self.x = pos[0]
        self.y = pos[1]
        self.rect.top = pos[1]
        self.rect.left = pos[0]

        if check:
            print "Mouse Pos: %s" % self.rect
            print self.x, self.y

    def get_rect(self):
        return self.x, self.y

# Environment Asset
class EnvironmentTile(Entity):
    def __init__(self, x, y, width, height, type, name, sprite_image):
        Entity.__init__(self)
        self.x = x
        self.y = y
        self.type = type
        self.name = name
        self.image = sprite_image
        self.image.convert()
        self.rect = Rect(x, y, width, height)

    def hit_test(self, x, y):
        hit_x = self.rect.x <= x < self.rect.x + self.rect.width  # X between the left and right
        hit_y = self.rect.y <= y < self.rect.y + self.rect.height  # Y between the top and bottom
        return hit_x and hit_y

    def get_rect(self):
        return self.rect


# Button class
class Button(Entity):
    def __init__(self, id, x, y, main_image, alt_image=None):
        Entity.__init__(self)

        self.id = id
        self.main_image = main_image
        self.main_image.convert()

        # If the alternate image doesn't exist, just use the same image
        if alt_image is not None:
            self.alt_image = alt_image
        else:
            self.alt_image = main_image
        self.alt_image.convert()

        self.image = main_image  # The default image for the button
        self.size = self.image.get_rect().size
        self.rect = Rect(x, y, self.size[0], self.size[1])

        self.mouse_colliding = False

    def update(self, mouse_pos):

        # Alternate between the alt and main image depending on mouse over
        if self.rect.collidepoint(mouse_pos):
            self.image = self.alt_image
            self.mouse_colliding = True
        else:
            self.image = self.main_image
            self.mouse_colliding = False

    def mouse_collision(self):
        return self.mouse_colliding

    def action(self):
        pass  # Override in main if required

import pygame, sys, os, functions
from pygame.locals import *


# Main Entity Class
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


# The Player Class
class Player(Entity):
    def __init__(self, x, y, image_cache):
        Entity.__init__(self)
        self.image_cache = image_cache
        self.pos_x = x
        self.pos_y = y
        self.in_shop = False
        self.image = functions.get_image("data/images/Character.png", self.image_cache)
        self.image.convert()
        self.rect = Rect(self.pos_x, self.pos_y, 32, 32)

    def update(self, up, down, left, right, position_check,
               obsticles, trees, level_width, level_height):
        if up:
            self.pos_y = -8
        elif down:
            self.pos_y = 8
        elif left:
            self.pos_x = -8
        elif right:
            self.pos_x = 8

        if not (up or down):
            self.pos_y = 0
        if not (left or right):
            self.pos_x = 0

        # Moving the character
        self.rect.left += self.pos_x
        self.rect.top += self.pos_y

        # Collision Detection and animations
        self.collision_test(level_width, level_height, trees, obsticles)

        if position_check:
            print "Player Pos: {0:s} ".format(self.rect)

    def collision_test(self, level_width, level_height, trees, obsticles):
        if self.rect.top < 0:
            self.pos_y = 0
            self.rect.top = 0

        if self.rect.bottom > level_height:
            self.pos_y = 0
            self.rect.bottom = level_height

        if self.rect.left < 0:
            self.pos_x = 0
            self.rect.left = 0

        if self.rect.right > level_width:
            self.pos_x = 0
            self.rect.right = level_width

        for t in trees:
            if pygame.sprite.collide_rect(self, t):
                if self.pos_x > 0:
                    self.rect.right = t.rect.left
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_x < 0:
                    self.rect.left = t.rect.right
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_y > 0:
                    self.rect.bottom = t.rect.top
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_y < 0:
                    self.rect.top = t.rect.bottom
                    self.pos_x = 0
                    self.pos_y = 0
        for o in obsticles:
            if pygame.sprite.collide_rect(self, o):
                if self.pos_x > 0:
                    self.rect.right = o.rect.left
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_x < 0:
                    self.rect.left = o.rect.right
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_y > 0:
                    self.rect.bottom = o.rect.top
                    self.pos_x = 0
                    self.pos_y = 0
                elif self.pos_y < 0:
                    self.rect.top = o.rect.bottom
                    self.pos_x = 0
                    self.pos_y = 0

    def walking_animation(self, walking, up, down, left, right):
        walk = walking
        if down:
            if walk:
                walk = False
                self.image = functions.get_image("data/images/Character_W.png", self.image_cache)
            elif not walk:
                walk = True
                self.image = functions.get_image("data/images/Character.png", self.image_cache)
        elif up:
            if walk:
                walk = False
                self.image = functions.get_image("data/images/Character_Back_W.png", self.image_cache)
            elif not walk:
                walk = True
                self.image = functions.get_image("data/images/Character_Back.png", self.image_cache)
        elif left:
            if walk:
                walk = False
                self.image = functions.get_image("data/images/Character_Left_W.png", self.image_cache)
            elif not walk:
                walk = True
                self.image = functions.get_image("data/images/Character_Left.png", self.image_cache)
        elif right:
            if walk:
                walk = False
                self.image = functions.get_image("data/images/Character_Right_W.png", self.image_cache)
            elif not walk:
                walk = True
                self.image = functions.get_image("data/images/Character_Right.png", self.image_cache)

        return walk

    def get_pos(self):
        return self.pos_x, self.pos_y


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

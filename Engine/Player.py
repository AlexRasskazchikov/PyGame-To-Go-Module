from pygame import draw
from pygame import transform
import pygame

class Player:
    def __init__(self, size=(50, 100), speed=1,
                 color=(255, 0, 0), controls=None,
                 coords=None, b_collision=True,
                 animation_pack=None):
        self.speed = speed
        self.width, self.height = size
        self.controls = controls
        self.color = color
        self.border_collision = b_collision
        self.animation = animation_pack
        self.image = None
        self.coords = None
        self.start_coords = None
        self.direction = "right"

        if animation_pack is not None:
            self.image = transform.scale(animation_pack[list(animation_pack.get_sets_names())[0]][0], (self.width, self.height))

        """If current player is npc."""
        self.act = "left"
        self.sleep = True
        self.awakeFrame = 50
        self.coords = (10, pygame.display.get_surface().get_size()[1] - self.height)
        self.start_coords = self.coords
        if coords is not None:
            self.coords = coords
            self.start_coords = self.coords


    def right(self):
        """Moves player right on self.speed pixels."""
        self.coords = (self.coords[0] + self.speed, self.coords[1])
        return self.coords

    def left(self):
        """Moves player left on self.speed pixels."""
        self.coords = (self.coords[0] - self.speed, self.coords[1])
        return self.coords

    def up(self):
        """Moves Player Up"""
        self.coords = (self.coords[0], self.coords[1] - self.speed)

    def down(self):
        """Moves Player Down"""
        self.coords = (self.coords[0], self.coords[1] + self.speed)

    def jump(self):
        """Player jumps"""
        pass

    def collisionWith(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def setColor(self, new_color):
        """Changes Player color"""
        self.color = new_color

    def setCoords(self, new_cords):
        """Sets new coords to player"""
        if self.start_coords is None:
            self.start_coords = new_cords
        self.coords = new_cords

    def draw(self, screen):
        """Draw Player on choosen screen"""
        if self.image is None:
            draw.rect(screen, self.color,
                      (*self.coords, self.width, self.height))
        else:
            screen.blit(self.image, self.coords)

    def set_sprite_from_pack(self, name, id):
        """Change player's sprite to sprite from Pack"""
        self.image = transform.scale(self.animation.get_frame(name, id), (self.width, self.height))

    def set_sprite_from_image(self, image):
        """Change player's sprite to your image"""
        self.image = transform.scale(image, (self.width, self.height))

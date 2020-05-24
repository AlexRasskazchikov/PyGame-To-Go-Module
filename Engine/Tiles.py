import pygame
from pygame.rect import Rect


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Platform(Entity):
    def __init__(self, x, y, image):
        Entity.__init__(self)
        self.img = pygame.Surface((32, 32))
        self.img.convert()
        self.img = pygame.transform.scale(image, (32, 32))
        self.rect = Rect(x, y, 32, 32)
        self.mask = pygame.mask.from_surface(self.img)
    def update(self):
        pass


class ExitBlock(Platform):
    def __init__(self, x, y):
        super().__init__(self, x, y)
        self.img.fill((255, 255, 255))

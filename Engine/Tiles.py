import pygame
from pygame.rect import Rect


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Background(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(r"Assets/level1/Hills Layer 01.png"), (3000, 1500))
        self.rect = self.image.get_rect(topleft=(0, 0))

    def update(self):
        pass


class Platform(Entity):
    def __init__(self, x, y, image):
        Entity.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.image.convert()
        self.image = pygame.transform.scale(image, (32, 32))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass


class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill((255, 255, 255))

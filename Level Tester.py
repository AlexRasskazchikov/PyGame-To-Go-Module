import pygame
from pygame.rect import Rect

from Engine.Characters import player1, knight
from Engine.Levels import Plain

WIN_WIDTH = 1000
WIN_HEIGHT = 600
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 100
cell_height = 32


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l + HALF_WIDTH, -t + HALF_HEIGHT, w, h)


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l + HALF_WIDTH, -t + HALF_HEIGHT, w, h

    l = min(0, l)  # stop scrolling at the left edge
    l = max(-(camera.width - WIN_WIDTH), l)  # stop scrolling at the right edge
    t = max(-(camera.height - WIN_HEIGHT), t)  # stop scrolling at the bottom
    t = min(0, t)  # stop scrolling at the top
    return Rect(l, t, w, h)


def run(level, display, player):
    timer = pygame.time.Clock()

    background = level.background
    player2 = knight

    player1.set_coords((50, 50), start=True)
    player2.set_coords((50, 50), start=True)

    entities, platforms = level.render_files()
    total_level_width = level.total_level_width
    total_level_height = level.total_level_height

    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player1)
    player2.name = "Clone"
    level.background_objects.append(player2)
    FramesClock = 0
    while True:
        timer.tick(100)
        FramesClock += 1
        keys = pygame.key.get_pressed()
        events = list(map(lambda x: x.type, pygame.event.get()))
        if pygame.QUIT in events:
            raise SystemExit("Quit")
        screen.fill(background)

        player.update_frame(pygame.key.get_pressed(), FramesClock)
        player2.update_frame(pygame.key.get_pressed(), FramesClock)
        camera.update(player1)

        player.update(keys, platforms)
        player2.update(keys, platforms)

        for o in level.background_objects:
            screen.blit(o.image, camera.apply(o))
            if player.hit_collides(o):
                print(f"Hitted {o.name}")

        for e in entities:
            display.blit(e.image, camera.apply(e))

        pygame.display.update()


pygame.init()
screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.display.set_caption("Engine Testing")

run(Plain, screen, player1)

import random

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from Engine.Characters import Knight
from Engine.Functions import show_fps
from Engine.Player import Player
from Engine.Levels import Plain
from Engine.Tiles import Entity, ExitBlock

WIN_WIDTH = 1000
WIN_HEIGHT = 600
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 100
cell_height = 32


def main():
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Engine Testing")
    timer = pygame.time.Clock()
    player = Player((50, 50), (int(50 * 3.2), int(37 * 3.2)), animation=Knight)

    level = Plain
    background = level.background
    entities, platforms = level.render_files()
    total_level_width = level.total_level_width
    total_level_height = level.total_level_height

    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player)
    FramesClock = 0
    while True:
        timer.tick(100)
        FramesClock += 1
        keys = pygame.key.get_pressed()
        events = list(map(lambda x: x.type, pygame.event.get()))
        if pygame.QUIT in events:
            raise SystemExit("QUIT")

        screen.fill(background)
        show_fps(screen, timer)
        player.update_frame(pygame.key.get_pressed(), FramesClock)
        camera.update(player)

        player.update(keys, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()


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


if __name__ == "__main__":
    main()

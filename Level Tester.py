import random

import pygame
from pygame.rect import Rect
from copy import copy
from Engine import show_fps, White
from Engine.Characters import player1, knight
from Engine.Levels import Plain

WIN_WIDTH = 1000
WIN_HEIGHT = 500
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

    clock = pygame.time.Clock()

    background = level.background
    player2 = knight

    player1.set_coords((700, 350), start=True)
    player2.set_coords((50, 50), start=True)

    entities, platforms = level.render_files()
    total_level_width = level.total_level_width
    total_level_height = level.total_level_height

    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player1)
    player2.name = "Clone"
    level.background_objects.append(player2)
    FramesClock = 0
    background_objects = list(map(lambda x: copy(x), level.background_objects))
    while True:
        clock.tick(60)
        FramesClock += 1
        keys = pygame.key.get_pressed()
        events = list(map(lambda x: x.type, pygame.event.get()))
        if keys[pygame.K_LSHIFT]:
            player.speed = 10
        else:
            player.speed = 5
        screen.fill(background)

        player.update_frame(keys, FramesClock)
        player2.update_frame(keys, FramesClock)
        player.update_mask()

        camera.update(player1)

        player.update(keys, platforms)

        draw_list = ["Tree", "Clone", "Cloud"]

        for o in list(filter(lambda x: x.name in draw_list, background_objects)):
            if player.check_hit(o, random.choice(o.sounds)) is not None:
                display.blit(o.hitted_image, camera.apply(o))
                if o.hp - player.damage >= 0:
                    o.hp -= player.damage
                else:
                    background_objects.remove(o)
            else:
                display.blit(o.image, camera.apply(o))

        for e in entities:
            display.blit(e.image, camera.apply(e))

        player.draw_mask(display, color=(0, 0, 0))
        show_fps(display, clock)
        pygame.display.update()

        if keys[pygame.K_r]:
            from Engine.Levels import Plain
            background_objects = list(map(lambda x: copy(x), level.background_objects))
            print(list(map(lambda x: x.name + " " + str(x.hp), level.background_objects)))

        if pygame.QUIT in events:
            raise SystemExit("Quit")


pygame.init()
screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.display.set_caption("Engine Testing")

run(Plain, screen, player1)

import random
from copy import copy

import pygame
from pygame.rect import Rect

from Engine import show_fps, show_info, bake_light
from Engine.Characters import player1
from Engine.Levels import Plain, LightDemo

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

    player1.set_coords((700, 350), start=True)

    entities, platforms = level.render_files()
    total_level_width = level.total_level_width
    total_level_height = level.total_level_height
    font = pygame.font.Font(r'C:\Windows\Fonts\Arial.ttf', 25)
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player1)
    FramesClock = 0
    background_objects = list(map(lambda x: copy(x), level.background_objects))
    size = pygame.display.get_surface().get_size()
    image_filter = pygame.Surface(size, pygame.SRCALPHA, 32)
    light = pygame.image.load('Assets/light.png')
    w, h = player.rect.w, player.rect.h
    light = pygame.transform.scale(light, (w * 4, h * 4))
    clear_image_filter = copy(image_filter)
    clear_image_filter.fill((100, 100, 100))

    while True:
        clock.tick(90)
        FramesClock += 1
        keys = pygame.key.get_pressed()
        events = list(map(lambda x: x.type, pygame.event.get()))
        screen.fill((0, 0, 0))

        player.update_frame(keys, FramesClock)
        player.update_mask()
        camera.update(player1)
        player.update(keys, platforms)

        for i in range(len(background_objects)):
            o = background_objects[i]
            if o.name == "Cloud":
                move_cloud(FramesClock, o, i % 2)

        draw_list = ["Tree"]

        for o in list(filter(lambda x: x.name in draw_list, background_objects)):
            if o.name == "Cloud" and "Wood" in player.inventory and player.inventory["Wood"]['count'] >= 3:
                o.set_active(True)
            if player.check_hit(o, random.choice(o.sounds)) is not None:
                display.blit(o.h_img, camera.apply(o))
                if o.hp - player.damage >= 0:
                    o.hp -= player.damage
                else:
                    player.inventory_add_object(o)
                    print(player.inventory)
                    background_objects.remove(o)
            else:
                display.blit(o.img, camera.apply(o))

        for e in entities:
            display.blit(e.image, camera.apply(e))

        if level.lighting:
            bake_light(display, clear_image_filter, camera, player, light)

        if keys[pygame.K_F1]:
            player.draw_mask(display)
            show_fps(display, clock, font)
            show_info(display, f"{player.rect.x}; {player.rect.y + player.rect.h}", font)

        player.draw_inventory(display)
        pygame.display.update()

        if keys[pygame.K_r]:
            background_objects = list(map(lambda x: copy(x), level.background_objects))

        if pygame.QUIT in events:
            raise SystemExit("Quit")

        if pygame.MOUSEBUTTONDOWN in events:
            break

def move_cloud(FramesClock, Object, Reversed=False, speed=500):
    if Reversed:
        if FramesClock % speed < speed // 2:
            Object.move(-1, 0)
        else:
            Object.move(1, 0)
    else:
        if FramesClock % speed < speed // 2:
            Object.move(1, 0)
        else:
            Object.move(-1, 0)




pygame.init()
screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.display.set_caption("Engine Testing")

while True:
    run(LightDemo, screen, player1)
    run(Plain, screen, player1)

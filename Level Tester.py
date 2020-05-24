import random
from copy import copy

import pygame

from Engine import show_fps, show_info, bake_light
from Engine.Characters import player1
from Engine.Levels import Plain, LightDemo, BackgroundObject

WIN_WIDTH = 1366
WIN_HEIGHT = 768
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
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

    player1.set_coords((700, 350), start=True)
    total_level_width = level.total_level_width
    total_level_height = level.total_level_height
    font = pygame.font.Font(r'C:\Windows\Fonts\Arial.ttf', 25)
    camera = Camera(complex_camera, total_level_width, total_level_height)
    FramesClock = 0

    """Level Objects loading"""
    entities, platforms, background_tiles = level.render_files()
    level.background_objects = list(map(lambda x: copy(x), level.background_objects)) + list(
        map(lambda x: copy(x), background_tiles))
    background_objects = list(map(lambda x: copy(x), level.background_objects))
    entities.add(player1)

    """Lighting"""
    background = level.background
    image_filter = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA, 32)
    light = pygame.image.load('Assets/light.png')
    light = pygame.transform.scale(light, (player.rect.w * 4, player.rect.h * 4))
    clear_image_filter = copy(image_filter)
    clear_image_filter.fill((100, 100, 100))

    while True:
        clock.tick(300)
        FramesClock += 1
        keys = pygame.key.get_pressed()
        events = list(map(lambda x: x.type, pygame.event.get()))
        display.fill(background)

        player.update_frame(keys, FramesClock)
        player.update_mask()
        camera.update(player1)
        player.update(keys, platforms)

        for i in range(len(background_objects)):
            o = background_objects[i]
            if o.name == "Cloud":
                move_cloud(FramesClock, o, bool(i % 2))

        for key in player.inventory:
            if pygame.MOUSEBUTTONDOWN in events and player.inventory[key]["choosen"]:
                o = player.inventory[key]["object"]
                new = BackgroundObject(o.img, (player.rect.x, 0), name=o.name, act=True, mat=o.mat)
                player.inventory[key]["count"] -= 1
                if player.inventory[key]["count"] <= 0:
                    del player.inventory[key]
                    background_objects.append(new)
                    break
                background_objects.append(new)

        draw_list = ["Tree", "Cloud", "Tile"]

        for o in list(filter(lambda x: x.name in draw_list, background_objects)):
            if player.check_hit(o, random.choice(o.sounds)) is not None:
                display.blit(o.h_img, camera.apply(o))
                if o.hp - player.damage > 0:
                    o.hp -= player.damage
                else:
                    player.inventory_add_object(copy(o))
                    print(player.inventory)
                    background_objects.remove(o)
            else:
                display.blit(o.img, camera.apply(o))

        for e in entities:
            display.blit(e.img, camera.apply(e))

        if level.lighting:
            bake_light(display, clear_image_filter, camera, player, light)

        if keys[pygame.K_F1]:
            player.draw_mask(display)
            show_fps(display, clock, font)
            show_info(display, f"{player.rect.x}; {player.rect.y + player.rect.h}", font)

        player.draw_inventory(display, font)
        pygame.display.update()

        if keys[pygame.K_F5]:
            background_objects = list(map(lambda x: copy(x), level.background_objects))
            player.inventory = {}

        if keys[pygame.K_ESCAPE]:
            raise SystemExit("Escape")

        if keys[pygame.K_F3]:
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
from pygame.locals import *

flags = FULLSCREEN | DOUBLEBUF
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), flags)

while True:
    run(Plain, display, player1)
    run(LightDemo, display, player1)

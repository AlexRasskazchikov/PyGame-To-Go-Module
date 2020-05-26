import pickle
import random
from copy import copy

import pygame

from Engine import show_fps, show_info, bake_light
from Engine.Characters import player1
from Engine.Levels import Plain, BackgroundObject, Polygon

WIN_WIDTH = 1366
WIN_HEIGHT = 768
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
CAMERA_SLACK = 500
cell_height = 50


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def reverse(self, pos):
        """Gets the world coordinates by screen coordinates"""
        return pos[0] - self.state.left, pos[1] - self.state.top

    def apply_rect(self, rect):
        return rect.move(self.state.topleft)


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


def run(level, display, player, load=False):
    clock = pygame.time.Clock()
    if not load:
        player1.set_coords((700, 350), start=True)
        total_level_width = level.total_level_width
        total_level_height = level.total_level_height
        camera = Camera(complex_camera, total_level_width, total_level_height)

        """Level Objects loading"""
        entities, platforms, background_tiles = level.render_files()
        level.background_objects = list(map(lambda x: copy(x), level.background_objects)) + list(
            map(lambda x: copy(x), background_tiles))
        background_objects = list(map(lambda x: copy(x), level.background_objects))
        entities.add(player1)
        """Lighting"""
        image_filter = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA, 32)
        light = pygame.image.load('Assets/light.png')
        light = pygame.transform.scale(light, (player.rect.w * 4, player.rect.h * 4))
        clear_image_filter = copy(image_filter)
        clear_image_filter.fill((100, 100, 100))
    else:
        with open("savegame", "rb") as f:
            load_dict = pickle.load(f)
        entities, platforms, background_tiles = load_dict["Game-Objects"]
        background_objects = load_dict["Background-Objects"]
        camera = load_dict["Camera"]

    gradient = vertical_gradient((WIN_WIDTH, WIN_HEIGHT), (107, 116, 202), (211, 211, 211))
    font = pygame.font.Font(r'C:\Windows\Fonts\Arial.ttf', 25)
    FramesClock = 0

    while True:
        clock.tick(300)
        FramesClock += 1
        keys = pygame.key.get_pressed()
        events = list(map(lambda x: x.type, pygame.event.get()))
        """display.fill(background)"""
        display.blit(gradient, (0, 0))

        player.update_frame(keys, FramesClock)
        player.update_mask()
        camera.update(player1)
        player.update(keys, platforms)

        for i in range(len(player.inventory)):
            if pygame.MOUSEBUTTONDOWN in events and pygame.mouse.get_pressed()[2] and player.inventory[i].choosen:

                mouse = camera.reverse(pygame.mouse.get_pos())
                colliding = list(map(lambda p: p.rect.collidepoint(mouse), platforms))

                if not any(colliding):
                    o = player.inventory[i]
                    new_coords = list(map(lambda x: x - x % cell_height, camera.reverse(pygame.mouse.get_pos())))
                    new = BackgroundObject(o.img, new_coords, name=o.name, act=True,
                                           mat=o.mat, hp=o.hp, type=o.type)
                    player.inventory[i].amount -= 1

                    # Recognizing: BkgObject, or just a platform.
                    if new.type == "BackgroundObject":
                        background_objects.append(new)
                    else:
                        platforms.append(new)
                        entities.add(new)

                    # If material ended in player's inventory.
                    if player.inventory[i].amount <= 0:
                        del player.inventory[i]
                        break

            # Drawing before-placing rectangle
            elif player.inventory[i].choosen:
                mouse = camera.reverse(pygame.mouse.get_pos())
                colliding = list(map(lambda p: p.rect.collidepoint(mouse), platforms))
                if not any(colliding):
                    new_coords = list(map(lambda x: x - x % cell_height, mouse))
                    rect = player.inventory[i].img.get_rect(topleft=new_coords)
                    pygame.draw.rect(display, (255, 255, 255), camera.apply_rect(rect), 2)

        # Drawing Background objects
        for o in background_objects:
            if player.check_hit(o, random.choice(o.sounds)) is not None \
                    or (pygame.MOUSEBUTTONDOWN in events and pygame.mouse.get_pressed()[0]
                        and o.rect.collidepoint(camera.reverse(pygame.mouse.get_pos()))):
                display.blit(o.h_img, camera.apply(o))
                if o.hp - player.damage > 0:
                    o.hp -= player.damage
                else:
                    print("BKG:", o.mat, o.name, o.type)
                    player.inventory_add_object(copy(o))
                    background_objects.remove(o)
            else:
                display.blit(o.img, camera.apply(o))

        # Cheking on platforms
        for p in platforms:
            if pygame.mouse.get_pressed()[0] and p.rect.collidepoint(camera.reverse(pygame.mouse.get_pos())):
                player.hitting = True
                if not player.hitted:
                    p.hp -= player.damage
                    player.hitted = True
                    if p.hp <= 0:
                        print("PLT:", p.mat, p.name, p.type)
                        platforms.remove(p)
                        entities.remove(p)
                        player.inventory_add_object(p)
            if not player.hitting:
                player.hitted = False

        # Drawing collidable objects.
        for e in entities:
            display.blit(e.img, camera.apply(e))

        # Baking Light.
        if level.lighting:
            bake_light(display, clear_image_filter, camera, player, light)

        # Drawing debug data.
        if keys[pygame.K_F1]:
            player.draw_mask(display, color=(0, 0, 0))
            show_fps(display, clock, font, color=(0, 0, 0))
            show_info(display, f"{player.rect.x}; {player.rect.y + player.rect.h}", font, color=(0, 0, 0))

        # Drawing Player inventory.
        player.draw_inventory(display, font)

        pygame.display.update()

        # Restarting Level.
        if keys[pygame.K_F5]:
            background_objects = list(map(lambda x: copy(x), level.background_objects))
            player.inventory = []

        # Exit Game.
        if keys[pygame.K_ESCAPE]:
            load_dict = {"Game-Objects": [entities, platforms, background_tiles],
                         "Background-Objects": background_objects,
                         "Camera": camera}
            """Saving code"""
            raise SystemExit("Escape")

        # Go to next level.
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


def vertical_gradient(size, startcolor, endcolor):
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    height = size[1]
    bigSurf = pygame.Surface((1, height)).convert_alpha()
    dd = 1.0 / height
    sr, sg, sb = startcolor
    er, eg, eb = endcolor
    rm = (er - sr) * dd
    gm = (eg - sg) * dd
    bm = (eb - sb) * dd
    for y in range(height):
        bigSurf.set_at((0, y),
                       (int(sr + rm * y),
                        int(sg + gm * y),
                        int(sb + bm * y)
                        ))
    return pygame.transform.scale(bigSurf, size)


pygame.init()
from pygame.locals import *

flags = DOUBLEBUF | FULLSCREEN
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), flags)

while True:
    run(Plain(), display, player1)
    run(Polygon(), display, player1)

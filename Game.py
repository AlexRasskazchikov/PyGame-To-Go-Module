import pickle
import random
from copy import copy

import pygame

from Engine import show_fps, show_info, bake_light
from Engine.Characters import player1
from Engine.Levels import Plain, BackgroundObject, Polygon

WIN_WIDTH = 1366
WIN_HEIGHT = 768
HALF_WIDTH = WIN_WIDTH // 2
HALF_HEIGHT = WIN_HEIGHT // 2

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
    portal.play()
    clock = pygame.time.Clock()
    if not load:
        player1.set_coords(level.spawn, start=True)
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

    position_line = pygame.Surface((485, 7), pygame.SRCALPHA, 32)
    position_line.fill((255, 255, 255, 110))
    player_position = pygame.Surface((11, 21), pygame.SRCALPHA, 32)
    player_position.fill((255, 255, 255, 110))

    Run = True

    while Run:
        clock.tick(100)
        FramesClock += 1

        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        events_type = list(map(lambda x: x.type, events))
        mouse_pressed = pygame.mouse.get_pressed()

        """display.fill((0, 0, 0))"""
        display.blit(gradient, (0, 0))
        player.update_frame(keys, FramesClock)
        player.update_mask()
        camera.update(player1)
        player.update(keys, platforms)
        mouse = camera.reverse(pygame.mouse.get_pos())

        for i in range(len(player.inventory)):
            if pygame.MOUSEBUTTONDOWN in events_type and pygame.mouse.get_pressed()[2] and player.inventory[i].choosen:
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
            if "portal" in o.name or "protector" in o.name:
                protectors = {"micro": 10}
                if "protector" in o.name:
                    rad = (FramesClock % cell_height * protectors[o.name.split("-")[0]] // 2)
                else:
                    rad = (FramesClock % 500)
                coords = list(map(lambda x: x + 32, camera.apply_rect(o.rect)[:2]))
                if rad >= 1:
                    pygame.draw.circle(display, (100, 100, 100), coords, rad, 1)

            if "portal" in o.name:
                if player.collides(o) and keys[pygame.K_e]:
                    Run = False

            if player.check_hit(o) is not None \
                    or (pygame.MOUSEBUTTONDOWN in events_type and mouse_pressed[0]) and o.rect.collidepoint(mouse):
                display.blit(o.h_img, camera.apply(o))
                random.choice(o.sounds).play()
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
            if mouse_pressed[0] and p.rect.collidepoint(mouse):
                player.hitting = True
                if not player.hitted:
                    p.hp -= player.damage
                    player.hitted = True
                    random.choice(p.sounds).play()

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
            player.draw_mask(display, color=(255, 255, 255))
            show_fps(display, clock, font, color=(255, 255, 255))
            show_info(display, f"{player.rect.x}; {player.rect.y + player.rect.h}", font, color=(255, 255, 255))

        # Drawing Player inventory.
        player.draw_inventory(display, font)

        # Drawing map.
        display.blit(position_line, (440, 54))
        display.blit(player_position, (map_coords_calculate(player.rect.x, level.total_level_width), 33))
        print(map_coords_calculate(player.rect.x, level.total_level_width))

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


def map_coords_calculate(player_x, level_width=2000, map_width=485, map_delta_x=440):
    return int((player_x / level_width) * map_width + map_delta_x)


pygame.init()
from pygame.locals import *

flags = DOUBLEBUF | FULLSCREEN
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), flags)
portal = pygame.mixer.Sound(r"DEEPWORLD 3.0/portal.wav")
pygame.mixer.music.load(r"DEEPWORLD 3.0/main.mp3")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(999)

while True:
    run(Plain(), display, player1)
    run(Polygon(), display, player1)

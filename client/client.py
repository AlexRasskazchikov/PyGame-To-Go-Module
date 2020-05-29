import random
from copy import copy

import pygame
from pygame.rect import Rect

from Engine.Characters import Player1
from Engine.Levels import Polygon
from functions import vertical_gradient, inventory_add_object, show_info, show_fps
from network import Network
from player import Player

WIN_WIDTH = 1366
WIN_WIDTH = 500
WIN_HEIGHT = 768
WIN_HEIGHT = 500
HALF_WIDTH = WIN_WIDTH // 2
HALF_HEIGHT = WIN_HEIGHT // 2

CAMERA_SLACK = 500
ch = 50
display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Client")

PACK = Player1

ground = pygame.Surface((ch, ch))
ground.fill((125, 125, 125))
construct = pygame.Surface((ch, ch))
construct.fill((156, 156, 159))

sprites = {
    "ground": ground,
    "construct": construct,
    "right": pygame.Surface((ch, ch)),
    "left": pygame.Surface((ch, ch)),
    "earth": pygame.Surface((ch, ch)),
}


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


def check_connection(*ps):
    for p in ps:
        if p is None:
            raise SystemError("Сервер недоступен.")
        if isinstance(p, str):
            raise SystemError(p)


def redrawWindow(win, player, player2, keys, FramesClock, camera):
    p1, p2 = player.img.split(":"), player2.img.split(":")

    win.blit(PACK[p1[0]][int(p1[1])], camera.apply_rect(player.rect))
    win.blit(PACK[p2[0]][int(p2[1])], camera.apply_rect(player2.rect))

    player.update_frame(keys, FramesClock, PACK)


def main(level):
    camera = Camera(complex_camera, level.total_level_width, level.total_level_height)

    gradient = vertical_gradient((WIN_WIDTH, WIN_HEIGHT), (107, 116, 202), (211, 211, 211))
    font = pygame.font.Font(r'C:\Windows\Fonts\Arial.ttf', 25)

    entities, platforms, background_tiles = level.render_files()
    level.background_objects = list(map(lambda x: copy(x), level.background_objects)) + list(
        map(lambda x: copy(x), background_tiles))

    run = True
    n = Network()

    player_coords, player_img = n.getP()
    player = Player(*player_coords, 170, 100)
    player.img = player_img
    p2 = Player(0, 0, 170, 100)

    clock = pygame.time.Clock()
    FramesClock = 1

    while run:
        clock.tick(100)
        FramesClock += 1
        display.blit(gradient, (0, 0))

        keys = pygame.key.get_pressed()
        events = list(map(lambda x: x.type, pygame.event.get()))
        mouse_pressed = pygame.mouse.get_pressed()
        mouse = camera.reverse(pygame.mouse.get_pos())

        coords, image = n.send(([player.rect.x, player.rect.y], player.img))
        p2.rect.x, p2.rect.y = coords
        p2.img = image

        check_connection(player)
        player.move(keys, platforms)

        if pygame.QUIT in events:
            run = False

        camera.update(player)

        # Cheking on platforms
        for p in platforms:
            if mouse_pressed[0] and p.rect.collidepoint(mouse):
                player.hitting = True
                if not player.hitted:
                    p.hp -= player.damage
                    player.hitted = True
                    random.choice(p.sounds).play()

                    if p.hp <= 0:
                        print("PLT:", p.name, p.type)
                        platforms.remove(p)
                        entities.remove(p)
                        inventory_add_object(player, p)

            if not player.hitting:
                player.hitted = False

        # Drawing collidable objects.
        for e in entities:
            display.blit(sprites[e.img], camera.apply_rect(e.rect))

        p1_img, p2_img = player.img.split(":"), p2.img.split(":")

        display.blit(PACK[p1_img[0]][int(p1_img[1])], camera.apply_rect(player.rect))
        display.blit(PACK[p2_img[0]][int(p2_img[1])], camera.apply_rect(p2.rect))

        show_fps(display, clock, font, color=(255, 255, 255))
        show_info(display, f"{player.rect.x}; {player.rect.y + player.rect.h}", font, color=(255, 255, 255))

        player.update_frame(keys, FramesClock, PACK)
        player.draw_inventory(display, font, sprites, coords=(WIN_WIDTH // 3, 10))
        pygame.display.update()


main(Polygon())

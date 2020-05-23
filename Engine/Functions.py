import random

import pygame


def show_fps(display, clock):
    """This function draws current fps on screen"""
    font = pygame.font.Font(r'C:\Windows\Fonts\Arial.ttf', 25)
    text = font.render(str(int(clock.get_fps())), True, (255, 0, 0))
    display.blit(text, (25, 25))


def draw(display, *players):
    """This function redraws chosen objects"""
    for player in players:
        player.draw(display)


def npc(player=None, reactionSpeed=250, sleepDiapasone=(100, 150), FramesClock=None, borders=True):
    """NPC Logic."""
    w, h = pygame.display.get_surface().get_size()
    if player is None:
        raise ValueError("There is no Player given.")
    if FramesClock is None:
        raise ValueError("There is no FramesClock given.")
    if FramesClock >= player.awakeFrame:
        if not FramesClock % reactionSpeed:
            if player.act == "left":
                player.act = "right"
                player.awakeFrame += random.randint(*sleepDiapasone)
            else:
                player.act = "left"
                player.awakeFrame += random.randint(*sleepDiapasone)
        if player.act == "left":
            if player.border_collision and borders:
                if player.coords[0] - player.speed < 0:
                    player.coords = [0, player.coords[1]]
                else:
                    player.left()
                    player.set_sprite_from_pack("run-left", FramesClock // 17 % 6)
                    player.direction = "left"
            else:
                player.left()
                player.set_sprite_from_pack("run-left", FramesClock // 17 % 6)
                player.direction = "left"
        else:
            if player.border_collision and borders:
                if player.coords[0] + player.width + player.speed > w:
                    player.coords = [w - player.width, player.coords[1]]

                else:
                    player.right()
                    player.set_sprite_from_pack("run-right", FramesClock // 17 % 6)
                    player.direction = "right"
            else:
                player.right()
                player.set_sprite_from_pack("run-right", FramesClock // 17 % 6)
                player.direction = "right"
    else:
        if player.direction == "right":
            player.set_sprite_from_pack("idle-right", FramesClock // 40 % 3)
        else:
            player.set_sprite_from_pack("idle-left", FramesClock // 40 % 3)

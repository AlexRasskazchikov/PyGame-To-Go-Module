import random

import pygame


def move(players, keys, display, borders=True):
    """This function checks, if someone need to move and draws them in right position."""
    w, h = pygame.display.get_surface().get_size()
    for player in players:
        if "left" in player.controls:
            if keys[player.controls["left"]]:

                if player.border_collision and borders:
                    if player.coords[0] - player.speed < 0:
                        player.coords = [0, player.coords[1]]

                    else:
                        player.left()
                else:
                    player.left()

        if "right" in player.controls:
            if keys[player.controls["right"]]:

                if player.border_collision and borders:
                    if player.coords[0] + player.width + player.speed > w:
                        player.coords = [w - player.width, player.coords[1]]

                    else:
                        player.right()
                else:
                    player.right()

        if "up" in player.controls:
            if keys[player.controls["up"]]:

                if player.border_collision and borders:
                    if player.coords[1] - player.speed - player.width < 0:
                        player.coords = [player.coords[0], player.width]

                    else:
                        player.up()
                else:
                    player.up()

        if "down" in player.controls:
            if keys[player.controls["down"]]:
                if player.border_collision and borders:
                    if player.coords[1] + player.height + player.speed > h:
                        player.coords = [player.coords[0], h - player.height]

                    else:
                        player.down()
                else:
                    player.down()

        if "reset-position" in player.controls:
            if keys[player.controls["reset-position"]]:
                player.setCoords(player.startCoords)
        player.draw(display)


def events(eventList):
    for event in eventList:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


def npc(player=None, reactionSpeed=100, sleepDiapasone=(300, 400), FramesClock=None, borders=True):
    """NPC Logic."""
    w, h = pygame.display.get_surface().get_size()

    if player is None:
        raise ValueError("В логике NPC не указан Игрок.")

    if FramesClock is None:
        raise ValueError("В логике NPC не указан FramesClock.")

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
            else:
                player.left()
        else:
            if player.border_collision and borders:
                if player.coords[0] + player.width + player.speed > w:
                    player.coords = [w - player.width, player.coords[1]]

                else:
                    player.right()
            else:
                player.right()

import pygame
from Engine.Characters import player1, knight
from Engine.Colors import *

pygame.init()

display = pygame.display.set_mode((1200, 600))
pygame.display.toggle_fullscreen()
pygame.display.set_caption("Engine Testing")


def run(*players):
    clock, FramesClock = pygame.time.Clock(), 0
    player1 = players[0]
    player2 = players[1]
    while True:
        FramesClock += 1
        keys = pygame.key.get_pressed()
        events = list(map(lambda x: int(x.type), pygame.event.get()))
        if pygame.QUIT in events:
            pygame.quit()
            quit()
        player1.update_frame(keys, FramesClock)
        player2.update_frame(keys, FramesClock)
        player1.move(keys)
        player2.move(keys)
        display.fill(Black)
        if player1.hit_collides(player2):
            player1.color = Red
        else:
            player1.color = White
        if player2.hit_collides(player1):
            player2.color = Red
        else:
            player2.color = White
        player1.draw(display)
        player2.draw(display)
        pygame.display.update()
        clock.tick(100)


run(player1, knight)

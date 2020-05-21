import pygame

from Engine.Colors import *
from Engine.Functions import npc, move, events
from Engine.Player import Player

pygame.init()

display = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Engine Testing")

player1 = Player(controls={"left": pygame.K_LEFT,
                           "right": pygame.K_RIGHT,
                           "up": pygame.K_UP,
                           "down": pygame.K_DOWN,
                           "reset-position": pygame.K_r}, coords=(10, 400), speed=3)
player1.setColor(White)

player2 = Player(controls={"left": 1,
                           "right": 1,
                           "up": 1,
                           "down": 1,
                           "reset-position": pygame.K_t}, coords=(80, 400), speed=2)
player2.setColor(Green)


def run(*players):
    clock = pygame.time.Clock()
    FramesClock = 0
    while True:
        FramesClock += 1
        display.fill(Black)
        move(players, pygame.key.get_pressed(), display)
        npc(player2, FramesClock=FramesClock)
        events(pygame.event.get())
        pygame.display.update()
        clock.tick(100)


run(player1, player2)

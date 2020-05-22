import pygame

from Engine.Animations import AnimationPack
from Engine.Colors import *
from Engine.Player import Player

pygame.init()

display = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Engine Testing")

Player1 = AnimationPack()
Player1.add_animation_set("run-right", r"C:\Users\Alex\Desktop\MainProj\Assets\pl1Run")
Player1.add_animation_set("idle-right", r"C:\Users\Alex\Desktop\MainProj\Assets\pl1Idle")
Player1.add_animation_set("hit1-right", r"C:\Users\Alex\Desktop\MainProj\Assets\p1Hit1")
Player1.add_animation_set("hit2-right", r"C:\Users\Alex\Desktop\MainProj\Assets\p1Hit2")
Player1.add_animation_set("hit3-right", r"C:\Users\Alex\Desktop\MainProj\Assets\p1Hit3")

Player1.create_flipped_animation_set("hit1-right")
Player1.create_flipped_animation_set("hit2-right")
Player1.create_flipped_animation_set("hit3-right")
Player1.create_flipped_animation_set("run-right")
Player1.create_flipped_animation_set("idle-right")

player1 = Player(controls={"left": pygame.K_a, "right": pygame.K_d,
                           "reset-position": pygame.K_r, "hit": pygame.K_SPACE}, speed=3, size=(200, 148),
                 animation_pack=Player1)
player1.setColor(Yellow)
player1.setCoords((10, pygame.display.get_surface().get_size()[1] - player1.height))


def run(*players):
    clock, FramesClock = pygame.time.Clock(), 0

    while True:
        FramesClock += 1

        keys = pygame.key.get_pressed()
        events = list(map(lambda x: int(x.type), pygame.event.get()))
        player = players[0]

        if pygame.QUIT in events:
            pygame.quit()
            quit()

        player.update_frame(keys, FramesClock)
        player.move(keys)

        display.fill(Black)
        player.draw(display)

        pygame.display.update()
        clock.tick(100)


run(player1)

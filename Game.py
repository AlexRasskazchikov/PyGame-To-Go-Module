import pygame

from Engine.Animations import AnimationPack
from Engine.Colors import *
from Engine.Functions import npc, move, events
from Engine.Player import Player

pygame.init()

display = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Engine Testing")

Player1 = AnimationPack()
Player1.add_animation_set("run-right", r"C:\Users\Alex\Desktop\MainProj\Assets\pl1Run")
Player1.add_animation_set("idle-right", r"C:\Users\Alex\Desktop\MainProj\Assets\pl1Idle")
Player1.create_flipped_animation_set("run-right")
Player1.create_flipped_animation_set("idle-right")
print(Player1)

player1 = Player(controls={"left": pygame.K_a,
                           "right": pygame.K_d,
                           "up": pygame.K_w,
                           "down": pygame.K_s,
                           "reset-position": pygame.K_r},
                 speed=3,
                 animation_pack=Player1,
                 size=(200, 148))
player1.setColor(White)
player1.setCoords((10, pygame.display.get_surface().get_size()[1] - player1.height))

player2 = Player(controls={"left": 1,
                           "right": 1,
                           "up": 1,
                           "down": 1,
                           "reset-position": pygame.K_t}, speed=2, animation_pack=Player1, size=(200, 148))
player2.setColor(Green)


def run(*players):
    clock = pygame.time.Clock()
    FramesClock = 0
    flag = False
    while True:
        FramesClock += 1
        keys = pygame.key.get_pressed()
        player = players[0]

        if keys[player.controls["right"]]:
            player.set_sprite_from_pack("run-right", FramesClock // 17 % 6)
            player.direction = "right"
        elif keys[player.controls["left"]]:
            player.set_sprite_from_pack("run-left", FramesClock // 17 % 6)
            player.direction = "left"
        elif keys[player.controls["up"]] or keys[player.controls["down"]]:
            player.set_sprite_from_pack(f"run-{player.direction}", FramesClock // 17 % 6)
        else:
            if player.direction == "right":
                player.set_sprite_from_pack("idle-right", FramesClock // 40 % 3)
            else:
                player.set_sprite_from_pack("idle-left", FramesClock // 40 % 3)

        display.fill(Black)
        move(players, keys, display)
        npc(player2, FramesClock=FramesClock)
        npc(player1, FramesClock=FramesClock)
        events(pygame.event.get())
        pygame.display.update()
        clock.tick(100)


run(player1, player2)

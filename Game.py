import pygame

from Engine.Animations import AnimationPack
from Engine.Colors import *
from Engine.Player import Player

pygame.init()

display = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Engine Testing")

Player1 = AnimationPack()
Player1.add_animation_set("run-right", r"Assets/Hero\Run")
Player1.add_animation_set("idle-right", r"C:\Users\Alex\Desktop\MainProj\Assets\Hero\Idle")
Player1.add_animation_set("hit1-right", r"C:\Users\Alex\Desktop\MainProj\Assets\Hero\Hit1")
Player1.add_animation_set("hit2-right", r"C:\Users\Alex\Desktop\MainProj\Assets\Hero\Hit2")
Player1.add_animation_set("hit3-right", r"C:\Users\Alex\Desktop\MainProj\Assets\Hero\Hit3")
Player1.create_flipped_animation_set("hit1-right")
Player1.create_flipped_animation_set("hit2-right")
Player1.create_flipped_animation_set("hit3-right")
Player1.create_flipped_animation_set("run-right")
Player1.create_flipped_animation_set("idle-right")
Player1.set_animation_count({"hit": 3})

Knight = AnimationPack()
Knight.add_animation_set("run-right", r"C:\Users\Alex\Desktop\MainProj\Assets\Knight\Run")
Knight.add_animation_set("idle-right", r"C:\Users\Alex\Desktop\MainProj\Assets\Knight\Idle")
Knight.add_animation_set("hit1-right", r"C:\Users\Alex\Desktop\MainProj\Assets\Knight\Hit1")
Knight.add_animation_set("hit2-right", r"C:\Users\Alex\Desktop\MainProj\Assets\Knight\Hit2")
Knight.create_flipped_animation_set("run-right")
Knight.create_flipped_animation_set("idle-right")
Knight.create_flipped_animation_set("hit1-right")
Knight.create_flipped_animation_set("hit2-right")
Knight.set_animation_count({"hit": 2})

knight = Player(controls={"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "down": pygame.K_DOWN, "up": pygame.K_UP, "hit": pygame.K_l},
                animation_pack=Knight, size=(240, 240), speed=5, name="Knight")
knight.setColor(Green)
knight.direction = "left"
knight.name_delta_x = 80
knight.name_delta_y = 80
knight.setCoords((500, pygame.display.get_surface().get_size()[1] - knight.height))

player1 = Player(controls={"left": pygame.K_a, "right": pygame.K_d, "reset-position": pygame.K_r, "hit": pygame.K_SPACE},
                 speed=3, size=(200, 148), animation_pack=Player1, name="Alex")
player1.setColor(Yellow)
player1.name_delta_x = 80
player1.setCoords((10, pygame.display.get_surface().get_size()[1] - player1.height))


def run(*players):
    clock, FramesClock = pygame.time.Clock(), 0
    player = players[0]
    knight = players[1]
    while True:
        FramesClock += 1
        keys = pygame.key.get_pressed()
        events = list(map(lambda x: int(x.type), pygame.event.get()))
        if pygame.QUIT in events:
            pygame.quit()
            quit()
        player.update_frame(keys, FramesClock)
        knight.update_frame(keys, FramesClock)
        player.move(keys)
        knight.move(keys)

        display.fill(Black)

        player.draw(display)
        knight.draw(display)

        offset_x, offset_y = (knight.rect.left - player.rect.left), (knight.rect.top - player.rect.top)
        if player.mask.overlap(knight.mask, (offset_x, offset_y)) is not None:
            if player.hitting:
                player.name = "Hit!"
                player.color = (255, 0, 0)
        if player.name == "Hit!" and not player.hitting:
            player.color = (0, 0, 0)
        pygame.display.update()
        clock.tick(100)


run(player1, knight)



import pygame

display = pygame.display.set_mode((1200, 600))
from Engine.Player import *
from Engine.Animations import AnimationPack, Level, Layer
from pygame.image import load

"""Knight Player"""
Knight = AnimationPack("Assets/Knight")
Knight.add_animation_sets("run-right", "idle-right", "hit1-right", "hit2-right")
Knight.create_flipped_animation_sets()
Knight.set_animation_count({"hit": 2})

knight = Player(speed=10)
knight.direction = "left"
knight.name_delta_x = 160
knight.name_delta_y = 150
knight.coords = (500, pygame.display.get_surface().get_size()[1] - knight.height - 20)
knight.hit_animation_speed = 7

"""Default Player"""
Player1 = AnimationPack("Assets/Hero")
Player1.add_animation_sets("run-right", "idle-right", "hit1-right", "hit2-right", "hit3-right")
Player1.create_flipped_animation_sets()
Player1.set_animation_count({"hit": 3})

player1 = Player(
    controls={"left": pygame.K_a, "right": pygame.K_d, "reset-position": pygame.K_r, "hit": pygame.K_SPACE},
    size=(350, 260), animation=Player1, speed=17)
player1.set_coords((10, pygame.display.get_surface().get_size()[1] - player1.height - 20))

player1.hit_animation_speed = 7
player1.name_delta_x = 140
player1.name_delta_y = 5

level = Level()
level.layers_set(Layer("Bushes", load(r"Assets/level1/Hills Layer 06.png"), size=(2400, 600)),
                 Layer("Hills", load(r"Assets/level1/Hills Layer 01.png"), size=(2400, 600)),
                 Layer("Ground", load(r"Assets/level1/Hills Layer 05.png"), size=(2400, 600)),
                 Layer("Trees1", load(r"Assets/level1/Hills Layer 03.png"), size=(2400, 600)),
                 Layer("Trees2", load(r"Assets/level1/Hills Layer 04.png")), )

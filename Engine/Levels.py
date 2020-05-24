import random
from copy import copy

import pygame

from Engine import calculate_coords
from Engine.Tiles import Platform, Entity


class Level:
    def __init__(self):
        self.map = []
        self.materials = {}
        self.total_level_width = 0
        self.total_level_height = 0
        self.background = (0, 0, 0)
        self.background_objects = []
        self.lighting = False

    def set_map(self, map):
        self.map = map
        self.total_level_width = len(self.map[0]) * 32
        self.total_level_height = len(self.map) * 32

    def render_files(self):
        entities = pygame.sprite.Group()
        platforms = []
        x = y = 0
        for row in self.map:
            for col in row:
                if col in self.materials:
                    p = Platform(x, y, self.materials[col])
                    platforms.append(p)
                    entities.add(p)
                x += 32
            y += 32
            x = 0
        return (entities, platforms)

    def add_background_object(self, *other):
        self.background_objects += other


class BackgroundObject(Entity):
    def __init__(self, path, coords, alph=250, size=None, name="Unknown", hp=100,
                 sounds=["Assets/sounds/tree/wood1.mp3",
                         "Assets/sounds/tree/wood2.mp3",
                         "Assets/sounds/tree/wood3.mp3",
                         "Assets/sounds/tree/wood4.mp3"], act=True, mat="Wood", mat_count=1):
        super().__init__()
        self.name = name
        self.img = pygame.image.load(path)
        if alph is not None:
            self.img.fill((255, 255, 255, alph), None, pygame.BLEND_RGBA_MULT)
        if size is not None:
            rect = self.img.get_rect(topleft=coords)
            size = (rect.w * size, rect.h * size)
            self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect(topleft=coords)
        self.coords = calculate_coords(self.rect.w, self.rect.h, *coords)[0]
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect(topleft=self.coords)

        self.mat = mat
        self.mat_count = mat_count
        self.h_img = copy(self.img)
        self.h_img.fill((50, 50, 50), special_flags=pygame.BLEND_ADD)

        self.hp, self.start_hp = hp, hp
        self.sounds = sounds

        self.act = act

    def move(self, deltax, deltay):
        self.coords = (self.coords[0] + deltax, self.coords[1] + deltay)
        self.rect = self.img.get_rect(topleft=self.coords)
        self.mask = pygame.mask.from_surface(self.img)

    def __iadd__(self, other):
        self.hp += other

    def __isub__(self, other):
        self.hp -= other

    def is_active(self):
        return self.act

    def set_active(self, bool):
        self.act = bool


"""Plain level"""
Plain = Level()
Plain.set_map([
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                     LGG",
    "                                                                                     PPP",
    "                                                                                    LPPP",
    "                                                                                    PPPP",
    "                                                                                    PPPP",
    "                                                                                    PPPP",
    "                                                                                    PPPP",
    "                                                                                    PPPP",
    "GGR                                                                                 PPPP",
    "PPPGGGGR                                                                            PPPP",
    "PPPPPPPPGGGGR                                                                       PPPP",
    "PPPPPPPPPPPPPGGR                                                                    PPPP",
    "PPPPPPPPPPPPPPPPGR                                                                  PPPP",
    "PPPPPPPPPPPPPPPPPPGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGR            LGGGGGGGGGGGGGGGGGPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR          LPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR        LPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR      LPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPGGGGGGPPPPPPPPPPPPPPPPPPPPPPPPP",
])

cloth = [r"Assets/sounds/cloth/cloth1.mp3",
         r"Assets/sounds/cloth/cloth2.mp3",
         r"Assets/sounds/cloth/cloth3.mp3",
         r"Assets/sounds/cloth/cloth4.mp3"]
trees = [r"Assets/Objects/obj_0022_Layer-23.png",
         r"Assets/Objects/obj_0021_Layer-22.png"]
clouds = [r"Assets/Objects/Cloud0.png",
          r"Assets/Objects/Cloud1.png", ]

Plain.add_background_object(
    BackgroundObject(clouds[1], (100, 300), name="Cloud", size=5, act=False, mat="Cloudy Stuff-1"),
    BackgroundObject(clouds[0], (1200, 300), name="Cloud", size=5, act=False, mat="Cloudy Stuff-2"),
    BackgroundObject(clouds[1], (1400, 300), name="Cloud", size=5, act=False, mat="Cloudy Stuff-3"),
    BackgroundObject(trees[1], (500, 0), name="Tree", size=5, mat_count=random.randint(1, 10)),
    BackgroundObject(trees[0], (1300, 0), name="Tree", size=5, mat_count=random.randint(1, 10), mat="Test"),
    BackgroundObject(trees[1], (2200, 0), name="Tree", size=5, mat_count=random.randint(1, 10)))

Plain.materials = {"G": pygame.image.load(r"Assets/Tiles/Tile_02.jpg"),
                   "P": pygame.image.load(r"Assets/Tiles/Tile_14.jpg"),
                   "L": pygame.image.load(r"Assets/Tiles/Tile_01.jpg"),
                   "R": pygame.image.load(r"Assets/Tiles/Tile_03.jpg")}

Plain.background = (5, 0, 59)

LightDemo = Level()
LightDemo.lighting = True
LightDemo.set_map([
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "                                                        ",
    "GGR                                                     ",
    "PPPGGGGR                                                ",
    "PPPPPPPPGGGGR                                       PPPP",
    "PPPPPPPPPPPPPGGR                                    PPPP",
    "PPPPPPPPPPPPPPPPGR                                  PPPP",
    "PPPPPPPPPPPPPPPPPPGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
])

LightDemo.add_background_object(
    BackgroundObject(clouds[1], (100, 300), name="Cloud", size=5, act=False, mat="Cloudy Stuff-1"),
    BackgroundObject(trees[1], (500, 0), name="Tree", size=5, mat_count=random.randint(1, 10)))

LightDemo.materials = {"G": pygame.image.load(r"Assets/Tiles/Tile_02.jpg"),
                   "P": pygame.image.load(r"Assets/Tiles/Tile_14.jpg"),
                   "L": pygame.image.load(r"Assets/Tiles/Tile_01.jpg"),
                   "R": pygame.image.load(r"Assets/Tiles/Tile_03.jpg")}
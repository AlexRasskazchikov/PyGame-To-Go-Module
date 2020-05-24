from copy import copy

import pygame
from pygame.mixer import Sound

from Engine.Tiles import Platform, Entity


class Level:
    def __init__(self):
        self.map = []
        self.materials = {}
        self.total_level_width = 0
        self.total_level_height = 0
        self.background = (0, 0, 0)
        self.background_objects = []

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
    def __init__(self, image_path, coords, alpha=250, size=None, name="Unknown", hp=100,
                 sounds=["Assets/sounds/tree/wood1.mp3",
                         "Assets/sounds/tree/wood2.mp3",
                         "Assets/sounds/tree/wood3.mp3",
                         "Assets/sounds/tree/wood4.mp3"]):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(image_path)
        if alpha is not None:
            self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        if size is not None:
            self.image = pygame.transform.scale(self.image, size)
        self.coords = coords
        self.rect = self.image.get_rect(topleft=self.coords)
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = hp
        self.start_hp = hp
        self.hitted_image = copy(self.image)
        self.hitted_image.fill((50, 50, 50), special_flags=pygame.BLEND_ADD)
        self.sounds = sounds

    def move(self, deltax, deltay):
        self.coords = (self.coords[0] + deltax, self.coords[1] + deltay)
        self.rect = self.image.get_rect(topleft=self.coords)
        self.mask = pygame.mask.from_surface(self.image)

    def __iadd__(self, other):
        self.hp += other

    def __isub__(self, other):
        self.hp -= other


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
    "PPPPPPPPPPPPPGGR                  LGGGGGR                                           PPPP",
    "PPPPPPPPPPPPPPPPGR               LPPPPPPPR                                          PPPP",
    "PPPPPPPPPPPPPPPPPPGGGGGGGGGGGGGGGPPPPPPPPPGGGGGGGGGGGR            LGGGGGGGGGGGGGGGGGPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR          LPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR        LPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR      LPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPGGGGGGPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
])

cloth = [r"Assets/sounds/cloth/cloth1.mp3",
         r"Assets/sounds/cloth/cloth2.mp3",
         r"Assets/sounds/cloth/cloth3.mp3",
         r"Assets/sounds/cloth/cloth4.mp3"]

Plain.add_background_object(BackgroundObject(r"Assets/Objects/C2013.jpg", (100, -50), name="Cloud", sounds=cloth),
                            BackgroundObject(r"Assets/Objects/C2010.jpg", (1200, -50), name="Cloud", sounds=cloth),
                            BackgroundObject(r"Assets/Objects/C2011.jpg", (1400, -50), name="Cloud", sounds=cloth),
                            BackgroundObject(r"Assets/Objects/obj_0022_Layer-23.png", (500, 150), size=(300, 330), name="Tree"),
                            BackgroundObject(r"Assets/Objects/obj_0022_Layer-23.png", (2200, 150), size=(300, 330), name="Tree"),
                            BackgroundObject(r"Assets/Objects/obj_0022_Layer-23.png", (1300, 150), size=(300, 330), name="Tree"))

Plain.materials = {"G": pygame.image.load(r"Assets/Tiles/Tile_02.jpg"),
                   "P": pygame.image.load(r"Assets/Tiles/Tile_14.jpg"),
                   "L": pygame.image.load(r"Assets/Tiles/Tile_01.jpg"),
                   "R": pygame.image.load(r"Assets/Tiles/Tile_03.jpg")}

Plain.background = (99, 182, 235)

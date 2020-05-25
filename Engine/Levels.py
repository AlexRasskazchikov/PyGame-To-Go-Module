import random
from copy import copy

import pygame

from Engine.Tiles import Entity


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
        background_tiles = []
        x = y = 0
        for row in self.map:
            for col in row:
                if col in self.materials:
                    p = BackgroundObject(image=self.materials[col],
                                         coords=(x, y),
                                         name=col, act=True, mat=col, hp=10, type="Platform")

                    if col.isupper():
                        platforms += [p]
                        entities.add(p)
                x += 32
            y += 32
            x = 0
        return entities, platforms, background_tiles

    def add_background_object(self, *other):
        self.background_objects += other


class BackgroundObject(Entity):
    def __init__(self, image, coords, size=None, name="Unknown", hp=100,
                 sounds=["Assets/sounds/tree/wood1.mp3",
                         "Assets/sounds/tree/wood2.mp3",
                         "Assets/sounds/tree/wood3.mp3",
                         "Assets/sounds/tree/wood4.mp3"], act=True, mat="Wood", amount=1, type="BackgroundObject"):
        super().__init__()
        self.name = name
        self.img = image
        if size is not None:
            rect = self.img.get_rect(topleft=coords)
            size = (rect.w * size, rect.h * size)
            self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect(topleft=coords)
        self.mask = pygame.mask.from_surface(self.img)
        self.collidable = True
        self.mat = mat
        self.amount = amount
        self.h_img = copy(self.img)
        self.h_img.fill((50, 50, 50), special_flags=pygame.BLEND_ADD)
        self.type = type
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

cloth = [r"Assets/sounds/cloth/cloth1.mp3",
             r"Assets/sounds/cloth/cloth2.mp3",
             r"Assets/sounds/cloth/cloth3.mp3",
             r"Assets/sounds/cloth/cloth4.mp3"]
trees = [pygame.image.load(r"Assets/Objects/obj_0022_Layer-23.jpg"),
         pygame.image.load(r"Assets/Objects/obj_0021_Layer-22.jpg")]
earth_sounds = [r"Assets/Sounds/grass/grass1.mp3",
                r"Assets/Sounds/grass/grass2.mp3",
                r"Assets/Sounds/grass/grass3.mp3",
                r"Assets/Sounds/grass/grass4.mp3"]
clouds = [pygame.image.load(r"Assets/Objects/Cloud0.bmp"),
          pygame.image.load(r"Assets/Objects/Cloud1.bmp"), ]

def Plain():
    """Plain level"""
    Plain = Level()
    Plain.set_map([
        "                                                                                        ",
        "                                                                                        ",
        "                                                                                        ",
        "                                                                                        ",
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
        "GGR                                w                                                PPPP",
        "PPPGGGGR                          www                                               PPPP",
        "PPPPPPPPGGGGR                    wwwww                                              PPPP",
        "PPPPPPPPPPPPPGGR                wwwwwww                                             PPPP",
        "PPPPPPPPPPPPPPPPGR             wwwwwwwww                                            PPPP",
        "PPPPPPPPPPPPPPPPPPGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGR            LGGGGGGGGGGGGGGGGGPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR          LPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR        LPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR      LPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPGGGGGGPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
    ])

    Plain.add_background_object(
        BackgroundObject(clouds[1], (100, 300), name="Cloud", size=5, act=False, mat="Cloudy Stuff-1"),
        BackgroundObject(clouds[0], (1200, 300), name="Cloud", size=5, act=False, mat="Cloudy Stuff-2"),
        BackgroundObject(clouds[1], (1400, 300), name="Cloud", size=5, act=False, mat="Cloudy Stuff-3"),
        BackgroundObject(trees[1], (500, 0), name="Tree", size=5, amount=random.randint(1, 1)),
        BackgroundObject(trees[0], (1300, 0), name="Tree", size=5, amount=random.randint(1, 1), mat="Test"),
        BackgroundObject(trees[1], (2200, 0), name="Tree", size=5, amount=random.randint(1, 1)))

    ground = pygame.transform.scale(pygame.image.load(r"Assets/Tiles/Tile_02.bmp"), (32, 32))
    right = pygame.transform.scale(pygame.image.load(r"Assets/Tiles/Tile_03.bmp"), (32, 32))
    left = pygame.transform.scale(pygame.image.load(r"Assets/Tiles/Tile_01.bmp"), (32, 32))
    earth = pygame.transform.scale(pygame.image.load(r"Assets/Tiles/Tile_14.bmp"), (32, 32))
    """earth = pygame.Surface((32, 32))
    earth.fill((91, 49, 56))"""

    house_wall = pygame.Surface((32, 32))
    house_wall.fill((92, 43, 1))

    roof = pygame.Surface((32, 32))
    roof.fill((54, 8, 0))

    Plain.materials = {"G": ground,
                       "L": left,
                       "R": right,
                       "r": roof,
                       "P": earth,
                       "w": pygame.image.load(r"Assets/Tiles/Tile_02.bmp").convert_alpha()}

    Plain.background = (105, 169, 204)
    return Plain


def LightDemo():
    LightDemo = Level()
    LightDemo.lighting = True
    LightDemo.set_map([
        "                                                        ",
        "                                                        ",
        "                                                        ",
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
        BackgroundObject(trees[1], (500, 0), name="Tree", size=5, amount=random.randint(1, 10)))

    ground = pygame.image.load(r"Assets/Tiles/Tile_02.bmp")
    right = pygame.image.load(r"Assets/Tiles/Tile_03.bmp")
    left = pygame.image.load(r"Assets/Tiles/Tile_01.bmp")
    earth = pygame.image.load(r"Assets/Tiles/Tile_14.bmp")
    """earth = pygame.Surface((32, 32))
    earth.fill((91, 49, 56))"""

    LightDemo.materials = {"G": ground,
                           "P": earth,
                           "L": left,
                           "R": right}
    return LightDemo


def Polygon():
    Polygon = Level()
    Polygon.set_map([
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                                                                                                                                               ",
        "                                 wwwww                                                                                                                         ",
        "PPPPPPPPPPPPPPPP                wwwwwww                                                                                                                        ",
        "G  G  G  G  PGGPPP             wwwwwwwww                                                                                                                       ",
        "  G  G  G  GPGGPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        " G  G  G  G PGGPPG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   GGG G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G",
        "G  G  G  G  PGGPG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G GGG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G ",
        "  G  G  G  GPGGP   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G  GG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G  ",
        " G  G  G  G PGGP  G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   GG  G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   ",
        "G  G  G  G  PGGP G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   GGG G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G",
        "  G  G  G  GPGGPG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G GGG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G ",
        " G  G  G  G PGGP   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G  GG   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G  ",
        "G  G  G  G  PGGP  G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   GG  G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   G   ",
    ])

    ground = pygame.Surface((32, 32))
    ground.fill((125, 125, 125))
    construct = pygame.Surface((32, 32))
    construct.fill((156, 156, 159))

    Polygon.materials = {"G": construct,
                         "P": ground,
                         "w": pygame.image.load(r"Assets/Tiles/Tile_02.bmp").convert_alpha()}

    Polygon.background = (105, 169, 204)
    return Polygon

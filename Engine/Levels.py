import random
from copy import copy

import pygame

from Engine.Tiles import Entity

cell_height = 50

pygame.init()


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
        self.total_level_width = len(self.map[0]) * cell_height
        self.total_level_height = len(self.map) * cell_height

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
                x += cell_height
            y += cell_height
            x = 0
        return entities, platforms, background_tiles

    def add_background_object(self, *other):
        self.background_objects += other


class BackgroundObject(Entity):
    def __init__(self, image, coords, size=None, name="Unknown", hp=100,
                 sounds=[pygame.mixer.Sound("DEEPWORLD 3.0/m2.wav"),
                         pygame.mixer.Sound("DEEPWORLD 3.0/m1.wav")], act=True, mat="Wood", amount=1,
                 type="BackgroundObject"):
        super().__init__()
        self.name = name
        self.img = image
        if size is not None:
            size = (int(cell_height * size[0]), int(cell_height * size[1]))
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

earth_sounds = [r"Assets/Sounds/grass/grass1.mp3",
                r"Assets/Sounds/grass/grass2.mp3",
                r"Assets/Sounds/grass/grass3.mp3",
                r"Assets/Sounds/grass/grass4.mp3"]
deep_world_objects = {"brass-engine": (pygame.image.load(r"DEEPWORLD 3.0/brass-engine.png")),
                      "brass-summonner": (pygame.image.load(r"DEEPWORLD 3.0/brass-summonner.png")),
                      "map": (pygame.image.load(r"DEEPWORLD 3.0/map.png")),
                      "portal": (pygame.image.load(r"DEEPWORLD 3.0/portal.png")),
                      "purple-crystal": (pygame.image.load(r"DEEPWORLD 3.0/purple-crystal.png")),
                      "red-crystal": (pygame.image.load(r"DEEPWORLD 3.0/red-crystal.png")),
                      "onyx": (pygame.image.load(r"DEEPWORLD 3.0/onyx.png")),
                      "giant-pumpkin": (pygame.image.load(r"DEEPWORLD 3.0/giant-pumpkin.png")),
                      "micro-protector": (pygame.image.load(r"DEEPWORLD 3.0/micro-protector.png")),
                      "ship-wheel": (pygame.image.load(r"DEEPWORLD 3.0/ship-wheel.png")),
                      "tiger-head": (pygame.image.load(r"DEEPWORLD 3.0/tiger-head.png")),
                      "terrapus-egg-broken": (pygame.image.load(r"DEEPWORLD 3.0/terrapus-egg-broken.png")),
                      "diamonds": (pygame.image.load(r"DEEPWORLD 3.0/diamonds.png")),
                      }


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
        BackgroundObject(deep_world_objects["portal"], (900, 750), name="portal", size=(3, 4),
                         amount=random.randint(1, 1)),
        BackgroundObject(deep_world_objects["brass-summonner"], (1300, 750), name="brass-summonner", size=(5, 4),
                         amount=random.randint(1, 1), mat="Test"),
        BackgroundObject(deep_world_objects["micro-protector"], (2200, 750), name="micro-protector", size=(1, 1),
                         amount=random.randint(1, 1)))

    ground = pygame.transform.scale(pygame.image.load(r"Assets/Tiles/Tile_02.bmp"), (cell_height, cell_height))
    right = pygame.transform.scale(pygame.image.load(r"Assets/Tiles/Tile_03.bmp"), (cell_height, cell_height))
    left = pygame.transform.scale(pygame.image.load(r"Assets/Tiles/Tile_01.bmp"), (cell_height, cell_height))
    earth = pygame.transform.scale(pygame.image.load(r"Assets/Tiles/Tile_14.bmp"), (cell_height, cell_height))

    house_wall = pygame.Surface((cell_height, cell_height))
    house_wall.fill((92, 43, 1))

    roof = pygame.Surface((cell_height, cell_height))
    roof.fill((54, 8, 0))

    Plain.materials = {"G": ground,
                       "L": left,
                       "R": right,
                       "r": roof,
                       "P": earth,
                       "w": pygame.image.load(r"Assets/Tiles/Tile_02.bmp").convert_alpha()}

    Plain.background = (105, 169, 204)
    Plain.spawn = (1000, 900)
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

    ground = pygame.image.load(r"Assets/Tiles/Tile_02.bmp")
    right = pygame.image.load(r"Assets/Tiles/Tile_03.bmp")
    left = pygame.image.load(r"Assets/Tiles/Tile_01.bmp")
    earth = pygame.image.load(r"Assets/Tiles/Tile_14.bmp")
    """earth = pygame.Surface((cell_height, cell_height))
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

    ground = pygame.Surface((cell_height, cell_height))
    ground.fill((125, 125, 125))
    construct = pygame.Surface((cell_height, cell_height))
    construct.fill((156, 156, 159))

    Polygon.materials = {"G": construct,
                         "P": ground,
                         "w": pygame.image.load(r"Assets/Tiles/Tile_02.bmp").convert_alpha()}

    Polygon.add_background_object(
        BackgroundObject(deep_world_objects["portal"], (600, 450), name="portal", size=(3, 4),
                         amount=random.randint(1, 1)))

    Polygon.background = (105, 169, 204)
    Polygon.spawn = (464, 750)
    return Polygon

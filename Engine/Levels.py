import pygame

from Engine.Tiles import Platform


class Level:
    def __init__(self):
        self.map = []
        self.materials = {}
        self.total_level_width = 0
        self.total_level_height = 0
        self.background = (255, 255, 255)

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

    def set_background(self, background):
        self.background = background


"""Plain level"""
Plain = Level()
Plain.set_map([
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                        ",
    "                                  GGGGGGGGGGGGGGGGGG                                    ",
    "                                                                                        ",
    "                                                                                        ",
    "GGGGGGGGGGGGGGGGGG                                                                      ",
    "                                                                 GGGGGGGGGGGGGGGGGG     ",
    "                                                                                        ",
    "GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP", ])
Plain.set_background((148, 207, 255))
Plain.materials = {"G": pygame.image.load(r"Assets/Tiles/Tile_02.png"),
                   "P": pygame.image.load(r"Assets/Tiles/Tile_14.png")}

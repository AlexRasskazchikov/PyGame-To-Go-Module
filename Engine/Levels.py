import pygame

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
    def __init__(self, image_path, coords, alpha=None, size=None, name="Unknown"):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(image_path)
        if alpha is not None:
            self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        if size is not None:
            self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=coords)
        self.mask = pygame.mask.from_surface(self.image)


"""Plain level"""
Plain = Level()
Plain.set_map([
    "                                                                                        ",
    "                                                                                        ",
    "                                                                                     GGG",
    "                                                                                     PPP",
    "                                                                                    GPPP",
    "                                                                                    PPPP",
    "                                                                                    PPPP",
    "                                                                                    PPPP",
    "                                                                                    PPPP",
    "                                                                                    PPPP",
    "GGG                                                                                 PPPP",
    "PPPGGGGG                                                                            PPPP",
    "PPPPPPPPGGGGG                                                                       PPPP",
    "PPPPPPPPPPPPPGGG                  GGGGGGG                                           PPPP",
    "PPPPPPPPPPPPPPPPGG               GPPPPPPPG                                          PPPP",
    "PPPPPPPPPPPPPPPPPPGGGGGGGGGGGGGGGPPPPPPPPPGGGGGGGGGGGG            GGGGGGGGGGGGGGGGGGPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPG          GPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPG        GPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPG      GPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPGGGGGGPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
])
Plain.add_background_object(BackgroundObject(r"Assets/Objects/C2013.jpg", (100, -50), name="Cloud"),
                            BackgroundObject(r"Assets/Objects/C2010.jpg", (700, -50), name="Cloud"),
                            BackgroundObject(r"Assets/Objects/C2011.jpg", (1400, -50), name="Cloud"),
                            BackgroundObject(r"Assets/Objects/obj_0022_Layer-23.png", (500, 150), size=(300, 330), name="Tree"))

Plain.materials = {"G": pygame.image.load(r"Assets/Tiles/Tile_02.jpg"),
                   "P": pygame.image.load(r"Assets/Tiles/Tile_14.jpg")}

Plain.background = (109, 144, 209)
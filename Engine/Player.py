from pygame import draw


class Player:
    def __init__(self, size=(50, 100), speed=10,
                 color=(255, 0, 0), controls=None,
                 coords=None):
        self.coords, self.speed = [0, 0], speed
        self.width, self.height = size
        self.controls = controls
        self.color = color
        if coords is not None:
            self.coords = coords

    def right(self):
        """Moves player right on self.speed pixels."""
        self.coords = (self.coords[0] + self.speed, self.coords[1])

    def left(self):
        """Moves player left on self.speed pixels."""
        self.coords = (self.coords[0] - self.speed, self.coords[1])

    def up(self):
        """Moves Player Up"""
        self.coords = (self.coords[0], self.coords[1] - self.speed)

    def down(self):
        """Moves Player Down"""
        self.coords = (self.coords[0], self.coords[1] + self.speed)

    def jump(self):
        """Player jumps"""
        pass

    def collisionWith(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def setColor(self, new_color):
        """Changes Player color"""
        self.color = new_color

    def setCoords(self, new_cords):
        """Sets new coords to player"""
        self.coords = new_cords

    def draw(self, screen):
        """Draw Player on choosen screen"""
        draw.rect(screen, self.color,
                  (*self.coords, self.width, self.height))
        draw.circle(screen, self.color,
                    (self.coords[0] + self.width // 2, self.coords[1] - self.width // 2),
                    self.width // 2)

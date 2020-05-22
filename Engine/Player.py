import random

import pygame
from pygame import draw
from pygame import transform


class Player:
    def __init__(self, size=(50, 100), speed=1, color=(255, 0, 0), controls=None,
                 coords=None, b_collision=True, animation_pack=None):

        """Position & Controls Block."""
        self.border_collision = b_collision
        self.width, self.height = size
        self.controls = controls
        self.speed = speed
        self.coords = (10, pygame.display.get_surface().get_size()[1] - self.height)
        self.start_coords = self.coords
        if coords is not None:
            self.coords = coords
            self.start_coords = self.coords

        """Animation variables."""
        self.anim_id = random.randint(1, 3)
        self.animation = animation_pack
        self.walk_animation_speed = 17
        self.idle_animation_speed = 40
        self.hit_animation_speed = 15
        self.direction = "right"
        self.hitting = False
        self.anim_count = 0
        self.color = color
        self.image = None
        if animation_pack is not None:
            self.image = transform.scale(animation_pack[list(animation_pack.get_sets_names())[0]][0],
                                         (self.width, self.height))

        """NPC Block."""
        self.act = "left"
        self.sleep = True
        self.awakeFrame = 50

    def right(self):
        """Moves player right on self.speed pixels."""
        self.coords = (self.coords[0] + self.speed, self.coords[1])
        return self.coords

    def left(self):
        """Moves player left on self.speed pixels."""
        self.coords = (self.coords[0] - self.speed, self.coords[1])
        return self.coords

    def up(self):
        """Moves Player Up"""
        self.coords = (self.coords[0], self.coords[1] - self.speed)

    def down(self):
        """Moves Player Down"""
        self.coords = (self.coords[0], self.coords[1] + self.speed)

    def jump(self):
        """Player jumps"""
        pass

    def setColor(self, new_color):
        """Changes Player color"""
        self.color = new_color

    def setCoords(self, new_cords):
        """Sets new coords to player"""
        if self.start_coords is None:
            self.start_coords = new_cords
        self.coords = new_cords

    def draw(self, screen):
        """Draw Player on choosen screen"""
        if self.image is None:
            draw.rect(screen, self.color,
                      (*self.coords, self.width, self.height))
        else:
            screen.blit(self.image, self.coords)

    def set_sprite_from_pack(self, name, index):
        """Change player's sprite to sprite from Pack"""
        if self.animation:
            self.image = transform.scale(self.animation.get_frame(name, index), (self.width, self.height))
        else:
            pass

    def set_sprite_from_image(self, image):
        """Change player's sprite to your image"""
        self.image = transform.scale(image, (self.width, self.height))

    def update_frame(self, keys, FramesClock):
        if "hit" in self.controls and keys[self.controls["hit"]]:
            self.hitting = True
        if self.hitting and self.animation:
            if self.anim_count == (self.animation.get_len(f"hit{self.anim_id}-{self.direction}") - 1) * self.hit_animation_speed:
                self.anim_count, self.hitting = 0, False
                self.anim_id = random.randint(1, self.animation.get_count("hit"))
            else:
                self.anim_count += 1
                self.set_sprite_from_pack(f"hit{self.anim_id}-{self.direction}", self.anim_count // self.hit_animation_speed)
        else:
            if "right" in self.controls and keys[self.controls["right"]]:
                self.set_sprite_from_pack("run-right",
                                          FramesClock // self.walk_animation_speed % self.animation.get_len("run-right"))
                self.direction = "right"
            elif "left" in self.controls and keys[self.controls["left"]]:
                self.set_sprite_from_pack("run-left",
                                          FramesClock // self.walk_animation_speed % self.animation.get_len("run-left"))
                self.direction = "left"
            else:
                if self.direction == "right":
                    self.set_sprite_from_pack("idle-right",
                                              FramesClock // self.idle_animation_speed % self.animation.get_len(
                                                  "idle-right"))
                else:
                    self.set_sprite_from_pack("idle-left",
                                              FramesClock // self.idle_animation_speed % self.animation.get_len(
                                                  "idle-left"))

    def move(self, keys, borders=True):
        if not self.hitting:
            w, h = pygame.display.get_surface().get_size()
            if "left" in self.controls and keys[self.controls["left"]]:
                if self.border_collision and borders:
                    if self.coords[0] - self.speed < 0:
                        self.coords = [0, self.coords[1]]
                    else:
                        self.left()
                else:
                    self.left()

            if "right" in self.controls and keys[self.controls["right"]]:
                if self.border_collision and borders:
                    if self.coords[0] + self.width + self.speed > w:
                        self.coords = [w - self.width, self.coords[1]]
                    else:
                        self.right()
                else:
                    self.right()

            if "up" in self.controls and keys[self.controls["up"]]:
                if self.border_collision and borders:
                    if self.coords[1] - self.speed < 0:
                        self.coords = [self.coords[0], 0]
                    else:
                        self.up()
                else:
                    self.up()

            if "down" in self.controls and keys[self.controls["down"]]:
                if self.border_collision and borders:
                    if self.coords[1] + self.height + self.speed > h:
                        self.coords = [self.coords[0], h - self.height]
                    else:
                        self.down()
                else:
                    self.down()

            if "reset-position" in self.controls and keys[self.controls["reset-position"]]:
                self.setCoords(self.start_coords)

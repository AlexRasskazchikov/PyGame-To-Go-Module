import random

import pygame

from Engine.Tiles import ExitBlock


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(Entity):
    def __init__(self, coords=(50, 50), size=(148, 200), speed=5, jump=15,
                 animation=None, controls={"up": pygame.K_w, "right": pygame.K_d,
                                           "left": pygame.K_a, "hit": pygame.K_SPACE}):
        Entity.__init__(self)
        self.width, self.height = size
        self.coords = coords
        self.start_coords = coords
        self.xvel, self.yvel = 0, 0
        self.onGround = False
        self.controls = controls
        self.anim_count, self.hitting = 0, False
        self.animation = animation
        self.hit_animation_speed = 5
        self.walk_animation_speed = 5
        self.idle_animation_speed = 5
        self.anim_id = 1
        self.direction = "right"
        self.speed = speed
        self.jump = jump
        if self.animation is not None:
            self.image = pygame.transform.scale(self.animation[list(self.animation.get_sets_names())[0]][0],
                                                (self.width, self.height))
            self.rect = self.image.get_rect(topleft=self.coords)
            self.mask = pygame.mask.from_surface(self.image)

    def set_sprite_from_pack(self, name, index):
        """Change player's sprite to sprite from Pack"""
        if self.animation:
            self.image = pygame.transform.scale(self.animation.get_frame(name, index), (self.width, self.height))
        else:
            pass

    def update_frame(self, keys, FramesClock):
        """Animates player"""
        if "hit" in self.controls and keys[self.controls["hit"]]:
            self.hitting = True
        if self.hitting and self.animation:
            if self.anim_count == (
                    self.animation.get_len(f"hit{self.anim_id}-{self.direction}") - 1) * self.hit_animation_speed:
                self.anim_count, self.hitting = 0, False
                self.anim_id = random.randint(1, self.animation.get_count("hit"))
            else:
                self.anim_count += 1
                self.set_sprite_from_pack(f"hit{self.anim_id}-{self.direction}",
                                          self.anim_count // self.hit_animation_speed)
        else:
            run_anim_speed = FramesClock // self.walk_animation_speed % self.animation.get_len("run-right")
            if "right" in self.controls and keys[self.controls["right"]]:
                self.set_sprite_from_pack("run-right", run_anim_speed)
                self.direction = "right"

            elif "left" in self.controls and keys[self.controls["left"]]:
                self.set_sprite_from_pack("run-left", run_anim_speed)
                self.direction = "left"
            else:
                idle_anim_speed = FramesClock // self.idle_animation_speed // self.walk_animation_speed % self.animation.get_len(
                    "idle-right")
                if self.direction == "right":
                    self.set_sprite_from_pack("idle-right", idle_anim_speed)
                else:
                    self.set_sprite_from_pack("idle-left", idle_anim_speed)

    def update(self, keys, platforms):
        """Moves player"""
        if keys[pygame.K_ESCAPE]:
            raise SystemExit("Escape")
        if not self.hitting:
            if "up" in self.controls and keys[self.controls["up"]]:
                if self.onGround:
                    self.yvel -= self.jump
            if "left" in self.controls and keys[self.controls["left"]]:
                self.xvel = -self.speed
            if "right" in self.controls and keys[self.controls["right"]]:
                self.xvel = self.speed
            if "reset" in self.controls and keys[self.controls["reset"]]:
                self.set_coords(self.start_coords)
            if not self.onGround:
                self.yvel += 0.5
                if self.yvel > 100:
                    self.yvel = 100
            if not (keys[self.controls["left"]] or keys[self.controls["right"]]):
                self.xvel = 0
            self.rect.left += self.xvel
            self.collide(self.xvel, 0, platforms)
            self.rect.top += self.yvel
            self.onGround = False
            self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        """Check platform collision"""
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print("collide right")

                    # Auto-jump
                    if self.onGround:
                        self.yvel -= 8
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print("collide left")

                    # Auto-jump
                    if self.onGround:
                        self.yvel -= 8

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

    def set_coords(self, coords, start=False):
        """Change player Position. If start - + set start coords"""
        if start:
            self.start_coords = coords
        self.rect = self.image.get_rect(topleft=(coords))

    def hit_collides(self, other):
        """Perfect Pixel Collision Checker"""
        offset_x, offset_y = (other.rect.left - self.rect.left), (other.rect.top - self.rect.top)
        if self.mask.overlap(other.mask, (offset_x, offset_y)) is not None and self.hitting:
            return True
        return False

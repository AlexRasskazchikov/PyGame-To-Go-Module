import os

import pygame
from pygame import transform


class AnimationPack:
    def __init__(self):
        self.pack = {}
        self.meta = {}

    def __str__(self):
        return "\n".join([f"({len(self.pack[key])}) '{key}': [{', '.join(self.meta[key])}]" for key in self.meta]) \
            if self.meta else f"There is no sets in this Pack"

    def add_animation_set(self, name, dir):
        """This function adds an animation frames set to Pack.
        Agruments: Name - new set name, Dir - sprites directory."""
        self.pack[name] = list(map(lambda x: pygame.image.load(dir + "/" + x), os.listdir(dir)))
        self.meta[name] = list(os.listdir(dir))

    def get_frame(self, name, id):
        """Get a frame by set's name and frame id
        Agruments: name - set name, id - frame id."""
        return self.pack[name][id]

    def get_set(self, name):
        """Get a frames set by it's name
        Agruments: name - set name"""
        return self.pack[name]

    def get_sets_names(self):
        """Get al sets names"""
        return self.pack.keys()

    def create_flipped_animation_set(self, name):
        """Create flipped set of animations."""
        anim_set = list(map(lambda x: transform.flip(x, True, False), self.pack[name]))
        if "right" in name:
            self.pack[name.replace("right", "left")] = anim_set
            self.meta[name.replace("right", "left")] = [f"Flipped {name}"]
        else:
            self.pack[f"{name}Flip"] = anim_set
            self.meta[f"{name}Flip"] = [f"Flipped {name}"]

    def __getitem__(self, item):
        return self.pack[item]

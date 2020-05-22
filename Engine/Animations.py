import os

import pygame
from pygame import transform


class AnimationPack:
    def __init__(self):
        self.pack = {}
        self.meta = {}

    def __str__(self):
        """Getting sets names, length and content."""
        return "\n".join([f"({len(self.pack[key])}) '{key}': [{', '.join(self.meta[key])}]" for key in self.meta]) \
            if self.meta else f"Can't find right animation set."

    def add_animation_set(self, name, directory):
        """This function adds an animation frames set to Pack.
        Arguments: Name - new set name, Dir - sprites directory.
        Currently supported sets: [hit{i}-right, run-right, idle-right]"""
        self.pack[name] = list(map(lambda x: pygame.image.load(directory + "/" + x), os.listdir(directory)))
        self.meta[name] = list(os.listdir(directory))

    def get_count(self, act):
        """Get a count of animation variations of one activity."""
        return len(list(filter(lambda x: act in x, list(self.meta.keys())))) // 2

    def get_frame(self, name, id):
        """Get a frame by set's name and frame id
        Arguments: name - set name, id - frame id."""
        if name not in self.pack:
            raise ValueError("Can't find right animation set.")
        if id > len(self.pack):
            raise ValueError("Кадр с данным индексом не найден.")
        return self.pack[name][id]

    def get_set(self, name):
        """Get a frames set by it's name
        Arguments: name - set name"""
        if name not in self.pack:
            raise ValueError("Can't find right animation set.")
        return self.pack[name]

    def get_sets_names(self):
        """Get sets names."""
        return list(self.pack.keys())

    def create_flipped_animation_set(self, name):
        """Create flipped set of animations."""
        if name not in self.pack:
            raise ValueError("Can't find right animation set.")

        # Flipping every frame.
        anim_set = list(map(lambda x: transform.flip(x, True, False), self.pack[name]))

        if "right" in name:
            self.pack[name.replace("right", "left")] = anim_set
            self.meta[name.replace("right", "left")] = [f"Flipped {name}"]
        else:
            self.pack[f"{name}Flip"] = anim_set
            self.meta[f"{name}Flip"] = [f"Flipped {name}"]

    def __getitem__(self, item):
        """Getting set by it's name."""
        if item not in self.pack:
            raise ValueError("Can't find right animation set.")
        return self.pack[item]

    def get_len(self, name):
        """Get the length of animation."""
        if name not in self.pack:
            raise ValueError("Can't find right animation set.")
        return len(self.pack[name])

import os
import pygame

from logger import l


def load_graphics(root_path, colorkey=(255, 0, 255)):
    images = {}
    for file in os.listdir(root_path):
        file_name, ext = os.path.splitext(file)
        img = pygame.image.load(os.path.join(root_path, file))
        if img.get_alpha():
            img = img.convert_alpha()
        else:
            img = img.convert()
            img.set_colorkey(colorkey)
        l.info(f"Loading image {file_name}")
        images[file_name] = img
    return images


def load_fonts(root_path):
    fonts = {}
    for file in os.listdir(root_path):

        file_name, ext = os.path.splitext(file)
        for size in (20, 30, 40):
            fontfile = pygame.font.Font(os.path.join(root_path, file), size)

            l.info(f"Loading font {file_name}_{str(size)}")
            fonts[F"{file_name}_{str(size)}"] = fontfile
    return fonts


class Image:
    images = load_graphics('assets/images')

    @classmethod
    def load(cls, filename: str):
        if filename in cls.images:
            return cls.images[filename]
        raise ValueError(f"Image {filename} not found")


class Font:
    fonts = load_fonts('assets/fonts')

    @classmethod
    def get_font(cls, font_name: str):
        if font_name in cls.fonts:
            return cls.fonts[font_name]
        raise ValueError(f"Font {font_name} not found")


class Content:
    Image = Image
    Font = Font




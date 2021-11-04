import pygame
from content import Content


def emit_event(event_type, *args, **kwargs):
    pygame.event.post(pygame.event.Event(event_type, *args, **kwargs))


def draw_text(
    text: str,
    font_name: str = "Inconsolata_30",
    bold: int = 0,
    color=pygame.Color("white"),
) -> pygame.surface.Surface:
    """
    Returns surface with rendered text
    :param text: text to render
    :param font_name: font name
    :param bold: bold value
    :param color: tuple representing (r, g, b)
    :return: pygame.surface.Surface
    """
    font = Content.Font.get_font(font_name)
    font.set_bold(bold)
    text_display = font.render(text, True, color)
    return text_display


def clamp(val, minval, maxval):
    """
    clamps val between minval and maxval inclusive
    :param val:
    :param minval:
    :param maxval:
    :return:
    """
    return max(minval, min(val, maxval))

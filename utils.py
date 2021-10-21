import pygame


def emit_event(event_type, *args, **kwargs):
    pygame.event.post(pygame.event.Event(event_type, *args, **kwargs))
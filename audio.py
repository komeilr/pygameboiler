import pygame


class Audio:
    def __init__(self):
        self.channel_0 = pygame.mixer.Channel(0)
        self.channel_1 = pygame.mixer.Channel(1)
        self.channel_2 = pygame.mixer.Channel(2)
        self.channel_3 = pygame.mixer.Channel(3)
        self.channel_4 = pygame.mixer.Channel(4)
        self.channel_5 = pygame.mixer.Channel(5)
        self.channel_6 = pygame.mixer.Channel(6)
        self.channel_7 = pygame.mixer.Channel(7)
        self.channels = [self.channel_0,
                         self.channel_1,
                         self.channel_2,
                         self.channel_3,
                         self.channel_4,
                         self.channel_5,
                         self.channel_6,
                         self.channel_7]

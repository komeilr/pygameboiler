from pygame.sprite import LayeredDirty
from interface import IProcessEvent


class LayeredDirtyEvent(LayeredDirty, IProcessEvent):
    def __init__(self, *args, **kwargs):
        LayeredDirty.__init__(self, *args, **kwargs)

    def process_event(self, event, *args, **kwargs):
        for sprite in self.sprites():
            sprite.process_event(event, *args, **kwargs)


layered_group = LayeredDirtyEvent()

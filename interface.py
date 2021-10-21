from abc import ABC, abstractmethod


class IEvent(ABC):
    @abstractmethod
    def handle_event(self, evt):
        pass

    @abstractmethod
    def on_event(self, evt_type, cb, *args):
        pass

    @abstractmethod
    def process_event(self, event):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

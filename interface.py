from abc import ABC, abstractmethod


class IEvent(ABC):
    @abstractmethod
    def handle_event(self, evt):
        pass

    @abstractmethod
    def on_event(self, evt_type, cb, *args):
        pass


class EventListener(IEvent):
    def __init__(self):
        self.listeners = {}

    def handle_event(self, event):
        for func, args in self.listeners[event.type]:
            func(event, *args)

    def on_event(self, event_type, cb, *args):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append((cb, args))


class IProcessEvent(ABC):
    @abstractmethod
    def process_event(self, event, *args, **kwargs):
        pass

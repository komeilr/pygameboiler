from interface import IEvent
from customevents import STATEDONE


class StateMachine(IEvent):
    def __init__(self):
        self.name = ''
        self.history = []
        self.states = {
            'IDLE': IdleState
        }

        self.active = self.states['IDLE']
        self.active.enter()
        self.listeners = {}

        self.on_event(STATEDONE, self.change_state)

    def change_state(self, state_name):
        if state_name == self.history[-1].name:
            self.active.exit()
            self.push_down()
        else:
            self.history.append(self.active)
            self.active.exit()
            self.active = self.states[self.active.next]
            self.active.enter()

    def push_down(self):
        self.active = self.history.pop()
        self.active.enter()

    def handle_event(self, event):
        super().handle_event(event)

    def on_event(self, event_type, cb, *args):
        super().on_event(event_type, cb, *args)

    def process_event(self, event):
        pass

    def update(self, dt):
        self.active.update(dt)

    def draw(self, screen):
        self.active.draw(screen)







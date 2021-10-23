from pygame.key import get_pressed
from pygame.mouse import get_pressed as gp
from pygame.locals import *

from constants import ACTIONS
from logger import l


def create_action_map(cls):
    actions = {}

    for action in cls.actions_list:
        actions[action] = False

    return actions


class Input:
    actions_list = ACTIONS

    key_action_map = {
        K_w: 'ui_up',
        K_UP: 'ui_up',
        K_s: 'ui_down',
        K_DOWN: 'ui_down',
        K_a: 'ui_left',
        K_LEFT: 'ui_left',
        K_d: 'ui_right',
        K_RIGHT: 'ui_right',
        K_RETURN: 'ui_accept',
        K_SPACE: 'ui_accept',
        K_BACKSPACE: 'ui_back',
    }

    mouse_action_map = {
        BUTTON_RIGHT: 'ui_back',
    }

    just_pressed = False
    action_map = None

    # #leftmousedown = False
    # middlemousedown = False
    # rightmousedown = False

    @classmethod
    def leftmousedown(cls):
        mouse = gp(num_buttons=3)
        return mouse[0]

    @classmethod
    def is_action_pressed(cls, action):
        return cls.action_map[action]

    @classmethod
    def is_action_just_pressed(cls, action):
        keys = []

        for key in cls.key_action_map:
            if cls.key_action_map[key] == action:
                keys.append(key)

        keys_pressed = get_pressed()

        if not cls.just_pressed and keys_pressed[keys[0]] or keys_pressed[keys[1]]:
            cls.just_pressed = True
            return True
        return False        

    @classmethod
    def update_keydown_actions(cls, event):
        if event.key in cls.key_action_map:
            action = cls.key_action_map[event.key]
            cls.action_map[action] = True
            # l.info(cls.action_map)  # debug

    @classmethod
    def update_keyup_actions(cls, event):
        pass

    @classmethod
    def update_mousedown_actions(cls, event):
        cls.update_mouse_button_state(event.button, True)

    @classmethod
    def update_mouseup_actions(cls, event):
        cls.update_mouse_button_state(event.button, False)

    @classmethod
    def reset_action_map(cls):
        for k in cls.action_map:
            cls.action_map[k] = False

    @classmethod
    def update_mouse_button_state(cls, button_type, val):
        pass


Input.action_map = create_action_map(Input)

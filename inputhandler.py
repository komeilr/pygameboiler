from pygame.key import get_pressed
from pygame.mouse import get_pressed as gp
from pygame.locals import *

from constants import ACTIONS
from logger import l


def create_action_map(cls) -> dict:
    """
    Creates and returns a dictionary with actions as keys and boolean values as parameters
    :param cls:
    :return:
    """
    actions = {}

    for action in cls.actions_list:
        actions[action] = False

    return actions


class Input:
    """
    Input class that keeps track of Keyboard and Mouse input
    """

    actions_list = ACTIONS

    # Dictionary that maps keyboard constants to actions
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
        K_TAB: 'ui_down'
    }

    # Dictionary that maps mouse constants to actions
    mouse_action_map = {
        BUTTON_RIGHT: 'ui_back',
    }

    just_pressed = False
    action_map = None

    @classmethod
    def leftmousedown(cls) -> bool:
        """
        Returns True if left mouse button is down
        :return: :bool
        """
        mouse = gp(num_buttons=3)
        return mouse[0]

    @classmethod
    def rightmousedown(cls) -> bool:
        """
        Returns True if right mouse button is down
        :return: :bool
        """
        mouse = gp(num_buttons=3)
        return mouse[2]

    @classmethod
    def middlemousedown(cls) -> bool:
        """
        Returns True if middle mouse is down
        :return: :bool
        """
        mouse = gp(num_buttons=3)
        return mouse[1]

    @classmethod
    def is_action_pressed(cls, action: str) -> bool:
        """
        Returns True if input representing action is held
        :param :str represents action
        :return: :bool
        """
        return cls.action_map[action]

    @classmethod
    def is_action_just_pressed(cls, action: str) -> bool:
        """
        Returns True if input representing action is pressed once.
        Will only return True once, even if action is held down
        :param action:
        :return: :bool
        """
        keys = []

        for key in cls.key_action_map:
            if cls.key_action_map[key] == action:
                keys.append(key)

        keys_pressed = get_pressed()

        if not cls.just_pressed and any([keys_pressed[key] for key in keys]):
            cls.just_pressed = True
            return True
        return False        

    @classmethod
    def update_keydown_actions(cls, event) -> None:
        """
        Updates action_map dictionary
        :param event:
        :return:
        """
        if event.key in cls.key_action_map:
            action = cls.key_action_map[event.key]
            cls.action_map[action] = True

    @classmethod
    def update_keyup_actions(cls, event) -> None:
        pass

    @classmethod
    def update_mousedown_actions(cls, event):
        cls.update_mouse_button_state(event.button, True)

    @classmethod
    def update_mouseup_actions(cls, event):
        cls.update_mouse_button_state(event.button, False)

    @classmethod
    def reset_action_map(cls) -> None:
        """
        Resets all actions in action_map to False
        :return:
        """
        for k in cls.action_map:
            cls.action_map[k] = False

    @classmethod
    def update_mouse_button_state(cls, button_type, val):
        pass


Input.action_map = create_action_map(Input)

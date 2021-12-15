import os
from configparser import ConfigParser
from ast import literal_eval


class ConfigSettings:
    def __init__(self):
        self.display = {
            'fullscreen': False,
            'vsync': False
        }

    def __str__(self):
        import pprint as pp
        pp.pprint(self.__dict__)


def check_settings_exists():
    return 'settings.ini' in os.listdir()


def load_settings(config_settings: ConfigSettings) -> ConfigSettings:
    config = ConfigParser()
    config.read('settings.ini')

    for section in config.sections():
        if not hasattr(config_settings, section):
            setattr(config_settings, section, {})
        for key in config[section]:
            getattr(config_settings, section)[key] = literal_eval(config[section][key])


def save_settings(config_settings: ConfigSettings) -> None:
    config = ConfigParser()

    for section in vars(config_settings):
        config[section] = {}
        for key, val in getattr(config_settings, section).items():
            config.set(section, key, str(val))

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)


def init_config_settings() -> ConfigSettings:
    configsettings = ConfigSettings()
    if check_settings_exists():
        load_settings(configsettings)
    else:
        save_settings(configsettings)

    return configsettings

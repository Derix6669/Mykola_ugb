from environs import Env

env = Env()
env.read_env()


class State:
    _default_values = {
        'ACTIVE_WINDOW_ID': {},
    }

    ACTIVE_WINDOW_ID = _default_values['ACTIVE_WINDOW_ID']
    CATEGORIES = [
        "Гуманітарна допомога",
        "Медицина",
        "Інше",
        "Піхота",
        "Радіо боротьба",
        "Їжа",
        "Транспорт",
        "Дрони та комплектуючі",
        "Електроніка"
    ]

    @classmethod
    def set_default(cls):
        for key, value in cls._default_values.items():
            setattr(cls, key, value)

    @classmethod
    def all_attr(cls):
        return {key: getattr(cls, key) for key in dir(cls)
                if not key.startswith('__') and not callable(getattr(cls, key)) and key not in {'LOGO', 'GIF'}}


class Config:
    DARK_THEME = True
    BASE_DIR = ''
    LOG_TO_CONSOLE = True
    Debug = True
    API_KEY = env.str('OPENAI_API_KEY')

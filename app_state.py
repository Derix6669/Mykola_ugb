from environs import Env

# Initialize environment configuration reader
env = Env()
env.read_env()


class State:
    """
    State class stores global application state and constants.

    Attributes:
        ACTIVE_WINDOW_ID (dict): Stores the active window ID of the application.
        CATEGORIES (list): A predefined list of categories used in the application.
        _default_values (dict): Dictionary of default state values to reset the state when needed.
    """

    _default_values = {
        'ACTIVE_WINDOW_ID': {},
    }

    ACTIVE_WINDOW_ID: dict = _default_values['ACTIVE_WINDOW_ID']
    CATEGORIES: list = [
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
    def set_default(cls) -> None:
        """
        Resets the state attributes to their default values.
        """
        for key, value in cls._default_values.items():
            setattr(cls, key, value)

    @classmethod
    def all_attr(cls) -> dict:
        """
        Retrieves all class attributes except for private and callable ones, excluding LOGO and GIF.

        Returns:
            dict: A dictionary of the current class attributes and their values.
        """
        return {
            key: getattr(cls, key) for key in dir(cls)
            if not key.startswith('__') and not callable(getattr(cls, key)) and key not in {'LOGO', 'GIF'}
        }


class Config:
    """
    Config class holds configuration variables for the application.

    Attributes:
        DARK_THEME (bool): Boolean flag to enable or disable dark theme.
        BASE_DIR (str): Base directory of the project.
        LOG_TO_CONSOLE (bool): Flag to enable or disable logging to console.
        Debug (bool): Flag to indicate whether the application is in debug mode.
        API_KEY (str): API key for the OpenAI service, loaded from environment variables.
    """

    DARK_THEME: bool = True
    BASE_DIR: str = ''
    LOG_TO_CONSOLE: bool = True
    Debug: bool = True
    API_KEY: str = env.str('OPENAI_API_KEY')  # Reads the OpenAI API key from the .env file

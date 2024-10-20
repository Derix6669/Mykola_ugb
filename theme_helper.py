from ctypes import wintypes, byref, HRESULT, c_int, c_void_p, c_uint, sizeof, WinDLL
from qfluentwidgets import setTheme, Theme
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QCoreApplication
from app_state import State, Config

def toggle_title_bar_theme_helper(windIds: dict, window: QWidget) -> None:
    """
    Toggles the title bar theme (light/dark mode) for windows based on the application's theme setting.

    Args:
        windIds (dict): A dictionary containing window IDs.
        window (QWidget): The window instance whose title bar theme needs to be toggled.
    """
    is_dark = Config.DARK_THEME
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20

    # Load the dwmapi library
    dwmapi = WinDLL("dwmapi")
    DwmSetWindowAttribute = dwmapi.DwmSetWindowAttribute

    # Set argument and return types for the DwmSetWindowAttribute function
    DwmSetWindowAttribute.argtypes = [wintypes.HWND, c_uint, c_void_p, c_uint]
    DwmSetWindowAttribute.restype = HRESULT

    # Determine the value for dark or light mode
    value = c_int(1 if is_dark else 0)

    # Apply the immersive dark mode setting to each window
    for windId in windIds.values():
        DwmSetWindowAttribute(
            windId, DWMWA_USE_IMMERSIVE_DARK_MODE, byref(value), sizeof(value)
        )

        # Resize the window to refresh the title bar appearance
        window.resize(window.width(), window.height() + 1)
        window.resize(window.width(), window.height() - 1)


def toggle_theme_helper(theme: Theme) -> None:
    """
    Toggles the application theme and updates the title bar theme for all top-level windows.

    Args:
        theme (Theme): The desired theme to set (light or dark).
    """
    setTheme(theme, False, True)

    # Retrieve the window ID from the application state
    win_id = State.ACTIVE_WINDOW_ID
    window = None

    # Get the QApplication instance
    app: QCoreApplication = QApplication.instance()

    # Find the top-level window with the object name 'WINDOW'
    if win_id:
        for child in app.topLevelWidgets():
            if child.objectName() == 'WINDOW':
                window = child
        if window:
            # Apply the title bar theme
            toggle_title_bar_theme_helper(win_id, window)
        else:
            print('No window found to apply the theme.')

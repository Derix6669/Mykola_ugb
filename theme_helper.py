from ctypes import wintypes
from qfluentwidgets import qconfig, Theme
import ctypes
from qfluentwidgets import setTheme, Theme
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QCoreApplication

from app_state import State, Config


def toggle_title_bar_theme_helper(windIds: dict, window):
    is_dark = Config.DARK_THEME
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20

    dwmapi = ctypes.WinDLL("dwmapi")
    DwmSetWindowAttribute = dwmapi.DwmSetWindowAttribute
    DwmSetWindowAttribute.argtypes = [
        wintypes.HWND,
        ctypes.c_uint,
        ctypes.c_void_p,
        ctypes.c_uint,
    ]
    DwmSetWindowAttribute.restype = ctypes.HRESULT

    value = ctypes.c_int(1 if is_dark else 0)
    for windId in windIds.values():
        DwmSetWindowAttribute(
            windId, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value)
        )

        window.resize(window.width(), window.height() + 1)
        window.resize(window.width(), window.height() - 1)


def toggle_theme_helper(theme: Theme) -> None:
    setTheme(theme, False, True)
    window = None
    win_id = State.ACTIVE_WINDOW_ID

    if win_id:
        app: QCoreApplication = QApplication.instance()

        for child in app.topLevelWidgets():
            if child.objectName() == 'WINDOW':
                window = child
        if window:
            toggle_title_bar_theme_helper(win_id, window)
        else:
            print('not window')

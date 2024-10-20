import os
from enum import Enum

from qfluentwidgets import StyleSheetBase, qconfig, Theme


class StyleSheet(StyleSheetBase, Enum):
    WINDOW = 'WINDOW'

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        theme = theme.value.lower()
        theme_path = os.path.join(os.path.dirname(__file__), "qss", f"{theme}.qss")
        return theme_path

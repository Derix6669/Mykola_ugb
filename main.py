import sys

from PyQt5.QtWidgets import QApplication

from AI.GUI import FundraisingApp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FundraisingApp()
    ex.show()
    sys.exit(app.exec_())

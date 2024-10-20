import sys
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QApplication, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QTextEdit
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont, LineEdit, PrimaryPushButton, \
    TitleLabel, BodyLabel, Theme, ScrollArea, TextEdit, PushButton
from qfluentwidgets import FluentIcon as FIF

from AI.app_state import State, Config
from AI.backend.client_worker import ClientWorker
from AI.logger import Logger
from AI.theme_helper import toggle_theme_helper
from style.style_sheet import StyleSheet


class Widget(QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)

        self.setObjectName("WINDOW")
        StyleSheet.WINDOW.apply(self)

        # Заголовок
        self.titleLabel = TitleLabel(title, self)
        setFont(self.titleLabel, 45)
        self.titleLabel.setStyleSheet("background-color: transparent;"
                                      "color: #FDFAF9;")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.textEdit = QTextEdit(self)
        self.textEdit.setStyleSheet("""
        border-radius: 10px;
        color: white;
        padding: 15px;
        font-size: 25px;
        background-color: #303845;
        border: 2px solid #B34F00; /* Зелена рамка */
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Легкий ефект тіні */
        """)
        setFont(self.textEdit, 25)
        self.textEdit.setMinimumSize(550, 300)
        self.textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Кнопка
        self.button = PushButton('Обробити')

        self.button.setFixedSize(350, 50)
        setFont(self.button, 35)
        self.button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        # Великий текстовий лейбл внизу
        self.bottomLabel = BodyLabel('Поки немає відповіді.', self)
        setFont(self.bottomLabel, 50)
        self.bottomLabel.setStyleSheet("background-color: #B83400;"
                                       "color: #FDFAF9;"
                                       "border-radius: 10px;"
                                       )
        self.bottomLabel.setAlignment(Qt.AlignCenter)
        self.bottomLabel.setWordWrap(True)  # Включаємо перенесення рядків
        self.bottomLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Підключення зміни тексту до функції автоматичного налаштування розміру
        self.updateBottomLabel("Поки немає відповіді.")
        # Основний лейаут
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.titleLabel, 1, Qt.AlignTop | Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.textEdit, 1, Qt.AlignTop | Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.button, 1, Qt.AlignTop | Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.bottomLabel, 7, Qt.AlignCenter)

        # Створюємо віджет-контейнер для прокручування
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.vBoxLayout)
        self.scrollWidget.setStyleSheet("""
            background-color: #222831;
        """)

        # Створюємо прокручувану область
        self.scrollArea = ScrollArea(self)
        self.scrollArea.setStyleSheet("""
            background-color: #4E781D;
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #5DBF68, stop:1 #37AD8B);
        """)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # Головний лейаут для відображення прокручуваної області
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.scrollArea)

        # Налаштовуємо об'єктне ім'я
        self.setObjectName(title.replace(' ', '-'))

    def updateBottomLabel(self, text):
        self.bottomLabel.setText(text)
        self.bottomLabel.adjustSize()  # Автоматично підлаштовує розмір під текст


class Window(FluentWindow):
    """ Main Interface """

    def __init__(self):
        super().__init__()
        self.setObjectName("WINDOW")
        StyleSheet.WINDOW.apply(self)
        State.ACTIVE_WINDOW_ID['MainWindow'] = int(self.winId())
        self.change_theme(self)
        self.setMinimumSize(850, 700)
        # Ініціалізація інтерфейсів
        self.homeInterface = self.create_home_interface()
        self.subtractContextInterface = self.create_subtract_interface()
        self.createTaskInterface = self.create_task_interface()
        self.searchPatternsInterface = self.create_searchPatternsInterface()
        self.homeInterface.button.clicked.connect(lambda: self.category_definition(self.homeInterface))
        self.subtractContextInterface.button.clicked.connect(
            lambda: self.finding_common_context(self.subtractContextInterface))
        self.createTaskInterface.button.clicked.connect(lambda: self.creating_new_tasks(self.createTaskInterface))
        self.searchPatternsInterface.button.clicked.connect(
            lambda: self.search_behavioral_pattern(self.searchPatternsInterface))

        self.initNavigation()
        self.initWindow()

        self.thread = None

    def create_home_interface(self) -> Widget:
        """Створюємо інтерфейс для Home сторінки"""
        return Widget('Визначення категорії', self)

    def create_subtract_interface(self) -> Widget:
        """Створюємо інтерфейс для Subtract Context сторінки"""
        return Widget('Знаходження спільного контексту', self)

    def create_task_interface(self) -> Widget:
        """Створюємо інтерфейс для Create Task сторінки"""
        return Widget('Створення нових завдань', self)

    def create_searchPatternsInterface(self) -> Widget:
        return Widget('Визначення поведінкових патернів', self)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.TAG, 'Визначення категорії')
        self.addSubInterface(self.subtractContextInterface, FIF.SEARCH, 'Знаходження спільного контексту')
        self.addSubInterface(self.createTaskInterface, FIF.ADD, 'Створення нових завдань')
        self.addSubInterface(self.searchPatternsInterface, FIF.HEART, 'Знаходження поведінкових патернів')
        self.navigationInterface.addSeparator()

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('./static/logo.png'))
        self.setWindowTitle('Eco UBG')

    @staticmethod
    def change_theme(self):
        if Config.DARK_THEME:
            QFrame.setStyleSheet(self, 'background: #2c2c2c;')

        else:
            QFrame.setStyleSheet(self, 'background: #fbfbfb;')

        theme = Theme.DARK if Config.DARK_THEME == 1 else Theme.LIGHT
        toggle_theme_helper(theme)

    def cleanup(self, thread):
        # Очищення сигналів і потоку
        thread.update_signal.disconnect(self.update_label)
        thread.finished_signal.disconnect(self.cleanup)
        thread.deleteLater()
        self.thread = None  # Очищуємо змінну, щоб знищити об'єкт

    def update_label(self, text, interface):
        interface.bottomLabel.setText(text)

    def search_behavioral_pattern(self, *args):
        interface = args[0]
        self.thread = ClientWorker()
        self.thread.set_parameters(task_name='search_behavioral_pattern', text=interface.textEdit.toPlainText(),
                                   interface=interface)
        self.thread.update_signal.connect(self.update_label)
        self.thread.finished_signal.connect(self.cleanup)
        self.thread.start()

    def category_definition(self, *args):
        interface = args[0]
        self.thread = ClientWorker()
        self.thread.set_parameters(task_name='category_definition', text=interface.textEdit.toPlainText(),
                                   interface=interface)
        self.thread.update_signal.connect(self.update_label)
        self.thread.finished_signal.connect(self.cleanup)
        self.thread.start()

    def finding_common_context(self, *args):
        interface = args[0]
        self.thread = ClientWorker()
        self.thread.set_parameters(task_name='finding_common_context', text=interface.textEdit.toPlainText(),
                                   interface=interface)
        self.thread.update_signal.connect(self.update_label)
        self.thread.finished_signal.connect(self.cleanup)
        self.thread.start()

    def creating_new_tasks(self, *args):
        interface = args[0]
        self.thread = ClientWorker()
        self.thread.set_parameters(task_name='creating_new_tasks', text=interface.textEdit.toPlainText(),
                                   interface=interface)
        self.thread.update_signal.connect(self.update_label)
        self.thread.finished_signal.connect(self.cleanup)
        self.thread.start()
        # interfase.bottomLabel.setText('Завдання\n'
        #                               '1. Задонать після сніданку\n'
        #                               '2. Задонать на ранковій пробіжці\n'
        #                               '3. Задонать перед роботаю\n')


def excepthook(exc_type, exc_value, exc_tb):
    formatted_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    Logger.log(message=f'!!!!EXCEPTION!!!!\nexc_type: {exc_type}\nexc_value: {exc_value}\nexc_tb: '
                       f'{formatted_traceback}\n', level=Logger.critical_log_level)

    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    msg_box = QMessageBox()
    msg_box.setText("An error occurred")
    msg_box.setInformativeText(error_msg)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.exec_()


sys.excepthook = excepthook

if __name__ == '__main__':
    Logger.log(message='\n' * 5 + '!!' + '\t' * 5 + '!!STARTING APP!!' + '\t' * 5 + '!!' + '\n' * 5,
               level=Logger.info_log_level)

    app = QApplication(sys.argv)

    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    w = Window()
    w.show()
    sys.exit(app.exec_())

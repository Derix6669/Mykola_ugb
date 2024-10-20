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
    """
    Custom widget class that represents a section of the main interface.

    Attributes:
        titleLabel (TitleLabel): The title label at the top of the widget.
        textEdit (QTextEdit): The text edit field for inputting data.
        button (PushButton): The button that triggers an action.
        bottomLabel (BodyLabel): A large label at the bottom displaying status or results.
        scrollWidget (QWidget): A widget container for the scroll area.
        scrollArea (ScrollArea): A scrollable area for the main content.
        vBoxLayout (QVBoxLayout): Main vertical layout for arranging elements.
    """

    def __init__(self, title: str, parent=None):
        """
        Initializes the custom widget with a title and creates the layout.

        Args:
            title (str): Title to be displayed at the top.
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent=parent)

        self.setObjectName("WINDOW")
        StyleSheet.WINDOW.apply(self)

        # Title Label
        self.titleLabel = TitleLabel(title, self)
        setFont(self.titleLabel, 45)
        self.titleLabel.setStyleSheet("background-color: transparent; color: #FDFAF9;")
        self.titleLabel.setAlignment(Qt.AlignCenter)

        # Text Edit
        self.textEdit = QTextEdit(self)
        self.textEdit.setStyleSheet("""
            border-radius: 10px;
            color: white;
            padding: 15px;
            font-size: 25px;
            background-color: #303845;
            border: 2px solid #B34F00;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        """)
        setFont(self.textEdit, 25)
        self.textEdit.setMinimumSize(550, 300)
        self.textEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Button
        self.button = PushButton('Process')
        self.button.setFixedSize(350, 50)
        setFont(self.button, 35)
        self.button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        # Bottom Label
        self.bottomLabel = BodyLabel('No response yet.', self)
        setFont(self.bottomLabel, 50)
        self.bottomLabel.setStyleSheet("background-color: #B83400; color: #FDFAF9; border-radius: 10px;")
        self.bottomLabel.setAlignment(Qt.AlignCenter)
        self.bottomLabel.setWordWrap(True)
        self.bottomLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Connect the text update function to adjust the label size
        self.updateBottomLabel("No response yet.")

        # Main Layout
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.titleLabel, 1, Qt.AlignTop | Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.textEdit, 1, Qt.AlignTop | Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.button, 1, Qt.AlignTop | Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.bottomLabel, 7, Qt.AlignCenter)

        # Scrollable widget
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.vBoxLayout)
        self.scrollWidget.setStyleSheet("background-color: #222831;")

        # Scroll Area
        self.scrollArea = ScrollArea(self)
        self.scrollArea.setStyleSheet("""
            background-color: #4E781D;
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #5DBF68, stop:1 #37AD8B);
        """)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        # Main Layout for Scroll Area
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.scrollArea)

        # Set object name for styling
        self.setObjectName(title.replace(' ', '-'))

    def updateBottomLabel(self, text: str) -> None:
        """
        Updates the bottom label text and adjusts its size.

        Args:
            text (str): The text to set in the bottom label.
        """
        self.bottomLabel.setText(text)
        self.bottomLabel.adjustSize()


class Window(FluentWindow):
    """
    Main application window class that manages multiple interfaces for different tasks.

    Attributes:
        homeInterface (Widget): Interface for category definition.
        subtractContextInterface (Widget): Interface for finding common context.
        createTaskInterface (Widget): Interface for creating tasks.
        searchPatternsInterface (Widget): Interface for searching behavioral patterns.
        thread (ClientWorker): Background thread for performing tasks.
    """

    def __init__(self):
        """
        Initializes the main window, sets up the interface, and configures event handlers.
        """
        super().__init__()
        self.setObjectName("WINDOW")
        StyleSheet.WINDOW.apply(self)
        State.ACTIVE_WINDOW_ID['MainWindow'] = int(self.winId())
        self.change_theme(self)
        self.setMinimumSize(850, 700)

        # Initialize different interfaces
        self.homeInterface = self.create_home_interface()
        self.subtractContextInterface = self.create_subtract_interface()
        self.createTaskInterface = self.create_task_interface()
        self.searchPatternsInterface = self.create_searchPatternsInterface()

        # Connect buttons to their respective actions
        self.homeInterface.button.clicked.connect(lambda: self.category_definition(self.homeInterface))
        self.subtractContextInterface.button.clicked.connect(lambda: self.finding_common_context(self.subtractContextInterface))
        self.createTaskInterface.button.clicked.connect(lambda: self.creating_new_tasks(self.createTaskInterface))
        self.searchPatternsInterface.button.clicked.connect(lambda: self.search_behavioral_pattern(self.searchPatternsInterface))

        # Initialize navigation and window settings
        self.initNavigation()
        self.initWindow()

        self.thread = None  # Thread for executing tasks

    def create_home_interface(self) -> Widget:
        """ Creates the home interface for category definition. """
        return Widget('Category Definition', self)

    def create_subtract_interface(self) -> Widget:
        """ Creates the interface for finding common context. """
        return Widget('Finding Common Context', self)

    def create_task_interface(self) -> Widget:
        """ Creates the interface for creating tasks. """
        return Widget('Creating New Tasks', self)

    def create_searchPatternsInterface(self) -> Widget:
        """ Creates the interface for searching behavioral patterns. """
        return Widget('Searching Behavioral Patterns', self)

    def initNavigation(self) -> None:
        """ Initializes the navigation menu with links to the different interfaces. """
        self.addSubInterface(self.homeInterface, FIF.TAG, 'Category Definition')
        self.addSubInterface(self.subtractContextInterface, FIF.SEARCH, 'Finding Common Context')
        self.addSubInterface(self.createTaskInterface, FIF.ADD, 'Creating New Tasks')
        self.addSubInterface(self.searchPatternsInterface, FIF.HEART, 'Searching Behavioral Patterns')
        self.navigationInterface.addSeparator()

    def initWindow(self) -> None:
        """ Configures the window size, icon, and title. """
        self.resize(900, 700)
        self.setWindowIcon(QIcon('./static/logo.png'))
        self.setWindowTitle('Eco UBG')

    @staticmethod
    def change_theme(self) -> None:
        """
        Changes the theme of the window based on the configuration.

        Args:
            self (QFrame): The window frame instance.
        """
        if Config.DARK_THEME:
            QFrame.setStyleSheet(self, 'background: #2c2c2c;')
        else:
            QFrame.setStyleSheet(self, 'background: #fbfbfb;')

        theme = Theme.DARK if Config.DARK_THEME == 1 else Theme.LIGHT
        toggle_theme_helper(theme)

    def cleanup(self, thread: ClientWorker) -> None:
        """
        Cleans up the thread by disconnecting signals and deleting the thread instance.

        Args:
            thread (ClientWorker): The thread to clean up.
        """
        thread.update_signal.disconnect(self.update_label)
        thread.finished_signal.disconnect(self.cleanup)
        thread.deleteLater()
        self.thread = None  # Clear thread object to allow garbage collection

    def update_label(self, text: str, interface: Widget) -> None:
        """
        Updates the text in the bottom label of a given interface.

        Args:
            text (str): The text to update the label with.
            interface (Widget): The interface whose label needs updating.
        """
        interface.bottomLabel.setText(text)

    def search_behavioral_pattern(self, *args) -> None:
        """
        Starts a background thread for searching behavioral patterns.

        Args:
            *args: Arguments passed from the button click.
        """
        interface = args[0]
        self.thread = ClientWorker()
        self.thread.set_parameters(task_name='search_behavioral_pattern', text=interface.textEdit.toPlainText(),
                                   interface=interface)
        self.thread.update_signal.connect(self.update_label)
        self.thread.finished_signal.connect(self.cleanup)
        self.thread.start()

    def category_definition(self, *args) -> None:
        """
        Starts a background thread for category definition.

        Args:
            *args: Arguments passed from the button click.
        """
        interface = args[0]
        self.thread = ClientWorker()
        self.thread.set_parameters(task_name='category_definition', text=interface.textEdit.toPlainText(),
                                   interface=interface)
        self.thread.update_signal.connect(self.update_label)
        self.thread.finished_signal.connect(self.cleanup)
        self.thread.start()

    def finding_common_context(self, *args) -> None:
        """
        Starts a background thread for finding common context.

        Args:
            *args: Arguments passed from the button click.
        """
        interface = args[0]
        self.thread = ClientWorker()
        self.thread.set_parameters(task_name='finding_common_context', text=interface.textEdit.toPlainText(),
                                   interface=interface)
        self.thread.update_signal.connect(self.update_label)
        self.thread.finished_signal.connect(self.cleanup)
        self.thread.start()

    def creating_new_tasks(self, *args) -> None:
        """
        Starts a background thread for creating new tasks.

        Args:
            *args: Arguments passed from the button click.
        """
        interface = args[0]
        self.thread = ClientWorker()
        self.thread.set_parameters(task_name='creating_new_tasks', text=interface.textEdit.toPlainText(),
                                   interface=interface)
        self.thread.update_signal.connect(self.update_label)
        self.thread.finished_signal.connect(self.cleanup)
        self.thread.start()


def excepthook(exc_type, exc_value, exc_tb) -> None:
    """
    Global exception handler that logs errors and displays a message box.

    Args:
        exc_type (type): The exception type.
        exc_value (BaseException): The exception instance.
        exc_tb (traceback): The traceback object.
    """
    formatted_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    Logger.log(message=f'!!!!EXCEPTION!!!!\nexc_type: {exc_type}\nexc_value: {exc_value}\nexc_tb: {formatted_traceback}\n',
               level=Logger.critical_log_level)

    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    msg_box = QMessageBox()
    msg_box.setText("An error occurred")
    msg_box.setInformativeText(error_msg)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.exec_()


# Set custom exception hook
sys.excepthook = excepthook

if __name__ == '__main__':
    # Start application logging
    Logger.log(message='\n' * 5 + '!!' + '\t' * 5 + '!!STARTING APP!!' + '\t' * 5 + '!!' + '\n' * 5,
               level=Logger.info_log_level)

    app = QApplication(sys.argv)

    # Enable high DPI scaling and pixmaps
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Create and display main window
    w = Window()
    w.show()
    sys.exit(app.exec_())

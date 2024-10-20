from typing import Any
from PyQt5.QtCore import QThread, pyqtSignal
from AI.backend.client_chat import client


class ClientWorker(QThread):
    """
    A worker thread for handling tasks asynchronously. It processes tasks like
    category definition, finding common context, creating new tasks, and searching for behavioral patterns.

    Signals:
        update_signal (str, object): Emitted when the task is completed, passing the response and the interface.
        finished_signal (object): Emitted when the task finishes, passing the thread instance itself.
    """

    update_signal = pyqtSignal(str, object)
    finished_signal = pyqtSignal(object)

    def __init__(self):
        """
        Initializes the ClientWorker instance with default parameters set to None.
        """
        super().__init__()
        self.__task_name: str | None = None
        self.__text: str | None = None
        self.__interface: Any = None

    def set_parameters(self, task_name: str, text: str, interface: Any) -> None:
        """
        Sets the parameters for the task that will be processed.

        Args:
            task_name (str): The name of the task (e.g., 'category_definition', 'finding_common_context').
            text (str): The text to process for the given task.
            interface (Any): The interface where the results will be displayed or updated.
        """
        self.__task_name = task_name
        self.__text = text
        self.__interface = interface

    def run(self) -> None:
        """
        Runs the task by sending a request to the client and processing the response.
        Emits the update_signal with the response and interface once completed.
        Resets the task parameters after execution.
        """
        # Make the client request based on task_name and text
        response = client(self.__task_name, self.__text)

        # Reset the task parameters to prevent reuse
        self.__task_name, self.__text = None, None

        # Emit the response and associated interface
        self.update_signal.emit(f'{response}', self.__interface)

        # Signal that the task is finished
        self.finished_signal.emit(self)

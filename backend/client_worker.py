from typing import Any

from PyQt5.QtCore import QThread, pyqtSignal

from AI.backend.client_chat import client


class ClientWorker(QThread):
    update_signal = pyqtSignal(str, object)
    finished_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.__task_name = None
        self.__text = None
        self.__interface = None

    def set_parameters(self, task_name: str, text: str, interface):
        """:param task_name: category_definition, finding_common_context, creating_new_tasks, search_behavioral_pattern
        :param text: text of the task"""
        self.__task_name = task_name
        self.__text = text
        self.__interface = interface

    def run(self):
        response = client(self.__task_name, self.__text)
        self.__task_name, self.__text = None, None
        self.update_signal.emit(f'{response}', self.__interface)
        self.finished_signal.emit(self)

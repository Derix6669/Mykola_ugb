import os
import sys

import psutil
from loguru import logger
import inspect
from app_state import Config


def get_root_drives():
    list_disk = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if 'fixed' in partition.opts:
            list_disk.append(partition.device)
    if 'C:\\' in list_disk:
        Config.BASE_DIR = 'C:\\'
    else:
        Config.BASE_DIR = list_disk[0]


get_root_drives()


class Logger:
    _configured = False
    filename = 'program_log'
    folder_path = f'{Config.BASE_DIR}/SilvusConfiguratorData/log'
    log_to_console = Config.LOG_TO_CONSOLE

    # log levels
    info_log_level = 'info'
    warning_log_level = 'warning'
    error_log_level = 'error'
    debug_log_level = 'debug'
    critical_log_level = 'critical'

    @classmethod
    def configure(cls):
        if cls._configured:
            return

        if not os.path.exists(cls.folder_path):
            os.makedirs(cls.folder_path)

        logger.remove()
        console_format = "<green>{time}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan> | <magenta>{extra[file]}</magenta>:<magenta>{extra[line]}</magenta>"
        file_format = "{time} | {level} | {message} | {extra[file]}:{extra[line]}"

        logger.add(f"{cls.folder_path}/{cls.filename}.log", format=file_format, level="DEBUG", rotation="10 MB",
                   retention="10 days")
        if cls.log_to_console:
            logger.add(sys.stdout, format=console_format, level="DEBUG")

        cls._configured = True

    @classmethod
    def log(cls, message, level='debug'):
        cls.configure()
        frame = inspect.currentframe().f_back.f_back
        file_path = line_number = None
        while frame:
            if os.path.basename(frame.f_code.co_filename) != 'logger.py':
                file_path = os.path.basename(frame.f_code.co_filename)
                line_number = frame.f_lineno
                break
            frame = frame.f_back

        log_method = {
            'info': logger.bind(file=file_path, line=line_number).info,
            'warning': logger.bind(file=file_path, line=line_number).warning,
            'error': logger.bind(file=file_path, line=line_number).error,
            'debug': logger.bind(file=file_path, line=line_number).debug,
            'critical': logger.bind(file=file_path, line=line_number).critical
        }.get(level, logger.bind(file=file_path, line=line_number).info)

        log_method(message)

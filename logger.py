import os
import sys
import psutil
from loguru import logger
import inspect
from app_state import Config


def get_root_drives() -> None:
    """
    Identifies the system's root drives and sets the `BASE_DIR` in the configuration.
    If the 'C:\\' drive is present, it is used; otherwise, the first available fixed drive is chosen.
    """
    list_disk = []
    partitions = psutil.disk_partitions()

    # Find all fixed drives
    for partition in partitions:
        if 'fixed' in partition.opts:
            list_disk.append(partition.device)

    # Set BASE_DIR to 'C:\\' if present, otherwise use the first fixed drive
    if 'C:\\' in list_disk:
        Config.BASE_DIR = 'C:\\'
    else:
        Config.BASE_DIR = list_disk[0]


# Execute the drive detection at the start
get_root_drives()


class Logger:
    """
    Logger class to manage application logging using loguru.
    Logs messages to both console and files with appropriate levels and formats.

    Attributes:
        _configured (bool): Indicates whether logging has been configured.
        filename (str): The base name of the log file.
        folder_path (str): The folder where log files will be saved.
        log_to_console (bool): Flag indicating whether logs should be output to the console.
        info_log_level (str): Log level for informational messages.
        warning_log_level (str): Log level for warnings.
        error_log_level (str): Log level for errors.
        debug_log_level (str): Log level for debug messages.
        critical_log_level (str): Log level for critical errors.
    """

    _configured: bool = False
    filename: str = 'program_log'
    folder_path: str = f'{Config.BASE_DIR}/SilvusConfiguratorData/log'
    log_to_console: bool = Config.LOG_TO_CONSOLE

    # Log levels
    info_log_level: str = 'info'
    warning_log_level: str = 'warning'
    error_log_level: str = 'error'
    debug_log_level: str = 'debug'
    critical_log_level: str = 'critical'

    @classmethod
    def configure(cls) -> None:
        """
        Configures the logger by setting up logging to both file and console.
        Creates the necessary directory if it does not exist, and applies formatting and rotation settings.
        """
        if cls._configured:
            return

        # Ensure the log folder exists
        if not os.path.exists(cls.folder_path):
            os.makedirs(cls.folder_path)

        # Remove default loguru configuration and set up custom formats
        logger.remove()

        # Log formats for console and file
        console_format = "<green>{time}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan> | <magenta>{extra[file]}</magenta>:<magenta>{extra[line]}</magenta>"
        file_format = "{time} | {level} | {message} | {extra[file]}:{extra[line]}"

        # Add file logging with rotation and retention
        logger.add(f"{cls.folder_path}/{cls.filename}.log", format=file_format, level="DEBUG", rotation="10 MB",
                   retention="10 days")

        # Optionally log to console
        if cls.log_to_console:
            logger.add(sys.stdout, format=console_format, level="DEBUG")

        cls._configured = True

    @classmethod
    def log(cls, message: str, level: str = 'debug') -> None:
        """
        Logs a message with the specified log level, including file and line number metadata.

        Args:
            message (str): The message to log.
            level (str): The log level to use ('info', 'warning', 'error', 'debug', 'critical').
        """
        cls.configure()

        # Capture the caller's file and line number
        frame = inspect.currentframe().f_back.f_back
        file_path = line_number = None
        while frame:
            if os.path.basename(frame.f_code.co_filename) != 'logger.py':
                file_path = os.path.basename(frame.f_code.co_filename)
                line_number = frame.f_lineno
                break
            frame = frame.f_back

        # Select the appropriate log method based on the log level
        log_method = {
            'info': logger.bind(file=file_path, line=line_number).info,
            'warning': logger.bind(file=file_path, line=line_number).warning,
            'error': logger.bind(file=file_path, line=line_number).error,
            'debug': logger.bind(file=file_path, line=line_number).debug,
            'critical': logger.bind(file=file_path, line=line_number).critical
        }.get(level, logger.bind(file=file_path, line=line_number).info)

        # Log the message using the selected log method
        log_method(message)

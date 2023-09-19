"""
Module: init_logging.py

This module provides utilities for configuring and initializing logging in an application.

Functions:
- init_logging(log_filename: str = "log/log.txt") -> None: Initialize logging configuration for the application.

"""
import datetime
import os
import logging
from typing import Optional, Callable
import inspect
from contextlib import contextmanager
import threading

class CustomLogger(logging.Logger):
    """
    A custom logger that supports inserting process ID and function name into log messages.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the CustomLogger.

        Args:
            *args: Variable length arguments to be passed to the base class logger.
            **kwargs: Arbitrary keyword arguments to be passed to the base class logger.
        """
        super().__init__(*args, **kwargs)
        self.thread_local = threading.local()
    def debug(self, msg, *args, **kwargs):
        """
        Log a debug-level message.

        Args:
            msg (str): The log message to be recorded.
            *args: Variable length arguments to be passed to the log message.
            **kwargs: Arbitrary keyword arguments to be passed to the log message.
        """
        custom_msg = self.get_custome_msg(msg)
        super().debug(custom_msg, *args, **kwargs)
    def info(self, msg, *args, **kwargs):
        """
        Log an info-level message.

        Args:
            msg (str): The log message to be recorded.
            *args: Variable length arguments to be passed to the log message.
            **kwargs: Arbitrary keyword arguments to be passed to the log message.
        """
        custom_msg = self.get_custome_msg(msg)
        super().info(custom_msg, *args, **kwargs)
    def warning(self, msg, *args, **kwargs):
        """
        Log a warning-level message.

        Args:
            msg (str): The log message to be recorded.
            *args: Variable length arguments to be passed to the log message.
            **kwargs: Arbitrary keyword arguments to be passed to the log message.
        """
        custom_msg = self.get_custome_msg(msg)
        super().warning(custom_msg, *args, **kwargs)
    def error(self, msg, *args, **kwargs):
        """
        Log an error-level message.

        Args:
            msg (str): The log message to be recorded.
            *args: Variable length arguments to be passed to the log message.
            **kwargs: Arbitrary keyword arguments to be passed to the log message.
        """
        custom_msg = self.get_custome_msg(msg)
        super().error(custom_msg, *args, **kwargs)
    def critical(self, msg, *args, **kwargs):
        """
        Log a critical-level message.

        Args:
            msg (str): The log message to be recorded.
            *args: Variable length arguments to be passed to the log message.
            **kwargs: Arbitrary keyword arguments to be passed to the log message.
        """
        custom_msg = self.get_custome_msg(msg)
        super().critical(custom_msg, *args, **kwargs)
    def get_custome_msg(self, msg):
        """
        Get the custom log message with process ID and function name.

        Args:
            msg (str): The original log message.

        Returns:
            str: The custom log message with process ID and function name, if available.
        """
        frame = inspect.currentframe().f_back.f_back
        func_name = frame.f_code.co_name
        proc_id = getattr(self.thread_local, 'proc_id', None)
        print_func_name = getattr(self.thread_local, 'print_func_name', None)


        custom_msg = msg
        if print_func_name:
            custom_msg = f'{func_name} - {custom_msg}'
        if proc_id:
            custom_msg = f'{proc_id} - {custom_msg}'
        return custom_msg


    @contextmanager
    def insert_func_name(self):
        """
        Context manager to enable printing the function name in log messages within the block.

        Usage:
            with logger.insert_func_name():
                logger.info('This message will include the function name.')

        Note:
            Log messages outside the block will not include the function name.
        """
        setattr(self.thread_local, 'print_func_name', True)
        try:
            yield
        finally:
            setattr(self.thread_local, 'print_func_name', None)

    @contextmanager
    def insert_proc_id(self, proc_id: str):
        """
        Context manager to insert a process ID into log messages within the block.

        Args:
            proc_id (str): The process ID to be included in log messages.

        Usage:
            with logger.insert_proc_id('123'):
                logger.info('This message will include the process ID.')

        Note:
            Log messages outside the block will not include the process ID.
        """
        setattr(self.thread_local, 'proc_id', proc_id)
        try:
            yield
        finally:
            setattr(self.thread_local, 'proc_id', None)

def get_custome_logger(logger_name = 'main_log'):
    """
    Retrieve an existing logger or create a new CustomLogger instance with the specified name.

    Args:
        logger_name (str): The name of the logger. Defaults to 'main_log'.

    Returns:
        CustomLogger: The existing logger or a new CustomLogger instance.

    """
    # Check if the logger with the specified name already exists
    if logger_name in logging.Logger.manager.loggerDict:
        return logging.getLogger(logger_name)
    logger = CustomLogger(logger_name)
    logging.Logger.manager.loggerDict[logger_name] = logger
    return logger
class UILogHandler(logging.Handler):
    """
    Custom logging handler that emits log records by calling a specified log function.
    """
    def __init__(self, log_func):
        """
        Initialize the UILogHandler.

        Args:
            log_func (callable): The log function to be called for emitting log records.
        """
        super().__init__()
        self.log_func = log_func

    def emit(self, record):
        """
        Emit a log record by calling the specified log function.

        Args:
            record (logging.LogRecord): The log record to be emitted.
        """
        msg = self.format(record)
        self.log_func(msg)

def init_logging(
    log_name_postfix: str,
    log_level: int,
    log_dir: str = "log",
    ui_log_func: Optional[Callable] = None,
    print_in_con: bool = False,
) -> None:
    """
    Initialize logging configuration for the application.

    This function configures the logging module to save log messages in separate files for each month.
    The log level is set to INFO, and the log message format includes the date, log level, and the actual message.
    The date format is specified as day.month.year.

    Args:
        log_name_postfix (str): The postfix to append to the log file name.
        log_level (int): The log level to set for the handlers.
        log_dir (str, optional): The directory to store the log files. Defaults to "log".
        ui_log_func (callable, optional): A custom function for logging to the UI. Defaults to None.
        print_in_con (bool, optional): Flag to enable printing log messages to the console. Defaults to False.

    Returns:
        None

    """
    os.makedirs(log_dir, exist_ok=True)

    # Get the current month and year
    current_month = datetime.datetime.now().strftime("%m")
    current_year = datetime.datetime.now().strftime("%Y")

    # Create the log file name using the current month and year
    log_file_name = f"{current_month}.{current_year}.{log_name_postfix}"
    
    # Create the full path to the log file
    log_file_path = os.path.join(log_dir, log_file_name)



    # Configure the logging module
    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
    


    file_handler = logging.FileHandler(log_file_path, mode="a")
    #file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)
    file_handler.setLevel(log_level)
    


    # Get the root logger and add the handlers
    #logger = logging.getLogger()
    logger = get_custome_logger()
    # Each handlers could have own log level, because this func
    # could be called multiple times
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    

    # Create a console handler
    if print_in_con:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)
    # A file handler for saving logs to the file
    if ui_log_func:
        ui_handler = UILogHandler(ui_log_func)
        ui_handler.setFormatter(log_formatter)
        ui_handler.setLevel(log_level)
        logger.addHandler(ui_handler)
    return logger

def main():
    """
    Example usage:
    """
    proc_id = "12345"
    log = init_logging('log.txt', logging.INFO, print_in_con = True)
    log.info("some info")
    log.error("some error")
    log.debug("some debug")
    log.critical("some critical")
    with log.insert_proc_id(proc_id):
        log.info("here should be proc id")
        with log.insert_func_name():
            log.info("here also should be proc id and a func name")
            with log.insert_func_name():
                log.info("here also should be proc id and a func name")
    with log.insert_func_name():
        log.info("here should be only a func name")
        with log.insert_proc_id(proc_id):
            log.info("here also should be proc id and a func name")
    log.info("some info")
if __name__ == '__main__':
    main()

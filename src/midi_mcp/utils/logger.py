# -*- coding: utf-8 -*-
"""
Logging utilities for MIDI MCP Server.

Provides standardized logging configuration with appropriate formatters,
handlers, and log levels for the MIDI MCP server.
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#

import logging
import sys
from typing import Optional
from pathlib import Path


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
    logger_name: Optional[str] = None,
) -> logging.Logger:
    """
    Set up logging configuration for the MIDI MCP Server.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file. If None, logs to console only.
        log_format: Optional custom log format string
        logger_name: Optional logger name. If None, uses root logger.

    Returns:
        Configured logger instance
    """
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Get or create logger
    logger = logging.getLogger(logger_name or "midi_mcp")

    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()

    # Set log level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(numeric_level)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        try:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(numeric_level)
            logger.addHandler(file_handler)

            logger.info(f"Logging to file: {log_file}")
        except Exception as e:
            logger.warning(f"Could not set up file logging to {log_file}: {e}")

    # Prevent propagation to root logger to avoid duplicate messages
    logger.propagate = False

    logger.info(f"Logging initialized at {level} level")

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggerMixin:
    """
    Mixin class that provides a logger property to any class.

    The logger name will be based on the class name and module.
    """

    @property
    def logger(self) -> logging.Logger:
        """Get logger instance for this class."""
        return logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")


def log_exceptions(logger: Optional[logging.Logger] = None):
    """
    Decorator to log exceptions raised by functions.

    Args:
        logger: Optional logger instance. If None, uses function's module logger.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.exception(f"Exception in {func.__name__}: {e}")
                else:
                    module_logger = logging.getLogger(func.__module__)
                    module_logger.exception(f"Exception in {func.__name__}: {e}")
                raise

        return wrapper

    return decorator


def log_async_exceptions(logger: Optional[logging.Logger] = None):
    """
    Decorator to log exceptions raised by async functions.

    Args:
        logger: Optional logger instance. If None, uses function's module logger.
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.exception(f"Exception in {func.__name__}: {e}")
                else:
                    module_logger = logging.getLogger(func.__module__)
                    module_logger.exception(f"Exception in {func.__name__}: {e}")
                raise

        return wrapper

    return decorator

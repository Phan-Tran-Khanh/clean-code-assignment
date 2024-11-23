"""
Command-line Interface Logger
"""

import sys


class CliLogger:
    """
    Command-line Interface Logger
    """
    _instance = None

    LEVELS = {
        'DEBUG': '\033[94m',        # Blue
        'INFO': '\033[92m',         # Green
        'WARNING': '\033[93m',      # Yellow
        'ERROR': '\033[91m',        # Red
        'CRITICAL': '\033[1;91m',   # Bold Red
        'RESET': '\033[0m',         # Reset
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _log(self, level: str, message: str, to_stderr: bool = False) -> None:
        """
        Print log directly in command-line interface
        
        Args:
            level (str): Level of the logger.
            message (str): The output message
            to_stderr (bool, optional): Print in stderr instead of stdout.
            Defaults to False.

        Returns:
            None
        """
        color = self.LEVELS.get(level, '')
        reset = self.LEVELS['RESET']
        output_stream = sys.stderr if to_stderr else sys.stdout
        print(f'{color}{level}: {message}{reset}', file=output_stream)

    def debug(self, message: str) -> None:
        """
        Log debug message

        Args:
            message (str): Message
        """
        self._log('DEBUG', message)

    def info(self, message: str) -> None:
        """
        Log info message

        Args:
            message (str): Message
        """
        self._log('INFO', message)

    def warning(self, message: str) -> None:
        """
        Log warning message

        Args:
            message (str): Message
        """
        self._log('WARNING', message)

    def error(self, message: str) -> None:
        """
        Log error message

        Args:
            message (str): Message
        """
        self._log('ERROR', message, to_stderr=True)

    def critical(self, message: str) -> None:
        """
        Log critical message

        Args:
            message (str): Message
        """
        self._log('CRITICAL', message, to_stderr=True)

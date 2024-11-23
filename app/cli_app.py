
"""
Command-line Interface Application
"""

from argparse import ArgumentParser


class CliApp:
    """
    Command-line Interface Application
    """
    def __init__(self, description: str = None):
        """
        Initialize the CliApp instance.
        
        Args:
            description (str): The description of the application.
        """
        self.parser = ArgumentParser(description=description)
        self._setup_arguments()

    def _setup_arguments(self) -> None:
        """
        Initialize commonly used arguments.
        
        Returns:
            None
        """

    def add_string_argument(self, name: str, description: str) -> None:
        """
        Add a string argument to the parser.

        Args:
            name (str): Name of argument.
            description (str): Description of argument.
        
        Returns:
            None
        """
        self.parser.add_argument(name, type=str, help=description)

    def get_arguments(self) -> tuple[str]:
        """
        Get arguments value from user input

        Returns:
            tuple[str]: Tuple of arguments value
        """
        args = self.parser.parse_args()
        return tuple(vars(args).values())

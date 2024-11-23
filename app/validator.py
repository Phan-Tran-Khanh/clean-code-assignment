"""
Validator
"""
from re import match as regex_match


class Validator:
    """
    Validator
    """
    @staticmethod
    def is_list_of_strings(value: list) -> bool:
        """
        Check if a list is a list of strings

        Args:
            value (list): A list

        Returns:
            bool: True if a list of strings else False.
        """
        return all(isinstance(item, str) for item in value)

    @staticmethod
    def is_url(value: str) -> bool:
        """
        Check if a text string is a URL

        Args:
            value (str): A text string

        Returns:
            bool: True if a text string is a URL else False.
        """
        pattern = r'^https?:\/\/[^\s]+(?:\.jpg|\.jpeg|\.png|\.gif)$'
        return False if not regex_match(pattern, value) else True

"""
Mixin Class to extend behaviors of model.Model
"""

from collections import Counter
from dataclasses import fields, is_dataclass
from typing import Self, get_origin, get_args


class Mixin:
    """
    Mixin Class to extend behaviors of model.Model
    """
    def _sanitize_fields(self) -> None:
        if not is_dataclass(self):
            raise TypeError('Invalid type of instance.')

        # field.value must be a correct value or None
        for field in fields(self):
            value = getattr(self, field.name)
            if field.type == float:
                setattr(self, field.name,
                        self._convert_to_float(value, field.name))
            elif field.type == str:
                setattr(self, field.name,
                        self._sanitize_string(value, field.name))
            elif get_origin(field.type) == list and get_args(field.type) == (str,):
                if value:
                    setattr(self, field.name, self._sanitize_list_string(
                        value, field.name))
                else: # Could be empty list
                    setattr(self, field.name, None)

    def _sanitize_list_string(self, values: list[str], field: str) -> list[str]|None:
        # Sanitize each text element
        normalized_list = [self._sanitize_string(v, field) for v in values]

        # Clean semantic replicate
        compressed_list = {}
        for idx, txt in enumerate(normalized_list):
            if txt is None:
                continue
            compressed_text = txt.replace(' ', '')
            if compressed_list.get(compressed_text):
                normalized_list[idx] = None
            else:
                compressed_list[compressed_text] = 1

        normalized_list = [txt for txt in normalized_list if txt is not None]

        return normalized_list if normalized_list else None

    def _sanitize_string(self, value: str|None, field: str) -> str|None:
        if not value:
            return None

        try:
            normalized_text = value.strip()
            normalized_text = ' '.join(normalized_text.split())
            return normalized_text if normalized_text else None
        except ValueError as err:
            raise ValueError('Invalid value for ' \
                             f'{type(self).__name__}.{field}: {value}.') from err

    def _convert_to_float(self, value: float|str|None, field: str) -> float|None:
        if not value:
            return None

        if isinstance(value, float):
            return value

        try:
            return float(value)
        except ValueError as err:
            raise ValueError('Invalid value for ' \
                             f'{type(self).__name__}.{field}: {value}.') from err

    @classmethod
    def merge(cls, instance_1: Self, instance_2: Self) -> Self:
        """
        Method to merge two instances of a model
        
        Args:
            instance_1 (model.*): First model instance
            instance_2 (model.*): Second model instance

        Returns:
            model.*: The same class model
        """
        raise NotImplementedError()    

    @staticmethod
    def _capitalize_first_letter(value: str) -> str:
        return value[0].upper() + value[1:]

    @staticmethod
    def _mix_string(text_1: str, text_2: str) -> str:
        def is_similar(txt_1: str, txt_2: str) -> bool:
            txt_1 = txt_1.lower().split(' ')
            txt_2 = txt_2.lower().split(' ')

            dict_txt_1 = dict(Counter(txt_1))
            dict_txt_2 = dict(Counter(txt_2))

            return len(txt_1) == len(txt_2) and \
                dict_txt_1.keys() == dict_txt_2.keys()

        if is_similar(text_1, text_2):
            return text_1

        separator = ' ' if text_1[-1] == '.' else '. '
        return f'{text_1}{separator}{text_2}'

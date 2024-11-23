"""
Link Model
"""

from dataclasses import dataclass, fields
from typing import Self

from app.mixin import Mixin
from app.validator import Validator


@dataclass
class Link(Mixin):
    """
    Link Model
    """
    link: str
    description: str

    def __post_init__(self):
        self._sanitize_fields()

        # Specific data sanitization
        if self.description:
            self.description = Mixin._capitalize_first_letter(self.description)

        if self.link and not Validator.is_url(self.link):
            raise ValueError(f'Invalid value for {type(self).__name__}.link: ' \
                             f'{self.link}')

    @classmethod
    def merge(cls, instance_1: Self, instance_2: Self) -> Self:
        link = {}
        for field in fields(cls):
            value_1 = getattr(instance_1, field.name)
            value_2 = getattr(instance_2, field.name)

            if value_1 is None or value_2 is None:
                link[field.name] = value_1 or value_2
            elif isinstance(value_1, str):
                if value_1 != value_2:
                    raise ValueError(f'{cls.__name__}.{field.name}: ' \
                                     f'{value_1} not equals to {value_2}')
                link[field.name] = value_1
            else:
                raise ValueError(f'Invalid values for {cls.__name__}.{field.name}' \
                                 f':{value_1} and {value_2}')
        return cls(**link)

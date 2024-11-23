"""
Location Model
"""

from dataclasses import dataclass, fields
from typing import Self

from app.mixin import Mixin


@dataclass
class Location(Mixin):
    """
    Location Model
    """
    lat: float
    lng: float
    address: str
    city: str
    country: str

    def __post_init__(self):
        self._sanitize_fields()

        # Specific data sanitization
        if self.address:
            self.address = Mixin._capitalize_first_letter(self.address)

        if self.city:
            self.city = Mixin._capitalize_first_letter(self.city)

        if self.country:
            self.country = Mixin._capitalize_first_letter(self.country)

    @classmethod
    def merge(cls, instance_1: Self, instance_2: Self) -> Self:
        location = {}
        for field in fields(cls):
            value_1 = getattr(instance_1, field.name)
            value_2 = getattr(instance_2, field.name)

            if value_1 is None or value_2 is None:
                location[field.name] = value_1 or value_2
            elif isinstance(value_1, float):
                if value_1 != value_2:
                    raise ValueError(f'{cls.__name__}.{field.name}: '\
                                     f'{value_1} not equals to {value_2}')
                location[field.name] = value_1
            elif isinstance(value_1, str):
                # Best practice maybe define a list of abbreviations?
                # if value_1 != value_2:
                #     raise ValueError(f'{cls.__name__}.{field.name}: '\
                #                      f'{value_1} not equals to {value_2}')
                location[field.name] = max([value_1, value_2], key=len)
            else:
                raise ValueError(f'Invalid values for {cls.__name__}.{field.name}' \
                                 f':{value_1} and {value_2}')
        return cls(**location)

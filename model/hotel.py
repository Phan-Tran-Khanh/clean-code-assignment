"""
Hotel Model
"""

from dataclasses import asdict, dataclass, fields
from json import dumps as json_dumps
from typing import Self

from app.mixin import Mixin
from app.validator import Validator

from model.amenities import Amenities
from model.image import Image
from model.location import Location


@dataclass
class Hotel(Mixin):
    """
    Hotel Model
    """
    id: str             # Sanitized
    destination_id: int # Sanitized
    name: str
    description: str
    location: Location
    amenities: Amenities
    images: Image
    booking_conditions: list[str]

    def __str__(self):
        return json_dumps(asdict(self), indent=4)

    def __post_init__(self):
        self._sanitize_fields()

        # Specific data sanitization
        if self.name:
            self.name = Mixin._capitalize_first_letter(self.name)

        if self.description:
            self.description = Mixin._capitalize_first_letter(self.description)

        if self.booking_conditions:
            self.booking_conditions = [
                cdt.lower() for cdt in self.booking_conditions]

    @classmethod
    def merge(cls, instance_1: Self, instance_2: Self) -> Self:
        hotel = {}
        for field in fields(cls):
            value_1 = getattr(instance_1, field.name)
            value_2 = getattr(instance_2, field.name)

            if value_1 is None or value_2 is None:
                hotel[field.name] = value_1 or value_2
            elif isinstance(value_1, int):
                if value_1 != value_2:
                    raise ValueError(f'{cls.__name__}.{field.name}: ' \
                                     f'{value_1} not equals to {value_2}')
                hotel[field.name] = value_1
            elif field.name == 'name':
                hotel[field.name] = max([value_1, value_2], key=len)
            elif isinstance(value_1, str):
                hotel[field.name] = Hotel._mix_string(value_1, value_2)
            elif isinstance(value_1, list) and \
                Validator.is_list_of_strings(value_1):
                hotel[field.name] = list(set(value_1 + value_2))
            elif hasattr(field.type, 'merge') and \
                callable(getattr(field.type, 'merge')):
                hotel[field.name] = field.type.merge(value_1, value_2)
            else:
                raise AttributeError("Attribute 'merge' is not defined in " \
                                     f"'{cls.__name__}.{field.name}'")
        return cls(**hotel)

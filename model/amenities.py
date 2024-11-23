"""
Amenity Model
"""

from dataclasses import dataclass, fields
from typing import Self

from app.mixin import Mixin
from app.validator import Validator


@dataclass
class Amenities(Mixin):
    """
    Amenity Model
    """
    general: list[str]
    room: list[str]

    def __post_init__(self):
        self._sanitize_fields()

        # Specific data sanitization
        if self.general:
            self.general = [amenity.lower() for amenity in self.general]

        if self.room:
            self.room = [amenity.lower() for amenity in self.room]

        if self.general and self.room:
            # Categorize hotel amenities as some suppliers have one key
            # assigned for amenities
            general_amenities = [
                amenity.replace(' ', '') for amenity in self.general]
            room_amenities = [
                amenity.replace(' ', '') for amenity in self.room]

            for room_amenity in room_amenities:
                for idx, general_amenity in enumerate(general_amenities):
                    if room_amenity == general_amenity:
                        self.general[idx] = None

            self.general = [fac for fac in self.general if fac is not None]

    @classmethod
    def merge(cls, instance_1: Self, instance_2: Self) -> Self:
        amenities = {}
        for field in fields(cls):
            value_1 = getattr(instance_1, field.name)
            value_2 = getattr(instance_2, field.name)

            if value_1 is None or value_2 is None:
                amenities[field.name] = value_1 or value_2
            elif isinstance(value_1, list) and \
                Validator.is_list_of_strings(value_1):
                amenities[field.name] = list(set(value_1 + value_2))
            else:
                raise ValueError(f'Invalid values for {cls.__name__}.{field.name}' \
                                 f':{value_1} and {value_2}')
        return cls(**amenities)

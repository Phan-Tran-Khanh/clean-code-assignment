"""
Image Model
"""

from dataclasses import dataclass, fields
from typing import Self

from app.mixin import Mixin

from model.link import Link


@dataclass
class Image(Mixin):
    """
    Image Model
    """
    rooms: list[Link]
    site: list[Link]
    amenities: list[Link]

    @classmethod
    def merge(cls, instance_1: Self, instance_2: Self) -> Self:
        image = {}
        for field in fields(cls):
            value_1 = getattr(instance_1, field.name)
            value_2 = getattr(instance_2, field.name)

            if value_1 is None or value_2 is None:
                image[field.name] = value_1 or value_2
            elif isinstance(value_1, list):
                image[field.name] = cls.get_unique_links(value_1 + value_2)
            else:
                raise ValueError(f'Invalid values for {cls.__name__}.{field.name}' \
                                 f':{value_1} and {value_2}')
        return cls(**image)

    @staticmethod
    def get_unique_links(image_list: list[Link]) -> list[Link]:
        """
        Extract unique model.Link

        Args:
            image_list (list[Link]): List of model.Link

        Returns:
            list[Link]: List of model.Link
        """
        unique_link = {}
        for link in image_list:
            if link.link not in unique_link:
                unique_link[link.link] = link
            else:
                unique_link[link.link] = Link(
                    link=link.link,
                    description=Image._mix_string(
                        link.description, unique_link[link.link].description)
                )
        return list(unique_link.values())

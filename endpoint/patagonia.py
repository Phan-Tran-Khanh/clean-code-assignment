"""
Supplier Patagonia
"""

from app.supplier import Supplier

from model.amenities import Amenities
from model.hotel import Hotel
from model.image import Image
from model.location import Location


class Patagonia(Supplier):
    """
    Supplier Patagonia
    """
    @staticmethod
    def _get_endpoint() -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia'

    @staticmethod
    def _get_data(dto: dict) -> Hotel:
        try:
            site_images, rooms_images, amenities_images = Patagonia._get_images(
                dto['images'])
        except KeyError:
            site_images = rooms_images = amenities_images = None

        return Hotel(
            id=dto['id'],
            destination_id=dto['destination'],
            name=dto.get('name'),
            description=dto.get('info'),
            location=Location(
                lat=dto.get('lat'),
                lng=dto.get('lng'),
                address=dto.get('address'),
                city=dto.get('city'),
                country=dto.get('country')
            ),
            amenities=Amenities(
                general=dto.get('amenities'),
                room=None
            ),
            images=Image(
                rooms=rooms_images,
                site=site_images,
                amenities=amenities_images
            ),
            booking_conditions=dto.get('booking_conditions')
        )

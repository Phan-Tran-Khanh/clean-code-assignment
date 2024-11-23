"""
Supplier Paperflies
"""

from app.supplier import Supplier

from model.amenities import Amenities
from model.hotel import Hotel
from model.image import Image
from model.location import Location


class Paperflies(Supplier):
    """
    Supplier Paperflies
    """
    @staticmethod
    def _get_endpoint() -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies'

    @staticmethod
    def _get_data(dto: dict) -> Hotel:
        hotel_location = None
        if 'location' in dto:
            hotel_location = Location(
                lat=dto['location'].get('lat'),
                lng=dto['location'].get('lng'),
                address=dto['location'].get('address'),
                city=dto['location'].get('city'),
                country=dto['location'].get('country')
            )

        hotel_amenities = None
        if 'amenities' in dto:
            hotel_amenities = Amenities(
                general=dto['amenities'].get('general'),
                room=dto['amenities'].get('room')
            )

        try:
            site_images, rooms_images, amenities_images = Paperflies._get_images(
                dto['images'])
        except KeyError:
            site_images = rooms_images = amenities_images = None

        return Hotel(
            id=dto['hotel_id'],
            destination_id=dto['destination_id'],
            name=dto.get('hotel_name'),
            description=dto.get('details'),
            location=hotel_location,
            amenities=hotel_amenities,
            images=Image(
                rooms=rooms_images,
                site=site_images,
                amenities=amenities_images
            ),
            booking_conditions=dto.get('booking_conditions')
        )

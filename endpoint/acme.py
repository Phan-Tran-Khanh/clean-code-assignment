"""
Supplier Acme
"""

from re import sub as re_sub

from app.supplier import Supplier

from model.amenities import Amenities
from model.hotel import Hotel
from model.location import Location


class Acme(Supplier):
    """
    Supplier Acme
    """
    @staticmethod
    def _get_endpoint() -> str:
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme'

    @staticmethod
    def _get_data(dto: dict) -> Hotel:
        # Return full address in conversion
        hotel_address = dto.get('Address', '').strip()
        hotel_postal_code = dto.get('PostalCode', '').strip()
        if hotel_postal_code and hotel_address:
            full_address = hotel_address if hotel_postal_code in hotel_address \
                else f'{hotel_address}, {hotel_postal_code}'
        else:
            full_address = hotel_address or hotel_postal_code

        facilities = dto.get('Facilities')
        if facilities:
            facilities = [
                re_sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', facility)
                for facility in facilities]

        # Pattern: PascalCase
        return Hotel(
            id=dto['Id'],
            destination_id=dto['DestinationId'],
            name=dto.get('Name'),
            description=dto.get('Description'),
            location=Location(
                lat=dto.get('Latitude'),
                lng=dto.get('Longitude'),
                address=full_address,
                city=dto.get('City'),
                country=dto.get('Country')
            ),
            amenities=Amenities(
                general=facilities,
                room=None
            ),
            images=None,
            booking_conditions=dto.get('BookingConditions')
        )


"""
Hotel Command-line Interface Application
"""

from app.cli_app import CliApp
from app.cli_logger import CliLogger
from app.database import Database


LOG = CliLogger()

class HotelApp(CliApp):
    """
    Hotel Command-line Interface Application
    """
    def __init__(self, description: str = None):
        super().__init__(description)
        self.db = Database()

    def _setup_arguments(self) -> None:
        self.add_string_argument(
            name='hotel_ids',
            description='List of comma-separated hotel IDs.')
        self.add_string_argument(
            name='destination_ids',
            description='List of comma-separated destination IDs.')

    def run(self):
        hotel_ids, destination_ids = self.get_arguments()
        if hotel_ids == 'none' or destination_ids == 'none':
            LOG.info('Retrieving all hotels data.')
            print(self.db.get_all_hotels())
        else:
            try:
                hotel_ids = hotel_ids.split(',')
                destination_ids = destination_ids.split(',')
                destination_ids = [int(d_id) for d_id in destination_ids]
            except ValueError as err:
                raise ValueError(f'Invalid values: {destination_ids}') from err

            hotels = []
            for hotel_id in hotel_ids:
                for destination_id in destination_ids:
                    LOG.info('Retrieving data of hotel, ' \
                             f'id={hotel_id} destination_id={destination_id}.')
                    hotel = self.db.get_hotel(hotel_id, destination_id)
                    if hotel:
                        hotels.append(hotel)
                        continue
                    LOG.error('Cannot retrieve data of hotel, ' \
                              f'id={hotel_id} destination_id={destination_id}.')
            print(hotels)

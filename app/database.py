
"""
Simulated-database
"""

from app.cli_logger import CliLogger
from app.supplier import Supplier

from endpoint.acme import Acme
from endpoint.paperflies import Paperflies
from endpoint.patagonia import Patagonia

from model.hotel import Hotel


LOG = CliLogger()

class Database:
    """
    Simulated-database
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._suppliers: list[Supplier] = []    # Composition of suppliers
        self._data: dict[tuple[str, int], Hotel] = {}

        # Add available suppliers
        self._add_supplier(Acme())
        self._add_supplier(Paperflies())
        self._add_supplier(Patagonia())
        LOG.info(f'Initialize a total of {len(self._suppliers)} suppliers')

        # Fetch hotel data from each supplier
        self._data = self._fetch_data()
        LOG.info(f'Initialize a total of {len(self._data)} unique hotels')


    def _add_supplier(self, supplier: Supplier) -> None:
        self._suppliers.append(supplier)

    def _fetch_data(self):
        hotel_data = []
        for supplier in self._suppliers:
            hotel_data.extend(supplier.fetch_data())
        return Database._merge_data(hotel_data)

    @staticmethod
    def _merge_data(dataset: list[Hotel]) -> dict[tuple[str, int], Hotel]:
        hotel_data = {}
        for hotel in dataset:
            retrieval_key = (hotel.id, hotel.destination_id)
            if retrieval_key not in hotel_data:
                hotel_data[retrieval_key] = hotel
            else:
                hotel_data[retrieval_key] = Hotel.merge(
                    hotel_data[retrieval_key], hotel
                )
        return hotel_data

    def get_all_hotels(self) -> list[Hotel]:
        """
        Get all hotels data

        Returns:
            list[Hotel]: All hotels data
        """
        return list(self._data.values())

    def get_hotel(self, hotel_id: str, destination_id: int) -> Hotel|None:
        """
        Get hotel by id and destination id

        Args:
            hotel_id (str): Hotel id
            destination_id (int): Destination id

        Returns:
            Hotel|None: Specific hotel data or None.
        """
        if not hotel_id or not destination_id:
            return None
        return self._data.get((hotel_id, destination_id), None)

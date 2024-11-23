"""
Hotel Data Supplier
"""
import requests

from app.cli_logger import CliLogger

from model.hotel import Hotel
from model.link import Link


LOG = CliLogger()

class Supplier:
    """
    Hotel Data Supplier
    """
    @staticmethod
    def _get_endpoint() -> str:
        """
        Endpoint of supplier to fetch data
        """
        raise NotImplementedError()

    @staticmethod
    def _get_data(dto: dict) -> Hotel:
        """
        Parse supplier-provided data into Hotel object

        Returns:
            model.hotel.Hotel
        """
        raise NotImplementedError()

    @staticmethod
    def _get_images(dto: dict) -> tuple[list[Link]|None]:
        def get_links(images_list: list):
            images = []
            for img in images_list:
                images.append(
                    Link(link=img.get('link') or img.get('url'),
                        description=img.get('caption') or img.get('description')))
            return images

        rooms_images = amenities_images = site_images = None
        if 'site' in dto:
            site_images = get_links(dto['site'])
        if 'rooms' in dto:
            rooms_images = get_links(dto['rooms'])
        if 'amenities' in dto:
            amenities_images = get_links(dto['amenities'])
        return site_images, rooms_images, amenities_images

    def fetch_data(self) -> list[Hotel]:
        """
        Fetch hotel data from the supplier
        
        Returns:
            list[Hotel]: Supplier dataset
        """
        try:
            url = self._get_endpoint()
            response = requests.get(url, timeout=120)

            dataset = []
            for dto in response.json():
                data = self._get_data(dto)
                LOG.info(f'Fetched from Supplier: {data}')
                dataset.append(data)
            return dataset
        except requests.exceptions.Timeout:
            LOG.error('Double check your network connection and ' \
                      'suppliers endpoint.')
        raise requests.RequestException

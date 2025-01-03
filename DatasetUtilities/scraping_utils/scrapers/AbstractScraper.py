from abc import abstractmethod, ABC


class AbstractScraper(ABC):

    @staticmethod
    @abstractmethod
    def scrape_images(query, api_key=None, count=100) -> list:
        pass
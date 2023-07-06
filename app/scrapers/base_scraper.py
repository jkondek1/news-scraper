import logging
from abc import ABC, abstractmethod

import requests
import validators

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class BaseScraper(ABC):
    """Base class for news scrapers."""

    def __init__(self, url: str):
        self.url = self.set_url(url)

    @staticmethod
    def set_url(url: str) -> str:
        if not validators.url(url):
            logger.info('invalid url, trying to automatically fix by adding https:// ...')
            url = 'https://' + url
            if not validators.url(url):
                raise ValueError("Invalid URL")
            logger.info('url fixed')
        return url

    def scrape_articles(self) -> None:
        content = self._download_website_content()
        articles = self._parse_articles(content)
        self._save_articles(articles)

    def _download_website_content(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise ConnectionError(f"Could not connect to {self.url}")
        return response.text

#     def _save_articles(self, list[Article], db_connector):
#        for article in list[Article]:
#           db_connector.save_article(article)

    @abstractmethod
    def _parse_articles(self, content: str) -> list[Article]:
    """returns combinations of article url and header parsing the main website of the news server,
    store in Article object
    """

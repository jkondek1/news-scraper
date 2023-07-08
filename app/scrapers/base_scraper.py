import logging
from abc import ABC, abstractmethod

import requests
import validators
from bs4 import BeautifulSoup

from app.data import Article
from app.data.cache import ArticleCache
from app.database.database_handler import DatabaseHandler

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

    def scrape_articles(self, cache, db_handler) -> None:
        content = self._download_website_content()
        articles = self._parse_articles(content)
        self._save_articles(articles=articles, cache=cache, db_handler=db_handler)

    def _download_website_content(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise ConnectionError(f"Could not connect to {self.url}")
        return response.text

    def _save_articles(self, articles: list[Article], cache: ArticleCache, db_handler: DatabaseHandler) -> None:
        unique_articles = cache.validate_if_in_cache(articles)
        db_handler.connect()
        db_handler.add_to_db(unique_articles)
        self._save_keywords(unique_articles)

    @staticmethod
    def _save_keywords(articles: list[Article], db_handler: DatabaseHandler):
        for article in articles:
            db_handler.add_to_db(article.keywords)

    @staticmethod
    def _get_bs_soup(content: str):
        return BeautifulSoup(content, 'html.parser')

    @abstractmethod
    def _parse_articles(self, content: str) -> list[Article]:
        """
        returns combinations of article url and header parsing the main website of the news server,
        store in Article object
        """

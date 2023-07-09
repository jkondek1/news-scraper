import logging
from abc import ABC, abstractmethod

import requests
import sqlalchemy
import validators
from bs4 import BeautifulSoup

from scraper.data import Article
from scraper.data.cache import ArticleCache
from scraper.database.database_handler import DatabaseHandler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class BaseScraper(ABC):
    """Base class for news scrapers."""

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
        logger.info(f'scraping using {self.__class__.__name__}')
        content = self._download_website_content()
        articles = self._parse_articles(content)
        self._save_articles(articles=articles, cache=cache, db_handler=db_handler)

    def _download_website_content(self):
        logger.info('getting website content')
        response = requests.get(self.url)
        if response.status_code != 200:
            raise ConnectionError(f"Could not connect to {self.url}")
        return response.text

    def _save_articles(self, articles: list[Article], cache: ArticleCache, db_handler: DatabaseHandler) -> None:
        logger.info('storing articles ...')
        unique_articles = cache.validate_if_in_cache(articles)
        if unique_articles:
            try:
                db_handler.connect()
                logger.info('inserting articles to database')
                db_handler.add_to_db(unique_articles)
                self._save_keywords(unique_articles)
            except sqlalchemy.exc.ArgumentError:
                logger.error('db connection failed, storing only in cache')
            cache.fill(unique_articles)

    @staticmethod
    def _save_keywords(articles: list[Article], db_handler: DatabaseHandler):
        logger.info('inserting keywords to database')
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

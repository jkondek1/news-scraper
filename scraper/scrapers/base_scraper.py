import logging
from abc import ABC, abstractmethod

import requests
import sqlalchemy
from bs4 import BeautifulSoup

from scraper.data import Article
from scraper.data.cache import ArticleCache
from scraper.database.database_handler import DatabaseHandler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class BaseScraper(ABC):
    """Base class for news scrapers."""

    def scrape_articles(self, cache: ArticleCache, db_handler: DatabaseHandler) -> None:
        """
        method orchestrating scraping process
        :param cache: cache object serving as a temporary storage for articles
        :param db_handler: database handler object
        """
        logger.info(f'scraping using {self.__class__.__name__}')
        content = self._download_website_content()
        if content:
            articles = self._parse_articles(content)
            self._save_articles(articles=articles, cache=cache, db_handler=db_handler)
        else:
            logger.info('no content parsed')

    def _download_website_content(self) -> str | None:
        """
        method downloading website content
        :return: string containing website content or None if exception occurred
        """
        logger.info('getting website content')
        try:
            response = requests.get(self.url)
            if response.status_code != 200:
                logger.info(f'get request failed, status code:{response.status_code}')
        except requests.exceptions.RequestException as e:
            logger.error(f'an error occurred: {e}')
            response.text = None
        return response.text

    def _save_articles(self, articles: list[Article], cache: ArticleCache, db_handler: DatabaseHandler) -> None:
        """
        method managing saving articles to cache and database
        :param articles: article objects containing all relevant scraped data
        :param cache: cache object serving as a temporary storage for articles
        :param db_handler: database handler object
        :return:
        """
        logger.info('storing articles ...')
        unique_articles = cache.validate_if_in_cache(articles)
        if unique_articles:
            try:
                db_handler.connect()
                logger.info('inserting articles to database')
                db_handler.add_to_db(unique_articles)
                self._save_keywords(unique_articles, db_handler=db_handler)
            except sqlalchemy.exc.ArgumentError:
                logger.error('db connection failed, storing only in cache')
            cache.fill(unique_articles)

    @staticmethod
    def _save_keywords(articles: list[Article], db_handler: DatabaseHandler):
        """
        method saving keywords to database
        :param articles: article objects containing all relevant scraped data
        :param db_handler: database handler object
        """
        logger.info('inserting keywords to database')
        for article in articles:
            db_handler.add_to_db(article.keywords)

    @staticmethod
    def _get_bs_soup(content: str) -> BeautifulSoup:
        return BeautifulSoup(content, 'html.parser')

    @abstractmethod
    def _parse_articles(self, content: str) -> list[Article]:
        """
        returns combinations of article url and header parsing the main website of the news server,
        store in Article object
        :param content: string containing website content
        """

import logging
import re
from datetime import datetime

from bs4 import BeautifulSoup

from scraper.data import Article
from scraper.scrapers.base_scraper import BaseScraper

logger = logging.getLogger()


class SmeScraper(BaseScraper):
    url = 'https://www.sme.sk'

    def _parse_articles(self, content: str) -> list[Article]:
        logger.info('parsing articles')
        articles = []
        soup = self._get_bs_soup(content)
        subsections = self._get_subsection_list(soup)
        for section in subsections:
            articles.append(self._get_article_objects(section))
        return articles

    @staticmethod
    def _get_subsection_list(soup: BeautifulSoup) -> list[BeautifulSoup]:
        """
        get smaller subsections from the main page
        :param soup:
        :return: list of subsections
        """
        subsections = soup.find_all("h2", {"class": "media-heading"})
        return subsections

    @staticmethod
    def _get_article_objects(section: BeautifulSoup) -> Article:
        heading = re.search(r'<a[^>]+>([^<]+)</a>', str(section)).group(1)
        url = re.search('href="(.+)">?', str(section)).group(1)
        return Article(url=url, header=heading, timestamp=datetime.now())

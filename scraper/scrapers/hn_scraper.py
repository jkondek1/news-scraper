import logging
import re
from datetime import datetime

from bs4 import BeautifulSoup

from scraper.data import Article
from scraper.scrapers.base_scraper import BaseScraper

logger = logging.getLogger()


class HnScraper(BaseScraper):
    url = 'https://www.hn.cz'

    def _parse_articles(self, content: str) -> list[Article]:
        articles = []
        soup = self._get_bs_soup(content)
        subsections = self._get_subsection_list(soup)
        for section in subsections:
            articles.append(self._get_article_objects(section))
        return articles

    @staticmethod
    def _get_subsection_list(soup) -> list[BeautifulSoup]:
        """
        get smaller subsections from the main page
        :param soup: BeautifulSoup object containg parsed website content
        :return: list of subsections
        """
        subsections = soup.find_all("div", {'class', 'article-box'})
        return subsections

    @staticmethod
    def _get_article_objects(section: BeautifulSoup) -> Article:
        heading = re.search(r'<a[^>]+>([^<]+)</a>', str(section)).group(1)
        url = 'https:' + re.search('href="(.+)">?', str(section)).group(1)
        return Article(url=url, header=heading, timestamp=datetime.now())

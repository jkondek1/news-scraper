import re
from datetime import datetime

from app.data import Article
from app.data.keyword import Keyword
from app.scrapers.base_scraper import BaseScraper


class SmeScraper(BaseScraper):
    def __init__(self, url: str):
        super().__init__(url)

    def _parse_articles(self, content: str) -> list[Article]:
        articles = []
        soup = self._get_bs_soup(content)
        subsections = self._get_subsection_list(soup)
        for section in subsections:
            articles.append(self._get_article_objects(section))
        return articles

    @staticmethod
    def _get_subsection_list(soup):
        subsections = soup.find_all("h2", {"class": "media-heading"})
        return subsections

    @staticmethod
    def _get_article_objects(section):
        heading = re.search(r'<a[^>]+>([^<]+)</a>', str(section)).group(1)
        url = re.search('href="(.+)">?', str(section)).group(1)
        return Article(heading, url, datetime.now(), Keyword(heading))

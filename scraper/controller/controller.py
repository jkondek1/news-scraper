import logging
import time

import schedule

from scraper.data.cache import ArticleCache
from scraper.database.database_handler import DatabaseHandler
from scraper.scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class Controller:

    def __init__(self, db_handler: DatabaseHandler, scrapers: list[BaseScraper], cache: ArticleCache):
        self.db = db_handler
        self.scrapers = scrapers
        self.cache = cache

    def run_scheduled(self, interval_min: int = 1):
        logger.info('running...')
        schedule.every(interval_min).minutes.do(self._run_scrapers)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def _run_scrapers(self):
        logger.info('starting scheduled scraping ...')
        for scraper in self.scrapers:
            scraper.scrape_articles(db_handler=self.db, cache=self.cache)

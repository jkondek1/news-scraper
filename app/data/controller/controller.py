import schedule

from app.data.cache import ArticleCache
from app.database.database_handler import DatabaseHandler
from app.scrapers.base_scraper import BaseScraper


class Controller:

    def __init__(self, db_handler: DatabaseHandler, scrapers: list[BaseScraper], cache: ArticleCache):
        self.db = db_handler
        self.scrapers = scrapers
        self.cache = cache

    def run_schedule(self, interval_min: int = 1):
        schedule.every(interval_min).minutes.do(self._run_scrapers)

    def _run_scrapers(self):
        for scraper in self.scrapers:
            scraper.scrape_articles(db_handler=self.db)

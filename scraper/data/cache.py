import logging
from datetime import timedelta, datetime

from scraper.data import Article

logger = logging.getLogger(__name__)


class ArticleCache:
    def __init__(self):
        self.cache = {}

    def __repr__(self):
        return '\n'.join([self._repr_one_article(article) for article in self.cache.values()])

    def __len__(self):
        return len(self.cache)

    @staticmethod
    def _repr_one_article(article):
        return f'{article.url} with timestamp {article.timestamp}'

    def fill(self, articles):
        self._delete_day_old_articles()
        for article in articles:
            self.cache[article.url] = article
        logger.info(f'{len(articles)} articles added to cache')

    def validate_if_in_cache(self, articles: list[Article]) -> list[Article]:
        """Checks if articles are already in cache, returns list of articles not in cache."""
        articles_not_in_cache = []
        for article in articles:
            if article.url not in self.cache:
                articles_not_in_cache.append(article)
        return articles_not_in_cache

    def _delete_day_old_articles(self):
        counter = 0
        for url, article in list(self.cache.items()):
            if article.timestamp < datetime.now() - timedelta(days=1):
                counter += 1
                del self.cache[url]
        if counter > 0:
            logger.info(f'{counter} articles deleted from cache')

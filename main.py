import argparse
import logging
import threading

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from rest_api.schema import KeywordRequest
from scraper.controller.controller import Controller
from scraper.data.cache import ArticleCache
from scraper.database.database_handler import DatabaseHandler
from scraper.scrapers.hn_scraper import HnScraper
from scraper.scrapers.sme_scraper import SmeScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--app_host', default='0.0.0.0')
parser.add_argument('--app_port', default=8080)
parser.add_argument('--app_workers', default=1)
parser.add_argument('--db_', default='localhost')
parser.add_argument('--db_port', default=5432)
parser.add_argument('--db_user', default='postgres')
parser.add_argument('--db_password', default='posgres')
parser.add_argument('--db_name', default='news')

scrapers = [HnScraper(), SmeScraper()]
cache = ArticleCache()


def create_db_url(user, password, host, port, name):
    """
    method creating db url from parsed arguments
    """
    return f'postgresql://{user}:{password}@{host}:{port}/{name}'


def create_app(database_handler):
    """
    method creating app instance
    """
    app = FastAPI()

    @app.on_event('startup')
    def run_scraping_in_background():
        """
        method invoking scheduled task
        """
        controller = Controller(db_handler=database_handler,
                                scrapers=scrapers,
                                cache=cache)
        scheduler_thread = threading.Thread(target=controller.run_scheduled)
        logger.info('starting scheduler thread...')
        scheduler_thread.start()

    @app.get('/articles/find')
    def list_articles_by_keyword(request: KeywordRequest):
        """
        public method querying all articles relevant to some listed keywords
        """
        articles = database_handler.query_by_keyword(request.keywords)
        return jsonable_encoder(articles)

    return app


if __name__ == "__main__":
    args = parser.parse_args()
    db_handler = DatabaseHandler(
        db_url=create_db_url(args.db_user, args.db_password, args.db_host, args.db_port, args.db_name))
    uvicorn.run(create_app(db_handler), host=args.app_host, port=args.app_port, workers=args.app_workers)

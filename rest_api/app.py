import logging
import threading

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

app = FastAPI()

database_handler = DatabaseHandler('postgresql://localhost:5432/news')
scrapers = [HnScraper(), SmeScraper()]
cache = ArticleCache()


@app.on_event('startup')
def run_scraping_in_background():
    controller = Controller(db_handler=database_handler,
                            scrapers=scrapers,
                            cache=cache)
    scheduler_thread = threading.Thread(target=controller.run_scheduled)
    logger.info('starting scheduler thread...')
    scheduler_thread.start()


@app.get('/articles/find')
def list_articles_by_keyword(request: KeywordRequest):
    articles = database_handler.query_by_keyword(request.keywords)
    return jsonable_encoder(articles)

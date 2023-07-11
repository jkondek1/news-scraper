import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from rest_api.schema import KeywordRequest
from scraper.data import Article
from scraper.data.article import Base
from scraper.data.keyword import Keyword

logger = logging.getLogger(__name__)


class DatabaseHandler:
    """
    TODO user management
    """

    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = None
        self.Session = None

    def connect(self):
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        if not self.engine or not self.Session:
            raise ValueError("You must connect to the database first.")
        return self.Session()

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.Session = None

    def add_to_db(self, sql_objects: list):
        session = self.get_session()
        for obj in sql_objects:
            try:
                session.add(obj)
            except:
                logger.error('data already in db, insert not successful')
        session.commit()

    @staticmethod
    def query_by_keyword(session, request: KeywordRequest):
        # TODO implement search of semantically similar keywords - to eliminate lemmatization issues
        # TODO and make up for imprecise keywords
        results = session.query(Keyword).join(Article).filter(Keyword.keyword == keyword).all()
        return results

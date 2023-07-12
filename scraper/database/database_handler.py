import logging

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scraper.data import Article
from scraper.data.article import Base
from scraper.data.keyword import Keyword

logger = logging.getLogger(__name__)


class DatabaseHandler:
    """
    Handles connection to the database, adding articles to it and querying data
    TODO: user management
    """

    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = None
        self.Session = None

    def connect(self) -> None:
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(bind=self.engine, checkfirst=True)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self) -> sqlalchemy.orm.session.Session:
        if not self.engine or not self.Session:
            raise ValueError("You must connect to the database first.")
        return self.Session()

    def disconnect(self) -> None:
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.Session = None

    def add_to_db(self, sql_objects: list) -> None:
        """
        inserts objects into the respective database tables
        :param sql_objects:
        """
        session = self.get_session()
        for obj in sql_objects:
            session.add(obj)
        try:
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            logger.error('data already in db, insert not successful')

    def query_by_keyword(self, keywords: list[str]) -> list[Article]:
        """
        queries database for articles containing at least one of given keywords
        :param keywords: validated list of strings to be found in the keyword table
        :return: relevant article objects
        """
        # TODO implement search of semantically similar keywords - to eliminate lemmatization issues
        # TODO and make up for imprecise keywords
        ses = self.get_session()
        results = ses.query(Keyword).join(Article).filter(Keyword.keyword.in_(keywords)).all()
        return results

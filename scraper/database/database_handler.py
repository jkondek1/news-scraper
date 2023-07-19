import logging

import sqlalchemy
from fastapi import HTTPException
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
        self.engine = create_engine(db_url, echo=True)
        self.session_maker = self._connect()

    def add_to_db(self, sql_objects: list) -> None:
        """
        inserts objects into the respective database tables
        :param sql_objects:
        """
        session = self._get_session(self.session_maker)
        if session:
            for obj in sql_objects:
                session.add(obj)
            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                logger.error('data already in db, insert not successful')
            session.close()
        else:
            logger.error(f'db connection failed: attempted url: {self.db_url}')

    def query_by_keyword(self, keywords: list[str]) -> list[Article]:
        """
        queries database for articles containing at least one of given keywords
        :param keywords: validated list of strings to be found in the keyword table
        :return: relevant article objects
        """
        # TODO implement search of semantically similar keywords - to eliminate lemmatization issues
        # TODO and make up for imprecise keywords
        session = self._get_session(self.session_maker)
        if session:
            results = session.query(Keyword).join(Article).filter(Keyword.keyword.in_(keywords)).all()
        else:
            raise HTTPException(status_code=503, detail="Database connection error")
        session.close()
        return results

    def _connect(self) -> sqlalchemy.orm.session.Session | None:
        try:
            Base.metadata.create_all(bind=self.engine, checkfirst=True)
            ses = sessionmaker(bind=self.engine)
        except sqlalchemy.exc.OperationalError:
            logger.error(f'db connection failed: attempted url: {self.db_url}')
            ses = None
        return ses

    @staticmethod
    def _get_session(session_factory) -> sqlalchemy.orm.session.Session | None:
        if None:
            return None
        return session_factory()

    def disconnect(self) -> None:
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.session_maker = None

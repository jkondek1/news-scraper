from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scraper.data import Article
from scraper.data.keyword import Keyword


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
        objects = []
        for obj in sql_objects:
            self.session.add(obj)
            objects.append(obj)
            self.session.commit()
            return objects

    @staticmethod
    def query_by_keyword(session, keyword):
        # TODO implement search of semantically similar keywords - to eliminate lemmatization issues
        # TODO and make up for imprecise keywords
        results = session.query(Keyword).join(Article).filter(Keyword.keyword == keyword).all()
        return results

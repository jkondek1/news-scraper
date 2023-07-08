from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseHandler:
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

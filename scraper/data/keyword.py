import logging
from dataclasses import dataclass

from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship

from scraper.data.sql_base import Base

logger = logging.getLogger(__name__)


@dataclass
class Keyword(Base):
    """Represents a set of keywords."""
    __tablename__ = 'keywords'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    url: str = Column(String)
    keyword: str = Column(String)
    article = relationship('Article', back_populates='keywords')

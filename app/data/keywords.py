import logging
from dataclasses import dataclass

from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

logger = logging.getLogger(__name__)


@dataclass
class Keyword:
    """Represents a set of keywords."""
    __tablename__ = 'keywords'

    url: str = Column(String, primary_key=True)
    keyword: set[str] = Column(String)
    article = relationship('Article', back_populates='keywords')

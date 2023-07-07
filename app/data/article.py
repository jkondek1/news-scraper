import logging
import re
from dataclasses import dataclass
from datetime import datetime

import simplemma
from langdetect import detect
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

logger = logging.getLogger(__name__)

LANGUAGES = ['sk', 'cs', 'en']


@dataclass
class Article(Base):
    __tablename__ = 'articles'
    """Represents an article from a news server."""
    header: str = Column(String, primary_key=True)
    url: str = Column(String)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)
    keywords = relationship('Keyword', back_populates='article')

    @hybrid_property
    def keywords(self) -> set:
        return self._get_keywords()

    def _get_keywords(self, text: str) -> set[str]:
        detected_lang = self._get_language_setting(text)
        text = re.sub('[.|,|!|?|:|;|\'|\"]', ' ', text)
        tokens = [tok.lower() for tok in text.split(' ') if tok != '']
        if detected_lang:
            keywords = [simplemma.lemmatize(tok, lang=detected_lang) for tok in tokens]
        else:
            logger.info('valid language not detected, not lematizing tokens')
            keywords = tokens
        return set(keywords)

    @staticmethod
    def _get_language_setting(text: str, valid_languages=LANGUAGES) -> str | None:
        lang = detect(text)
        if lang not in valid_languages:
            return None
        return lang

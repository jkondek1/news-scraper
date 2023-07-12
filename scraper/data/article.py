import logging
import re
from dataclasses import dataclass
from datetime import datetime

import simplemma
from langdetect import detect
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from scraper.data.keyword import Keyword
from scraper.data.sql_base import Base

logger = logging.getLogger(__name__)

LANGUAGES = ['sk', 'cs', 'en']


@dataclass
class Article(Base):
    __tablename__ = 'articles'
    """Represents an article from a news server."""
    url: str = Column(String, primary_key=True)
    header: str = Column(String)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)

    @hybrid_property
    def keywords(self) -> list[Keyword]:
        keywords = self._get_keywords(self.header)
        return self._create_keyword_instances(keywords)

    def _get_keywords(self, text: str) -> set[str]:
        detected_lang = self._get_language_setting(text)
        text = re.sub('[.|,|!|?|:|;|\'|\"]', ' ', text)
        tokens = [tok.lower() for tok in text.split(' ') if tok != '']
        if detected_lang:
            keywords = [simplemma.lemmatize(tok, lang=detected_lang).lower() for tok in tokens]
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

    def _create_keyword_instances(self, keywords: list[str]) -> list[Keyword]:
        kw_objects = []
        for kw in keywords:
            kw_objects.append(Keyword(url=self.url, keyword=kw))
        return kw_objects

import logging
import re
from dataclasses import dataclass

import simplemma
from langdetect import detect

logger = logging.getLogger(__name__)

LANGUAGES = ['sk', 'cs', 'en']


@dataclass
class Keywords:
    """Represents a set of keywords."""
    keywords: set[str]

    def __init__(self, text: str):
        self.keywords = self._get_keywords(text)

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

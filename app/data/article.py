from dataclasses import dataclass
from datetime import datetime

from app.data.keywords import Keywords


@dataclass
class Article:
    """Represents an article from a news server."""
    # TODO: add validation
    header: str
    url: str
    timestamp: datetime
    keywords: Keywords

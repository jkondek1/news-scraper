from dataclasses import dataclass
from datetime import datetime


@dataclass
class Article:
    """Represents an article from a news server."""
    header: str
    url: str
    timestamp: datetime.datetime.now()


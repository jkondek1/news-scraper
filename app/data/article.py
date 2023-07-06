from dataclasses import dataclass
from datetime import datetime


@dataclass
class Article:
    """Represents an article from a news server."""
    # TODO: add validation
    header: str
    url: str
    timestamp: datetime

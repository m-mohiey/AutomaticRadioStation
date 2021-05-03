from enum import Enum, auto
from datetime import datetime, timedelta
from Media import Media

class Priority(Enum):
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

class Program:
    def __init__(self, media: Media, start: datetime, priority: Priority):
        self.media = media
        self.priority = priority
        self.start = start
        
    @property
    def idx(self) -> float:
        return self.start.timestamp() if self.start else None

    
    @property
    def end(self) -> datetime:
        return self.start + self.media.duration if self.start else None

    @property
    def duration(self) -> timedelta:
        return self.media.duration




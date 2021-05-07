from enum import Enum, auto
from datetime import datetime, timedelta
from Media import Media
import os

class Priority(Enum):
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

class Program:
    def __init__(self, media: Media, start: datetime, priority: Priority, name: str = ''):
        self.media = media
        self.priority = priority
        self.start = start
        self.name = name
        self._duration = None

    def __repr__(self):
        return f'{self.__class__.__name__}({os.path.basename(self.media.path)}, {self.start} -> {self.end}, {self.priority}, {self.name})'
        
    @property
    def idx(self) -> float:
        return self.start.timestamp() if self.start else None

    
    @property
    def end(self) -> datetime:
        return self.start + self.duration if self.start else None

    @property
    def duration(self) -> timedelta:
        return (self._duration if self._duration else self.media.duration)

    @duration.setter
    def duration(self, d: timedelta):
        self._duration = d




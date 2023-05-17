from datetime import datetime
from enum import Enum


class StatusEmoji(Enum):
    SMILING_FACE = "\U0001F604"
    SHOCKED_FACE = "\U0001F630"
    X_MARK = "\U0000274C"
    QUESTION_MARK = "\U00002753"


class EventStatus(Enum):
    REGULAR = StatusEmoji.SMILING_FACE.value
    ALMOST_SOLDOUT = StatusEmoji.SHOCKED_FACE.value
    SOLDOUT = StatusEmoji.X_MARK.value
    UNKNOWN = StatusEmoji.QUESTION_MARK.value


class Event(object):
    def __init__(self, name: str, date: datetime, status: EventStatus, url: str, place: str):
        self.name = name
        self.date = date
        self.status = status
        self.url = url
        self.place = place

    def _get_emoji_status(self) -> str:
        return self.status.value

    def _pretty_date(self) -> str:
        return self.date.strftime("%A %d/%m/%Y")

    def is_soldout(self) -> bool:
        return self.status == EventStatus.SOLDOUT

    def short_title(self) -> str:
        return f"{self.name} ({self._pretty_date()})"

    def menu_title(self) -> str:
        return f"{self.name}  {self._get_emoji_status()}  ({self._pretty_date()})"

    def long_title(self) -> str:
        return f"{self.menu_title()}\n{self.url}"

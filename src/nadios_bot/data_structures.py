from nadios_bot.consts import StatusEmoji
from datetime import datetime
from enum import Enum


class EventStatus(Enum):
    REGULAR = "regular"
    ALMOST_SOLDOUT = "almost soldout"
    SOLDOUT = "soldout"


class Event(object):
    def __init__(self, name: str, date: datetime, status: EventStatus, url: str, place: str):
        self.name = name
        self.date = date
        self.status = status
        self.url = url
        self.place = place

    def _get_emoji_info(self) -> str:
        return StatusEmoji.SHOCKED_FACE.value if self.status == EventStatus.ALMOST_SOLDOUT else StatusEmoji.SMILING_FACE.value

    def _pretty_date(self) -> str:
        return self.date.strftime("%A %d/%m/%Y")

    def is_soldout(self) -> bool:
        return self.status == EventStatus.SOLDOUT

    def short_title(self) -> str:
        return f"{self.name} ({self._pretty_date()})"

    def menu_title(self) -> str:
        return f"{self.name}  {self._get_emoji_info()}  ({self._pretty_date()})"

    def long_title(self) -> str:
        return f"{self.menu_title()}\n{self.url}"

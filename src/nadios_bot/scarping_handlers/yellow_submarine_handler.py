from nadios_bot.scarping_handlers.scrap_utils import get_data_from_url
from nadios_bot.consts import YELLOW_SUBMARINE_URL, Places
from nadios_bot.data_structures import EventStatus, Event
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from typing import List


def parse_raw_events(raw_data: BeautifulSoup) -> List[Event]:
    raw_events = raw_data.select("div.b-artist")

    events = []
    for raw_event in raw_events:
        events.append(parse_raw_event(raw_event))

    return events


def parse_raw_event(raw_event: Tag) -> Event:
    event_name = raw_event.select("div.b-artist__info-title")[0].text
    event_url = raw_event.select("a.abs-link")[0].get("href")
    event_date = raw_event.select("div.b-artist__info")[1].span.text
    event_date = datetime.strptime(event_date, '%d.%m').replace(year=datetime.today().year)

    return Event(name=event_name,
                 date=event_date,
                 status=EventStatus.REGULAR,
                 url=event_url,
                 place=Places.YELLOW_SUBMARINE.value)


def get_yellow_submarine_events() -> List[Event]:
    raw_data = get_data_from_url(YELLOW_SUBMARINE_URL)
    events = parse_raw_events(raw_data)
    return events

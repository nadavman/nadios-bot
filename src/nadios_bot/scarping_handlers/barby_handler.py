from nadios_bot.scarping_handlers.scrap_utils import get_data_from_url
from nadios_bot.data_structures import EventStatus, Event
from nadios_bot.consts import BARBY_URL,Places
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from typing import List


def parse_raw_events(url: str, raw_data: BeautifulSoup) -> List[Event]:
    raw_events = raw_data.select("td.defaultRowHeight")

    events = []
    for raw_event in raw_events:
        events.append(parse_raw_event(url, raw_event))

    return events


def parse_raw_event(url: str, raw_event: Tag) -> Event:
    event_name = raw_event.select("div.defShowListDescHeight")[0].a.get_text()
    event_date = raw_event.select("div.def_titel2A")[0].get_text().split()[1]
    event_date = datetime.strptime(event_date, '%d/%m/%Y')
    event_url = url + raw_event.select("div.defShowListDescHeight")[0].a.get('href')

    if raw_event.select("img.blink-image"):
        event_status = EventStatus.ALMOST_SOLDOUT
    elif raw_event.select("img.showsoldoutListimg"):
        event_status = EventStatus.SOLDOUT
    else:
        event_status = EventStatus.REGULAR

    return Event(name=event_name,
                 date=event_date,
                 status=event_status,
                 url=event_url,
                 place=Places.BARBY.value)


def get_barby_events() -> List[Event]:
    raw_data = get_data_from_url(BARBY_URL)
    events = parse_raw_events(BARBY_URL, raw_data)
    return events

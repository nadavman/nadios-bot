from nadios_bot.consts import Places
from nadios_bot.scarping_handlers.barby_handler import get_barby_events
from nadios_bot.scarping_handlers.yellow_submarine_handler import get_yellow_submarine_events

HANDLERS = {
    Places.BARBY.name: get_barby_events,
    Places.YELLOW_SUBMARINE.name: get_yellow_submarine_events
}
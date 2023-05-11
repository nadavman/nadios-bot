from dotenv import load_dotenv
from enum import Enum
import os

# Environment
load_dotenv()
TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
TELEGRAM_BOT_DATA_FOLDER = os.getenv("TELEGRAM_BOT_DATA_FOLDER", default="/etc/nadios_bot")


# Telegram Replays
class Places(Enum):
    BARBY = 'Barby'
    YELLOW_SUBMARINE = 'Yellow Submarine'


class KeyboardNames(Enum):
    SEE_ALL = "See All Shows"
    SEARCH = "Search"
    REGISTER = "Register For Update"
    BACK = "< Go Back"
    CLOSE = 'X Close'


class StatusEmoji(Enum):
    SHOCKED_FACE = "\U0001F630"
    SMILING_FACE = "\U0001F604"


# Files
LOG_FILE_PATH = os.path.join("/", "var", "log", "nadios_bot", "bot.log")
PREVIOUS_SHOWS_PATH = os.path.join(TELEGRAM_BOT_DATA_FOLDER, "previous_shows.json")
PREVIOUS_SHOWS_DEFAULT_VALUE = {}
REGISTERED_USERS_PATH = os.path.join(TELEGRAM_BOT_DATA_FOLDER, "registered_users.json")
REGISTERED_USERS_DEFAULT_VALUE = []
# Scrap
BARBY_URL = "https://www.barby.co.il/"
YELLOW_SUBMARINE_URL = "https://yellowsubmarine.org.il/event/"

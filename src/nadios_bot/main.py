from nadios_bot.consts import TELEGRAM_BOT_API_KEY, PREVIOUS_SHOWS_PATH, \
    REGISTERED_USERS_PATH, REGISTERED_USERS_DEFAULT_VALUE, LOG_FILE_PATH
from nadios_bot.telegram_utils import run_bot, get_all_events, save_events
from logging.handlers import RotatingFileHandler
import logging
import json
import os


class MissingEnvironmentVariable(Exception):
    pass


def setup_data_file(file_path, file_default_data):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(file_default_data, f)


def setup():
    logging.info("Running Setup")
    if TELEGRAM_BOT_API_KEY is None:
        raise MissingEnvironmentVariable(f"TELEGRAM_BOT_API_KEY does not exist")
    if not os.path.exists(PREVIOUS_SHOWS_PATH):
        save_events(get_all_events())
    setup_data_file(file_path=REGISTERED_USERS_PATH, file_default_data=REGISTERED_USERS_DEFAULT_VALUE)


def main():
    logging.basicConfig(
        format='[%(levelname)-8s] %(asctime)s: %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            RotatingFileHandler(LOG_FILE_PATH, maxBytes=1000000, backupCount=4),
            logging.StreamHandler()
        ])
    try:
        setup()
        run_bot()
    except Exception as e:
        logging.exception("Oh no!")
        raise e


if __name__ == "__main__":
    main()

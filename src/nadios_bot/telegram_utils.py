from nadios_bot.consts import TELEGRAM_BOT_API_KEY, PREVIOUS_SHOWS_PATH, REGISTERED_USERS_PATH, KeyboardNames, Places
from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from nadios_bot.scarping_handlers import HANDLERS
from nadios_bot.data_structures import Event
from threading import Thread
from typing import List, Dict
from time import sleep
import schedule
import logging
import telebot
import json

bot = telebot.TeleBot(TELEGRAM_BOT_API_KEY)


def get_registered_users() -> List[str]:
    with open(REGISTERED_USERS_PATH, 'r') as f:
        return json.load(f)


def add_registered_users(new_user_id: int) -> bool:
    users = get_registered_users()
    if str(new_user_id) in users:
        logging.info(f"User {new_user_id} already on registered users!")
        return False
    users.append(str(new_user_id))
    with open(REGISTERED_USERS_PATH, 'w') as f:
        json.dump(users, f)
    logging.info(f"User {new_user_id} was added to registered users!")
    return True


def get_all_events() -> Dict[str, List[Event]]:
    all_events = {}
    for place in Places:
        all_events[place.name] = HANDLERS[place.name]()
    return all_events


def save_events(all_events: Dict[str, List[Event]]) -> None:
    events_text_format = {}
    for place, events in all_events.items():
        events_text_format[place] = [event.short_title() for event in events]
    with open(PREVIOUS_SHOWS_PATH, 'w') as f:
        json.dump(events_text_format, f)


def get_new_events(current_events: List[Event], prev_events: List[Event]) -> List[Event]:
    new_events = []
    for event in current_events:
        if event.short_title() not in prev_events:
            new_events.append(event)
    return new_events


def send_update_for_specific_place(place_name: str, new_events: List[Event]):
    new_events_as_text = [f"*We've found new shows at {place_name}*:"]
    new_events_as_text += [event.long_title() for event in new_events]
    new_events_as_text = "\n\n".join(new_events_as_text)
    for user_id in get_registered_users():
        logging.info(f"Trying to update user {user_id} for shows at {place_name}")
        bot.send_message(chat_id=user_id, text=new_events_as_text, parse_mode='Markdown')


def send_update_for_new_events() -> None:
    with open(PREVIOUS_SHOWS_PATH, 'r') as f:
        all_prev_events = json.load(f)
    all_current_events = get_all_events()
    for place in Places:
        new_events = get_new_events(current_events=all_current_events[place.name],
                                    prev_events=all_prev_events.get(place.name, []))
        logging.info(f"Find {len(new_events)} new events at {place.value}!")
        if new_events:
            send_update_for_specific_place(place_name=place.value, new_events=new_events)
    save_events(all_events=all_current_events)


def main_menu() -> InlineKeyboardMarkup:
    menu = [[InlineKeyboardButton(keyboard.value, callback_data=keyboard.name)]
            for keyboard in KeyboardNames
            if keyboard != KeyboardNames.BACK]
    return InlineKeyboardMarkup(menu)


def see_all_menu() -> InlineKeyboardMarkup:
    menu = [[InlineKeyboardButton(place.value, callback_data=place.name)] for place in Places]
    menu.append([InlineKeyboardButton(KeyboardNames.BACK.value, callback_data=KeyboardNames.BACK.name)])
    return InlineKeyboardMarkup(menu)


def specific_place_menu(place_name: str) -> InlineKeyboardMarkup:
    keyboard = []
    for event in HANDLERS[place_name]():
        if not event.is_soldout():
            keyboard.append([InlineKeyboardButton(event.menu_title(), url=event.url)])
    keyboard.append([InlineKeyboardButton(KeyboardNames.BACK.value, callback_data=KeyboardNames.BACK.name)])
    return InlineKeyboardMarkup(keyboard)


@bot.message_handler(commands=["Hola"])
def hola(message: Message):
    bot.reply_to(message, "Hola Amigo!")


@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(message.chat.id, "What can I do for you?", reply_markup=main_menu(), parse_mode='Markdown')


def search_show(message: Message):
    search_query = message.text
    relevant_events = []
    for events in get_all_events().values():
        relevant_events.extend(filter(lambda event: search_query in event.name, events))
    relevant_events.sort(key=lambda event: event.date)
    respond = "\n\n".join([event.long_title() for event in relevant_events]) \
        if relevant_events else "Can't fine any shows :("
    bot.send_message(message.chat.id, respond)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    match call.data:
        case KeyboardNames.SEE_ALL.name:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=see_all_menu())

        case place if place in [place.name for place in Places]:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=specific_place_menu(place))

        case KeyboardNames.SEARCH.name:
            search_query = bot.send_message(call.message.chat.id, "What shows are we looking for today?")
            bot.register_next_step_handler(search_query, search_show)

        case KeyboardNames.REGISTER.name:
            is_succeed = add_registered_users(call.message.chat.id)
            respond = "Successfully registered!" if is_succeed else "Already registered!"
            bot.edit_message_text(text=respond,
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)

        case KeyboardNames.BACK.name:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=main_menu())

        case _:
            bot.edit_message_text(text="See you soon!",
                                  chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def run_bot():
    logging.info("Starting bot!")
    schedule.every(15).minutes.do(send_update_for_new_events)
    Thread(target=schedule_checker).start()
    bot.polling(none_stop=True, timeout=90)

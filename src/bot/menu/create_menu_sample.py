from telebot import types
from src import config
from src.bot.actions.get_data_cars import get_category_list

logger = config.logger

def choose_category(message):
    logger.info(message)
    return {
        "message": "Выберите категорию: ",
        "keyboard": keyboard_generator(get_category_list())
    }


def keyboard_generator(keys):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for item in keys:
        keyboard.add(types.InlineKeyboardButton(text=item, callback_data=item))
    return keyboard


def choose_reports(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text="Итоговый за неделю", callback_data="final_report"),
                types.InlineKeyboardButton(text="Подробный за неделю", callback_data="detailed_report"),
                types.InlineKeyboardButton(text="Сотрудники", callback_data="get_all_users"),
                types.InlineKeyboardButton(text="Добавить машину", callback_data="add_new_car"))


    logger.info(message)
    return {"message": "Выберите действие: ",
            "keyboard": keyboard
            }

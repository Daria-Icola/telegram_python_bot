import os
from src import config
import telebot
from src.bot.menu.create_menu_sample import choose_category, keyboard_generator, choose_reports
from src.bot.actions.get_data_cars import get_brands_list, get_category_list, get_numbers_list, get_models_list, get_car_info, \
    add_ride, update_kms
from src.bot.actions.get_reports import register_user, update_user_data, get_user, get_employees, delete_car_by_num, get_all_numbers
from src.bot.utils.validators import km_validation
from src.bot.utils.utils import generate_log_message
from src.libs.excel import Excel

logger = config.logger
bot = telebot.TeleBot(config.telegram["token"])
choosed = {}
user_data = {}

# Constants to indicate steps while user is entering password
TEAM_USER_LOGGING = 0
TEAM_USER_ACCEPTED = 1

USER_GET_FULLNAME = 0
USER_ACCEPT_FULLNAME = 1
USER_ADD_FULLNAME = 2
user_get_fullname = {}


STATUS_ADD_KM_CURRENT = 0
STATUS_ADD_KM_END = 1
user_add_step = {}


user_step = {}
excel = Excel()

# Функция отлавливает состояние когда строка в списке user_step = TEAM_USERS_LOGIN
@bot.message_handler(func=lambda message: user_step.get(message.chat.id) == TEAM_USER_LOGGING)
def team_user_login(message):

    if not user_data.get(message.chat.id):
        user_data[message.chat.id] = {
            'telegram_id': message.from_user.id,
            'telegram_login': message.from_user.username,
            'first_name': message.from_user.first_name
        }

    pwd_counter = user_data.get(message.chat.id).get("password_counter")
    if pwd_counter is None:
        user_data[message.chat.id].update({'password_counter': 1})


    # если пароль водителей, то записать данные с ролью водитель
    if message.text == config.telegram["driver_password"]:
        user_data[message.chat.id].update({'role': 'Водитель'})
        # Обновляем данные пользователя в таблице users
        update_user_data(None, user_data[message.chat.id].get("role"), user_data[message.chat.id].get("telegram_id"))
        logger.info('INFO: ', user_data[message.chat.id])
        # добавляем в список пользователей-водителей
        user_step[message.chat.id] = TEAM_USER_ACCEPTED
        # функция получения ФИО от пользователя
        get_fullname(message)
        return

    # если пароль менеджера, то записать данные с ролью менеджер
    if message.text == config.telegram["manager_password"]:
        # получаем данные от пользователя
        user_data[message.chat.id].update({'role': 'Менеджер'})
        # Обновляем данные пользователя в таблице users
        update_user_data(user_data[message.chat.id].get(""), user_data[message.chat.id].get("role"), user_data[message.chat.id].get("telegram_id"))
        logger.info('INFO', user_data[message.chat.id])
        # добавляем в список пользователей-менеджеров
        user_step[message.chat.id] = TEAM_USER_ACCEPTED
        # функция получения ФИО от пользователя
        get_fullname(message)
        return

    pwd_counter = user_data.get(message.chat.id).get("password_counter")
    # if message.text != config.telegram["driver_password"] or message.text != config.telegram["manager_password"]:
    #     user_data[message.chat.id] = {'password_counter': 1}

    if pwd_counter:
        if user_data.get(message.chat.id) and int(pwd_counter) < 3:
            user_data[message.chat.id]["password_counter"] += 1
            logger.info(user_data)
            bot.send_message(message.chat.id, "Пароль введён неверно")
            return

        if user_data.get(message.chat.id) and pwd_counter and int(pwd_counter) == 3:
            logger.info(user_data)
            bot.send_message(message.chat.id, "Лимит ввода пароля прeвышен. Обратитесь к менеджеру")
            return



@bot.message_handler(commands=["start"])
def start_message(message):
    logger.info(generate_log_message(message))
    user = get_user(message.from_user.id)
    if user:
        user_data[message.chat.id] = user
        if not user.get('role'):
            user_step[message.chat.id] = TEAM_USER_LOGGING
            bot.send_message(message.chat.id, "Введите пароль: ")
            return
        if not user.get('fullname'):
            bot.send_message(message.chat.id, "Введите Фамилию Имя Отчество: ")
            user_get_fullname[message.chat.id] = USER_ACCEPT_FULLNAME
            return
        # если айди пользователя сохранен с ролью менеджер
        if user.get('role') == 'Менеджер':
            bot.send_message(message.chat.id, 'Выберите роль:', reply_markup=keyboard_generator(["Водитель", "Менеджер"]))
            logger.info("Open menu: choose role")
            return
        # если айди пользователя сохранен с ролью водитель
        if user.get('role') == 'Водитель':
            bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=keyboard_generator(get_category_list()))
            logger.info("Open menu: choose category")
            return

        # иначе запомни человека(id, firstname, login) и запроси пароль
    if not user:
        user_step[message.chat.id] = TEAM_USER_LOGGING
        register_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
        logger.info("Registration user: Success")
        bot.send_message(message.chat.id, "Введите пароль: ")
        return


@bot.message_handler(commands=["help"])
def start_message(message):
    bot.send_message(message.chat.id, """Инструкция по работе с ботом:

❗️ВАЖНО:
При первом вызове команды, бот запросит пароль и ваше ФИО.📝
Пожалуйста, указывайте настоящие данные❗️

Если вы заметили ошибку после отправки, не беспокойтесь. 
📍"Подтверждение" сохраняет внесенные данные ✅
📍"Назад" возвращает возможность ввести ФИО 🔙
Бот вас запомнит, и в дальнейшем,
вводить информацию не потребуется.

После авторизации вам будет предложен выбор категории автомобиля, марки, модели и номера.
Данные автомобиля, в том числе и текущий пробег, выведутся автоматически.

📍 "Добавить поездку" сохраняет выбранный автомобиль
и дает возможность ввести пробег ✔️
📍 "Отмена" возвращает возможность выбрать автомобиль
начиная с категории 🔙

❗️Проверяйте достоверность информации
В случае расхождения данных сообщите менеджеру 📩

Формат ввода километража 111111.
Если километраж подходит под требования - он обновится,
иначе, бот предупредит вас об этом 🔍

Для следующей поездки вы можете нажать на
📍 Кнопку "Новая поездка"
📍 /start
""")

def validation_user(message):
    # Кейсс 1: Проверка что роль установлена.
    # Кейс 2: Проверка Водителя что ФИО установлены.
    # Кейс 3: Проверка существования user_data
    # Описать алгоритм валидации юзера, на предмет заполненых полей в БД, и его шаге.
    user = get_user(message.from_user.id)
    if user and not user.get('fullname'):
        bot.send_message(message.chat.id, "Введите Фамилию Имя Отчество: ")
        user_get_fullname[message.chat.id] = USER_ACCEPT_FULLNAME
        return

    if user and not user.get('role'):
        return ''

def get_choosed_category(message):
    bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=keyboard_generator(get_category_list()))
    logger.info('INFO: get_choosed_category', user_data[message.chat.id])
    #  return user_data[message.chat.id]


@bot.message_handler(commands=["Добавить поездку"])
def new_km_message(message):
    bot.send_message(message.chat.id, "Введите новый пробег: ")
    user_add_step[message.chat.id] = STATUS_ADD_KM_CURRENT


@bot.message_handler(func=lambda message: user_get_fullname.get(message.chat.id) == USER_GET_FULLNAME)
def get_fullname(message):
    bot.send_message(message.chat.id, "Введите Фамилию Имя Отчество: ")
    user_get_fullname[message.chat.id] = USER_ACCEPT_FULLNAME
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id - 1,
                          text="Авторизация успешно пройдена")
    return

@bot.message_handler(func=lambda message: user_get_fullname.get(message.chat.id) == USER_ACCEPT_FULLNAME)
def accept_fullname(message):
    bot.send_message(message.chat.id, 'Подтвердите ФИО: ' + message.text, reply_markup=keyboard_generator(["Подтверждаю", "Назад"]))
    try:
        fullname = message.text
        user_data[message.chat.id].update({'fullname': fullname})
        user_get_fullname[message.chat.id] = None
    except Exception as error:
        logger.error('ERROR accept: ', error)


# @bot.message_handler(func=lambda message: user_get_fullname.get(message.chat.id) == USER_ADD_FULLNAME)
def add_fullname(message):
    try:
        update_user_data(user_data[message.chat.id].get("fullname"), user_data[message.chat.id].get("role"),
                         user_data[message.chat.id].get("telegram_id"))
    except Exception as error:
        logger.error("ERROR add fullname: ", error)


@bot.message_handler(func=lambda message: user_add_step.get(message.chat.id) == STATUS_ADD_KM_CURRENT)
def adding_kms(message): # Название функции не играет никакой роли
    km_end = message.text
    logger.info(km_end)
    if km_validation(km_end):
        km_current = get_car_info(user_data[message.chat.id].get('number')).get('km')

        if int(km_current) < int(km_end) or user_data[message.chat.id].get('role') == 'Менеджер':
            if not user_data[message.chat.id].get('fullname'):
                bot.send_message(message.chat.id, "Введите Ваше ФИО:")
                user_get_fullname[message.chat.id] = USER_ACCEPT_FULLNAME

            user_data[message.chat.id].update({'km_current': km_current})
            user_data[message.chat.id].update({'km_end': km_end})

            try:
                res = add_ride(user_data[message.chat.id].get('category'), user_data[message.chat.id].get('number'),
                               user_data[message.chat.id].get('brands'), user_data[message.chat.id].get('models'), user_data[message.chat.id].get('km_current'),
                               user_data[message.chat.id].get('km_end'), user_data[message.chat.id].get('fullname'),)

                bot.send_message(message.chat.id, 'Пробег обновлён',
                                 reply_markup=keyboard_generator(['Новая поездка']))

                update_kms(user_data[message.chat.id].get('number'), user_data[message.chat.id].get('km_end'))
                user_add_step[message.chat.id] = STATUS_ADD_KM_END
                return res

            except Exception as error:
                logger.error(error)

                bot.send_message(message.chat.id, 'Не удалось сохранить пробег')
                new_km_message(message)

        else:
            bot.send_message(message.chat.id, 'Введённый пробег не действителен.  Новый пробег должен быть больше нынешнего.')
            new_km_message(message)

    else:
        bot.send_message(message.chat.id, 'Некорректный формат пробега. Попробуйте ещё раз')
        new_km_message()




@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # validation_user(call.message)

    # Если сообщение из чата с ботом
    if call.message:
        if call.data == 'Менеджер':
            # Отправить меню с выбором отчета
            choosed_reports = choose_reports(call.message)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=choosed_reports["message"],
                                  reply_markup=choosed_reports["keyboard"])
            return

        if call.data == 'Водитель':
            # Отправить меню с выбором категории авто
            choosed_category = choose_category(call.message)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=choosed_category["message"],
                                  reply_markup=choosed_category["keyboard"])
            return

        if call.data in get_category_list() and user_data[call.message.chat.id]:
            user_data[call.message.chat.id].update({'category': call.data})
            brand_list = get_brands_list(call.data)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Выберите марку',
                                  reply_markup=keyboard_generator(brand_list))
            return
        if call.data in get_brands_list(user_data.get(call.message.chat.id).get('category')):
            user_data[call.message.chat.id].update({'brands': call.data})
            model_list = get_models_list(user_data[call.message.chat.id]['brands'], user_data[call.message.chat.id]['category'])
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Выберите модель:',
                                  reply_markup=keyboard_generator(model_list))
            return
        if user_data.get(call.message.chat.id).get('brands') and call.data in get_models_list(user_data[call.message.chat.id]['brands'], user_data[call.message.chat.id]['category']):
            user_data[call.message.chat.id].update({'models': call.data})
            number_list = get_numbers_list(user_data[call.message.chat.id]['models'])
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Номер автомобиля:',
                                  reply_markup=keyboard_generator(number_list))
            return
        if user_data.get(call.message.chat.id).get('models') and call.data in get_numbers_list(user_data[call.message.chat.id]['models']):
            user_data[call.message.chat.id].update({'number': call.data})
            number_list = get_numbers_list(user_data[call.message.chat.id]['models'])
            car_info = get_car_info(user_data[call.message.chat.id].get('number'))
            message = f"Информациця об авто:\nКатегория: {car_info.get('car_category')}\nМарка: {car_info.get('brand')}\nМодель: {car_info.get('model')}\nНомер: {car_info.get('number')}\nПробег: {car_info.get('km')}км"
            buttons = ["Добавить поездку", "Отмена"]
            if user_data[call.message.chat.id].get('role') == 'Менеджер':
                buttons += ["Удалить"]
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=message,
                                  reply_markup=keyboard_generator(buttons))
            return

        if call.data == 'Добавить поездку':
            new_km_message(call.message)
            car_info = get_car_info(user_data[call.message.chat.id].get('number'))
            info_message = f"Информациця об авто:\nКатегория: {car_info.get('car_category')}\nМарка: {car_info.get('brand')}\nМодель: {car_info.get('model')}\nНомер: {car_info.get('number')}\nПробег: {car_info.get('km')}км"
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=info_message)
            return

        if call.data == 'Удалить':
            print(user_data[call.message.chat.id].get('number'))
            car_info = get_car_info(user_data[call.message.chat.id].get('number'))
            delete_car_by_num(user_data[call.message.chat.id].get('number'))
            all_numbers = get_all_numbers()
            if user_data[call.message.chat.id].get('number') not in all_numbers:
                info_message = f"Автомобиль удален:\nМарка: {car_info.get('brand')}\nМодель: {car_info.get('model')}\nНомер: {car_info.get('number')}\nПробег: {car_info.get('km')}км"
            else:
                info_message = f"Ошибка в удалении автомобиля:\nМарка: {car_info.get('brand')}\nМодель: {car_info.get('model')}\nНомер: {car_info.get('number')}\n"
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=info_message)
            return

        if call.data == 'Отмена' or call.data == 'Новая поездка':
            choosed_category = choose_category(call.message)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=choosed_category["message"],
                                  reply_markup=choosed_category["keyboard"])

        if call.data == "Назад":
            bot.delete_message(chat_id=call.message.chat.id,
                                message_id=call.message.message_id)
            get_fullname(call.message)
            user_get_fullname[call.message.chat.id] = USER_GET_FULLNAME
            return

        if call.data == "Подтверждаю":
            # TODO FULLNAME
            add_fullname(call.message)
            if user_data[call.message.chat.id].get("role") == 'Водитель':
                choosed_category = choose_category(call.message)
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=choosed_category["message"],
                                      reply_markup=choosed_category["keyboard"])
                return

            elif user_data[call.message.chat.id].get("role") == 'Менеджер':

                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text='Выберите роль:',
                                      reply_markup=keyboard_generator(["Водитель", "Менеджер"]))
                return

        # Финальный отчет с текущем км за неделю. изменения применяются после нахатии на кнопку Недельный отчет отчет
        if call.data == 'final_report':
            try:
                document = excel.set_car_km()
                doc = open(document, 'rb')
                bot.send_document(call.message.chat.id, doc)
            except Exception as error:
                logger.error(f"ERROR!: {error}")
            return

        # Детальный отчет со всеми поездками, совешенными за неделю. изменения применяются после нахатии на кнопку Подробный отчет
        if call.data == 'detailed_report':
            try:
                document = excel.create_detail_report()
                doc = open(document, 'rb')
                bot.send_document(call.message.chat.id, doc)
            except Exception as error:
                logger.error("ERROR!: ", error)
            return

        # Получение списка всех зарегистрированных пользователей
        if call.data == 'get_all_users':
            try:
                all_emloyees = get_employees()
                message = '<code>'
                for employee in all_emloyees:
                    message += f'- {employee}'
                message += '</code>'
                return bot.send_message(call.message.chat.id, message, parse_mode='html')
            except Exception as error:
                logger.error(f"Не удалось получить пользователей: {error}")
            return

        if call.data == 'add_new_car':
            try:
                bot.send_message(call.message.chat.id, "Введите данные автомобиля, которые нужно добавить:")


            except Exception as error:
                logger.error(f"Не удалось добавить автомобиль с : {error}")





if __name__ == '__main__':
     bot.infinity_polling()

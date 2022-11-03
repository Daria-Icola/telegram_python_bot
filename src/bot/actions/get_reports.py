from src.config import database, logger
from src.libs.database import Database
from datetime import date
from src.bot.actions.get_data_cars import get_car_info

logger = logger
today = date.today()
database = Database(database["db_user"],
                    database["db_password"],
                    database["db"],
                    database["host"],
                    database["port"])


def get_all_numbers():
    result = database.get_all_numbers()

    all_numbers = []
    for item in result:
        all_numbers.append(item[0])

    return all_numbers


def get_report_by_car_number(number):
    car = get_car_info(number)
    date = today.strftime("%d.%m.%Y")
    pass


#вернёт список пользователей
def get_all_users():
    try:
        result = database.get_all_users()
        all_employees = []
        for item in result:
            all_employees.append(item)

        return all_employees
    except Exception as error:
        logger.error(error)


#вернёт список водителей
def get_all_users_id():
    try:
        result = database.get_all_users_id()
        all_employees = []
        for item in result:
            all_employees.append(item)

        return all_employees
    except Exception as error:
        logger.error(error)


#находит водителя по telegram_id
def get_user(telegram_id):
    response = database.get_user_by_id(telegram_id)
    if response:
        try:
            user = list(response[0])
            keys = ["id", "telegram_login", "fullname", "telegram_firstname", "telegram_id", "role"]
            employee_info = dict(zip(keys, user))
            logger.info(employee_info)
            return employee_info
        except Exception as error:
            logger.error(error)


def get_user_role_by_id(telegram_id):
    try:
        user_role = database.get_role_by_id(telegram_id)
        return user_role
    except Exception as error:
        logger.error(error)


def get_users_furllname_and_roles():
    try:
        users = database.get_all_users_fullname_and_roles()
        return users
    except Exception as error:
        logger.error(f"Ошибка в получении ФИО и роли: {error}")


def register_user(telegram_id, login, telegram_username):
    try:
        user = database.insert_to_users(telegram_id, login, telegram_username)
        return user
    except Exception as error:
        logger.error(f"Ошибка в регистрации пользователя: {error}")


def add_new_ride(car_category, number, brand, model, km_current, km_end, fullname):
    try:
        ride = database.insert_to_rides(car_category, number, brand, model, km_current, km_end, fullname)
        logger.info(f"Add new Ride: {car_category}, {number}, {brand}, {model}, {km_current}, {km_end}, {fullname}")
        return ride
    except Exception as error:
        logger.error(f"Ошибка в обновлении данных пользователя: {error}")


def update_user_data(fullname, role, telegram_id):
    try:
        logger.info(f"Update_user: {fullname}, {role}, {telegram_id}")
        return database.update_user(fullname, role, telegram_id)
    except Exception as error:
        logger.error(f"Ошибка в обновлении данных пользователя: {error}")


def delete_car_by_num(number):
    try:
        print(number)
        logger.info(f"Delete_car: {number}")
        return database.delete_car(number)
    except Exception as error:
        logger.error(f"Ошибка в удалении автомобиля: {error}")


def dict_for_detail_report():
    detailed_report = database.get_rides_week()
    rides = []
    for ride in detailed_report:
        try:
            result = list(ride)
            keys = ['id', 'car_category', 'car_number', 'car_brand',
                'car_model','km_start', 'km_end', 'fullname', 'ride_date']
            car_info = dict(zip(keys, result))
            rides.append(car_info)
        except Exception as error:
            logger.error("dict_for_detail_report error: ", error)
    logger.info(rides)
    return rides


def dict_for_final_report():
    rides = database.get_numbers_and_kms()
    final_car_info = []
    for ride in rides:
        try:
            result = list(ride)
            keys = ['number', 'km_end']
            car_info = dict(zip(keys, result))
            logger.info("CAR INFO: ", car_info)
            final_car_info.append(car_info)
        except Exception as error:
            logger.error("dict_for_final_report error: ", error)
    logger.info(final_car_info)
    return final_car_info


def get_employees():
    try:
        employees = database.get_all_users_fullname_and_roles()
        all = []
        for employee in employees:
            info = employee[0] + ' ' + employee[1] + '\n'
            all.append(info)
        logger.info(f'get_emloyees: {all}')
        return all
    except Exception as error:
        logger.error("get_employees error: ", error)



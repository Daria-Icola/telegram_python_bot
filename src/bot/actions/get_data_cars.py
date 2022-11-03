from src import config
from src.libs.database import Database

logger = config.logger
database = Database(config.database["db_user"],
                    config.database["db_password"],
                    config.database["db"],
                    config.database["host"],
                    config.database["port"])


def get_category_list():
    response = database.get_car_category()
    category_list = []
    for item in response:
        try:
            category_list.append(item[0])
        except Exception as error:
            logger.error(error)
    return category_list


def get_brands_list(car_categories):
    result = database.get_brands_by_category(car_categories)
    brands = []
    for item in result:
        try:
            brands.append(item[0])
        except Exception as error:
            logger.error(error)
    return brands


def get_models_list(brand, car_category):
    result = database.get_models_by_brand(brand, car_category)
    models = []
    for item in result:
        try:
            models.append(item[0])
        except Exception as error:
            logger.error(error)
    return models


def get_numbers_list(model):
    result = database.get_numbers_by_model(model)

    numbers = []
    for item in result:
        try:
            numbers.append(item[0])
        except Exception as error:
            logger.error(error)
    return numbers


def get_car_info(number):
    try:
        result = list(database.get_car_info(number)[0])
        keys = ["id", "car_category", "number", "brand", "model", "km"]
        car_info = dict(zip(keys, result))
        return car_info
    except Exception as error:
        logger.error(error)


def get_all_numbers():
    result = database.get_all_numbers()

    all_numbers = []
    for item in result:
        try:
            all_numbers.append(item[0])
        except Exception as error:
            logger.error(error)
    return all_numbers

def add_ride(car_category, number, brand, model, km_current, km_end, fullname):
    try:
        # print(f"adding: car_category:{car_category}, number:{number},brand:{brand},model:{model},km_current:{km_current},km_end:{km_end}fullname:{fullname},")
        return database.insert_to_rides(car_category, number, brand, model, km_current, km_end, fullname)
    except Exception as error:
        logger.error(error)


def update_kms(number, km):
    try:
        return database.update_km(number, km)
    except Exception as error:
        logger.error(error)

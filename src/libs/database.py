import psycopg2
from src import config

logger = config.logger

class Database:
    def __init__(self, user, password, database, host, port):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

    def connect(self):
        logger.info(f'Try connect to ip:{self.host}, port:{self.port}, db_name:{self.database}, user:{self.user}, pwd:{self.password}')
        try:
            conn = psycopg2.connect(database=self.database, user=self.user, password=self.password,
                                 host=self.host, port=self.port)
            logger.info(f"connection success! {conn}")
            return conn
        except psycopg2.Error as error:
            logger.error(error)
            #return "Ошибка соденинения с базой данных, свяжитесь с администратором."


    def send_query(self, query, params=None, many=None):
        print(query, params)
        #conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        conn = self.connect()
        print(conn)
        cur = conn.cursor()
        logger.info(f"{query} {params}")
        if params:
            try:
                cur.execute(query, params)
                response = cur.fetchall()
                logger.info(f"Response data: {response}")
                return response
            except psycopg2.Error as error:
                logger.error(f"Response error: {error}")
        else:
            try:
                cur.execute(query)
                response = cur.fetchall()
                logger.info(f"Response data: {response}")
                return response
            except psycopg2.Error as error:
                logger.error(f"Response error: {error}")

    def send_query_to_insert(self, query, params):
        try:
            #conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
            conn = self.connect()
            cur = conn.cursor()
            execute = cur.execute(query, params)
            conn.commit()
            return execute
        except Exception as error:
            logger.error(f"Response error: {error}")


    # FOR CARS
    # Get car's category
    def get_car_category(self):

        return self.send_query("SELECT DISTINCT(car_category) FROM cars")

    # Get brand's by category
    def get_brands_by_category(self, car_category):
        logger.info(f"get_brands_by_category: {car_category}")
        return self.send_query("SELECT DISTINCT(brand) FROM cars WHERE car_category=%s", (car_category,))


    # Get model's by brands
    def get_models_by_brand(self, brand, car_category):
        logger.info(f"get_model_by_brand: {brand} {car_category}")
        return self.send_query("SELECT DISTINCT(Model) FROM cars WHERE brand=%s and car_category=%s", (brand, car_category))


    # Get numbers's by models
    def get_numbers_by_model(self, model):
        logger.info(f"get_numbers_by_model: {model}")
        return self.send_query('SELECT DISTINCT(Number) FROM cars WHERE model=%s', (model,))

    def get_car_info(self, number):
        logger.info(f"get_car_info: {number}")
        return self.send_query('SELECT * FROM cars WHERE number=%s', (number,))

    def get_all_numbers(self):
        return self.send_query('SELECT DISTINCT(Number) FROM cars')

    # FOR DRIVERS
    def add_driver_fullinfo(self, telegram_username, fullname, telegram_id):
        logger.info(f"add_driver_fullinfo: {telegram_username}, {fullname}. {telegram_id}")
        return self.send_query('INSERT INTO users telegram_username=%s, fullname=%s, telegram_id=%s', (telegram_username, fullname, telegram_id))

    def get_all_users_fullname_and_roles(self):
        return self.send_query('SELECT fullname, role FROM users ')

    def get_all_users(self):
        return self.send_query('SELECT * FROM users')

    def get_all_users_id(self):
        return self.send_query('SELECT DISTINCT(telegram_id) FROM users')

    def get_employee_by_fullname(self, fullname):
        logger.info(f"get_employee_by_fullname: {fullname}")
        return self.send_query('SELECT * FROM users WHERE fullname=%s', (fullname,))

    def get_user_by_id(self, id):
        logger.info(f"get_user_by_id: {id}")
        return self.send_query('SELECT * FROM users WHERE telegram_id=%s', (id,))

    def get_role_by_id(self, id):
        logger.info(f"get_role_by_id: {id}")
        return self.send_query('SELECT role FROM users WHERE telegram_id=%s', (id,))

    # For Rides
    def get_all_rides(self):
        return self.send_query('SELECT * FROM rides')

    def get_numbers_and_km(self):
        return self.send_query('SELECT number, km_end FROM rides')

    def get_numbers_and_kms(self):
        return self.send_query('SELECT number, km FROM cars')

    def insert_to_rides(self, car_category, number, brand, model, km_current, km_end, fullname):
        logger.info(f"insert_to_rides: {car_category}, {number}, {brand}, {model}, {km_current}, {km_end}, {fullname}")
        return self.send_query_to_insert("INSERT INTO rides (car_category, number, brand, model, km_current, km_end, fullname) VALUES (%s,%s,%s,%s,%s,%s,%s)", (car_category, number, brand, model, km_current, km_end, fullname))

    def insert_to_users(self, telegram_id, telegram_login, firstname):
        logger.info(f"insert_to_user: {telegram_id}, {telegram_login}, {firstname}")
        return self.send_query_to_insert('INSERT INTO users(telegram_id, telegram_login, firstname) VALUES(%s,%s,%s)', (telegram_id, telegram_login, firstname))

    def update_user(self, fullname, role, telegram_id):
        logger.info(f"update_user: {telegram_id}, {fullname}, {role}")
        return self.send_query_to_insert('UPDATE users SET fullname=%s, role=%s WHERE telegram_id=%s', (fullname, role, telegram_id,))

    def update_km(self, number, km):
        logger.info(f"insert_to_user: {number}, {km}")
        return self.send_query_to_insert('UPDATE cars SET km=%s WHERE number=%s', (km, number,))

    def get_rides_week(self):
        return self.send_query('SELECT * FROM rides WHERE date BETWEEN current_date - 7 AND current_date')

    def delete_car(self, number):
        logger.info(f"delete_car: {number}")
        return self.send_query_to_insert('DELETE FROM cars WHERE number=%s', (number,))



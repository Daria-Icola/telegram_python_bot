import psycopg2
from src import config


def connect_data(db_user, db_password, host, port, db):
    return psycopg2.connect(user=db_user, password=db_password, host=host, port=port, database=db)


def create_table_cars(db_user, db_password, host, port, db):
    conn = connect_data(db_user, db_password, host, port, db)
    cur = conn.cursor()

    create_cars_table = '''CREATE TABLE cars(
            ID SERIAL PRIMARY KEY,
            CAR_CATEGORY TEXT NOT NULL,
            NUMBER TEXT NOT NULL,
            BRAND TEXT NOT NULL,
            MODEL TEXT NOT NULL,
            KM INT)
            '''
    cur.execute(create_cars_table)
    conn.commit()

    cur.close()
    conn.close()


def create_table_users(db_user, db_password, host, port, db):
    conn = connect_data(db_user, db_password, host, port, db)
    cur = conn.cursor()

    create_users_table = '''CREATE TABLE users(
            ID SERIAL,
            TELEGRAM_LOGIN TEXT,
            FULLNAME TEXT,
            FIRSTNAME TEXT,
            TELEGRAM_ID INT PRIMARY KEY,
            ROLE TEXT
            )
            '''
    cur.execute(create_users_table)
    conn.commit()

    cur.close()
    conn.close()


def update_table_data(db_user, db_password, host, port, db):
    conn = connect_data(db_user, db_password, host, port, db)
    cur = conn.cursor()
    update_table = '''ALTER TABLE users ALTER COLUMN telegram_id TYPE BIGINT'''
    cur.execute(update_table)
    conn.commit()

    cur.close()
    conn.close()



def create_table_rides(db_user, db_password, host, port, db):
    conn = connect_data(db_user, db_password, host, port, db)
    cur = conn.cursor()

    create_rides_table = '''
            CREATE TABLE rides(
            ID SERIAL PRIMARY KEY,
            CAR_CATEGORY TEXT NOT NULL,
            NUMBER TEXT NOT NULL,
            BRAND TEXT NOT NULL,
            MODEL TEXT NOT NULL,
            KM_CURRENT INT,
            KM_END INT,
            FULLNAME TEXT,
            DATE date not null default CURRENT_DATE
            )
            '''
    cur.execute(create_rides_table)
    conn.commit()

    cur.close()
    conn.close()


def insert_cars(db_user, db_password, host, port, db):
    conn = connect_data(db_user, db_password, host, port, db)
    cur = conn.cursor()
    insert_into_cars = '''
            INSERT INTO cars(car_category, number, brand, model, km) VALUES(%s,%s,%s,%s,%s)
        '''
    cars_info = [("Легковой", "A 001 AA 121'", "Toyota", "Camry", 11196),]
    print("Добавлено")
    cur.executemany(insert_into_cars, cars_info)
    conn.commit()

    cur.close()
    conn.close()


def update_cars(db_user, db_password, host, port, db):
    conn = connect_data(db_user, db_password, host, port, db)
    cur = conn.cursor()
    insert_into_cars = '''
            UPDATE cars SET car_category = 'Легковой', brand = 'Toyota', model = 'Camry', km = '11111' WHERE number = 'A 001 AA 121'
        '''
    cur.execute(insert_into_cars)
    conn.commit()
    print("Обновлено")
    cur.close()
    conn.close()


def update_car_number_by_number(db_user, db_password, host, port, db, old_number, new_number):
    conn = connect_data(db_user, db_password, host, port, db)
    cur = conn.cursor()
    insert_into_cars = f'''
            UPDATE cars SET number='{new_number}' WHERE number = '{old_number}'
        '''
    cur.execute(insert_into_cars)
    conn.commit()
    print("Обновлено")
    cur.close()
    conn.close()


def insert_car_to_cars(db_user, db_password, host, port, db, car_category, number, brand, model, km):
    conn = connect_data(db_user, db_password, host, port, db)
    cur = conn.cursor()
    insert_into_cars = '''
            INSERT INTO cars(car_category, number, brand, model, km) VALUES(%s,%s,%s,%s,%s)
        '''
    car_info = [(car_category, number, brand, model, km)]
    cur.executemany(insert_into_cars, car_info)
    print("Добавлено")
    conn.commit()

    cur.close()
    conn.close()

def delete_car(db_user, db_password, host, port, db, number):
    conn = connect_data(db_user, db_password, host, port, db)
    cur = conn.cursor()
    delete_car = f'''
            DELETE FROM cars WHERE number=%s
        '''
    car_info = [number]
    cur.execute(delete_car, car_info)
    print("Удалено")
    conn.commit()

    cur.close()
    conn.close()



# DROP TABLE
def drop_table(db_user, db_password, host, port, db):
    conn = connect_data(db_user, db_password, host, port, db)
    cur = conn.cursor()
    delete_table_req = '''
                DROP TABLE cars CASCADE
            '''
    cur.execute(delete_table_req)
    conn.commit()

    cur.close()
    conn.close()

# create_table_rides(config.database["db_user"], config.database["db_password"], config.database["host"], config.database["port"], config.database["db"])
# create_table_users(config.database["db_user"], config.database["db_password"], config.database["host"], config.database["port"], config.database["db"])
#create_table_cars(config.database["db_user"], config.database["db_password"], config.database["host"], config.database["port"], config.database["db"])
#insert_cars(config.database["db_user"], config.database["db_password"], config.database["host"], config.database["port"], config.database["db"])

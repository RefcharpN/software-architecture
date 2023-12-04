# Наполнение табоицы visits в постгрес
import random
import psycopg2
from datetime import datetime as DT
from datetime import timedelta
from random import randrange

database_name = "univerity_db"
user_name = "postgres"
password = "12345"
host_ip = "localhost"
host_port ="5432"

connection = psycopg2.connect(
            database = database_name,
            user = user_name,
            password = password,
            host = host_ip,
            port = host_port
)

connection.autocommit = True
cursor = connection.cursor()

def get_date_visit():
    start = DT.strptime('01.09.2022', '%d.%m.%Y')
    end = DT.strptime('22.12.2022', '%d.%m.%Y')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    random_date =  start + timedelta(seconds=random_second)
    random_date = str(random_date)
    return ' '.join(random_date.split(' ')[:-1])

data = [
    (5855, random.choice([True, False]), get_date_visit()),
    (5855, random.choice([True, False]), get_date_visit()),
    (5855, random.choice([True, False]), get_date_visit()),
    (5855, random.choice([True, False]), get_date_visit()),
]
print(data)

visit_records = ", ".join(["%s"] * len(data))

insert_query = (
    f"INSERT INTO visits (student_id,visited,date_visit) VALUES {visit_records}"
)

cursor.execute(insert_query, data)

print("visits table create")
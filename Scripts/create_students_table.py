# Студенты в редис и в постгрес

import redis
from faker import Faker
import string
import random
import psycopg2

redis = redis.Redis(
     host= 'localhost',
     port= '6379')

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


def get_stud_code():
     return random.randint(1000,9999)

fake = Faker('ru_RU')
cursor = connection.cursor()
data = []
for _ in range(3):
    stud_code = get_stud_code()
    fio = fake.name()
    redis.set(stud_code, fio)
    data.append((stud_code,fio))

studens_data = ", ".join(["%s"] * len(data))
insert_query = (f"INSERT INTO students (id_stud_code,fio) VALUES {studens_data}")
cursor.execute(insert_query, data)

print("success create")




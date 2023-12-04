import psycopg2
from faker import Faker
import random

fake = Faker('ru_RU')

database_name = "university_db"
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
# cursor = connection.cursor()
# query = "CREATE DATABASE univerity_db"
# cursor.execute(query)

# create_table_query = """
# CREATE TABLE IF NOT EXISTS visits (
# id SERIAL PRIMARY KEY,
# subject TEXT NOT NULL,
# student TEXT NOT NULL,
# week INTEGER,
# is_visited BOOLEAN
# );
# """

# cursor = connection.cursor()
# cursor.execute(create_table_query)

# наполнение БД

# data = [
#     ("Облачные технологии",fake.name(), random.randint(1,16), random.choice([True, False])),
#     ("Метода системной инженерии",fake.name(), random.randint(1,16), random.choice([True, False])),
#     ("Облачные технологии",fake.name(),  random.randint(1,16), random.choice([True, False])),
#     ("Разработка безопасного ПО",fake.name(),  random.randint(1,16), random.choice([True, False])),
#     ("Философия",fake.name(), random.randint(1,16), random.choice([True, False])),
# ]

# visit_records = ", ".join(["%s"] * len(data))

# insert_query = (
#     f"INSERT INTO visits (subject,student, week, is_visited) VALUES {visit_records}"
# )

# cursor.execute(insert_query, data)
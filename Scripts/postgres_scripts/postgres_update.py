import psycopg2

database_name = "lectures_db"
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

update_query = """
UPDATE
visits
SET
is_visited = False
WHERE
week <= 16
"""

cursor.execute(update_query)

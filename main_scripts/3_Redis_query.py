import psycopg2
import redis


database_name = "smelkin"
user_name = "mireaUser"
password = "2517Pass!Ab0ba"
host_ip = "10.66.66.1"
host_port ="5433"

connection = psycopg2.connect(
            database = database_name,
            user = user_name,
            password = password,
            host = host_ip,
            port = host_port
)

connection.autocommit = True
cursor = connection.cursor()

#3 В Redis (Steudents)
redis = redis.Redis(
     host= '10.66.66.1',
     port= '6379',
     db=1)

query_for_redis = ("SELECT id_stud_code,fio FROM public.students;")
cursor.execute(query_for_redis)
result=cursor.fetchall()

for i in range(len(result)):
    redis.set(str(result[i][0]),str(result[i][1]))

print("Redis fill")
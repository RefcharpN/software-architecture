from neo4j import GraphDatabase
import psycopg2
import redis

#postgresql
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

# Neo4j
uri = "bolt://10.66.66.1:7687"
userName = "neo4j"
password = "2517Pass"

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))

#Redis
redis = redis.Redis(host= '10.66.66.1', port= '6379', db=1)

#id дисциплин у которых есть специальный тэг
ds_id_array = []

querry_pattern = '''select ds.id from public.disciplines as ds where ds.special_tag is true ;'''
cursor.execute(querry_pattern)
result=cursor.fetchall()
for i in result:
    ds_id_array.append(str(i[0]))

print("выборка из pg - есть спец тэг")
print(ds_id_array)
#TODO:вид свзяи можно было бы сделать специальным

# список: студент группа плановые занятия
stud_gr=[]
with graphDB_Driver.session(database="smelkin") as neo_session:
        stud_gr.append(neo_session.run("match (d:Disciplines)--(l:Lecture)--(tt:TimeTable)--(gr:Group)--(st:Student) where d.iid in $dslist "
                                       "return st.id_stud_code as student_id, gr.name, collect(distinct l.iid)", dslist=(ds_id_array)).data())

stud_gr = stud_gr[0]
print("\nвыборка из neo - набор студентов с группой и набором занятий")
print(stud_gr)

# получение фактического посещения студента
fact_plan_stud = []
stud_list = []

querry_pattern = '''select v.student_id, count(v.visited) from public.visits v where v.student_id in (%s) and v."timeTable_id" in (%s) 
                                                                                        and v.visited is true group by v.student_id ;'''
for i in stud_gr:
    stud_list.append(int(i['student_id']))

cursor.execute(querry_pattern % (','.join(map(str, stud_list)), ','.join(map(str, i['collect(distinct l.iid)']))))
fact_plan_stud.append(cursor.fetchall())

print("\nвыборка из pg - студент с фактическим посещением")
print(fact_plan_stud)

#формирование отчёта
print("\nотчёт:")
for i in stud_gr:

    for obj in fact_plan_stud[0]:
        if obj[0] == int(i['student_id']):
            hours = obj
            break

    querry_pattern = "select g.kurs from public.group g where g.name like '%s'"
    cursor.execute(querry_pattern % ((i['gr.name'])))

    print("группа: " + i['gr.name'] + " №: " + i['student_id'] + " ФИО: " + redis.get(i['student_id']).decode() +
          " курс: " + str(cursor.fetchall()[0][0]) + " зап. часы: " + str(len(i['collect(distinct l.iid)']) * 2)
          + " факт. часы:" + str(hours[1] * 2))



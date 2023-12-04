# -*- coding: utf-8 -*-

from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
import psycopg2
import redis
from neo4j import GraphDatabase

import random
from faker import Faker
from datetime import datetime as DT
from datetime import timedelta
from random import randrange
import codecs
import os


#1 все в Postgres
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
cursor = connection.cursor()

# таблица Институт 2
cursor.execute('''CREATE TABLE public.institute  
    (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(256) COLLATE pg_catalog."default",
    CONSTRAINT institute_pkey PRIMARY KEY (id));''')

institutes_array = ['Институт кибербезопасности и цифровых технологий','Институт искусственного интеллекта']
institute_data = []
for i in range(len(institutes_array)):
    institute_data.append((institutes_array[i]))
institute_values = ", ".join(["(%s)"] * len(institute_data))

query_institute = (f"INSERT INTO public.institute (name) VALUES {institute_values}")
cursor.execute(query_institute, institute_data)

# таблица Кафедра 5
cursor.execute('''CREATE TABLE public.kafedra  
    (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying COLLATE pg_catalog."default",
    institute_id integer,
    CONSTRAINT kafedra_pkey PRIMARY KEY (id),
    CONSTRAINT kafedra_institute_id_fkey FOREIGN KEY (institute_id)
        REFERENCES public.institute (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION);''')

cafedras_array = ['КБ-2','КБ-3','КБ-5']

kafedra_data = []
get_array_institute_id = "SELECT array_agg(id) FROM public.institute"
cursor.execute(get_array_institute_id)
array_ids=cursor.fetchall()

for i in range(len(cafedras_array)):
    # id = random.randint(0,len(array_ids[0][0]))
    # institute_id = array_ids[0][0][id]
    kafedra_data.append((cafedras_array[i], random.randint(1,2)))

kafedra_values = ", ".join(["%s"] * len(kafedra_data))
insert_query = (f"INSERT INTO public.kafedra (name,institute_id) VALUES {kafedra_values}")
cursor.execute(insert_query, kafedra_data)

#Таблица Специальность 5
cursor.execute('''CREATE TABLE public.specialnost  
    (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying COLLATE pg_catalog."default",
    kafedra_id integer,
    CONSTRAINT specialnost_pkey PRIMARY KEY (id),
    CONSTRAINT specialnost_kafedra_id_fkey FOREIGN KEY (kafedra_id)
        REFERENCES public.kafedra (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
    );''')

specialnosts_array = ['Информационные системы и технологии','Информационная безопасность','Системный анализ и управление','Бизнес-информатика','Инноватика',]
# 'Информатика и вычислительная техника','Картография и геоинформатика','Лазерная техника и лазерные технологии','Машиностроение','Менеджмент',
# 'Приборостроение','Программная инженерия','Радиотехника','Статистика','Управление персоналом']

specialnosts_data = []
get_array_kafedra_id = "SELECT array_agg(id) FROM public.kafedra"
cursor.execute(get_array_kafedra_id)
array_ids=cursor.fetchall()

for i in range(len(specialnosts_array)):
    # id = random.randint(0,len(array_ids[0][0])-1)
    # kafedra_id = array_ids[0][0][id]
    specialnosts_data.append((specialnosts_array[i],  random.randint(1,3)))

specialnosts_values = ", ".join(["%s"] * len(specialnosts_data))
insert_query = (f"INSERT INTO public.specialnost (name,kafedra_id) VALUES {specialnosts_values}")
cursor.execute(insert_query, specialnosts_data)


# таблица Группа
cursor.execute('''CREATE TABLE public.group  
    (
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying COLLATE pg_catalog."default",
    kurs integer,
    spec_id integer,
    CONSTRAINT group_pkey PRIMARY KEY (id),
    CONSTRAINT group_spec_id_fkey FOREIGN KEY (spec_id)
        REFERENCES public.specialnost (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
    );''')

groups_array = ['БСБО-01-19','БСБО-02-19','БСБО-03-19','БСБО-04-19','БСБО-05-19','БСБО-06-19']

group_data = []
get_array_spec_id = "SELECT array_agg(id) FROM public.specialnost"
cursor.execute(get_array_spec_id)
array_ids=cursor.fetchall()
for i in range(len(groups_array)):
    id = random.randint(0,len(array_ids[0][0])-1)
    spec_id = array_ids[0][0][id]
    # Группа + рандомный курс от 1 до 4 +spec_id
    group_data.append((groups_array[i], random.randint(1,4),spec_id))
group_values = ", ".join(["%s"] * len(group_data))

query_group = (f"INSERT INTO public.group (name,kurs,spec_id) VALUES {group_values}")
cursor.execute(query_group, group_data)

# таблица Студенты
cursor.execute('''CREATE TABLE public.students
(
    id_stud_code integer NOT NULL,
    fio character varying COLLATE pg_catalog."default",
    group_id integer,
    CONSTRAINT student_pkey PRIMARY KEY (id_stud_code),
    CONSTRAINT student_group_id_fkey FOREIGN KEY (group_id)
        REFERENCES public."group" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);''')

kolvo_students = 100
def get_stud_code():
    return random.randint(1000000,9999999)

fake = Faker('ru_RU')

students_data = []

get_array_group_id = "SELECT array_agg(id) FROM public.group"
cursor.execute(get_array_group_id)
array_ids=cursor.fetchall()

for _ in range(kolvo_students):
    stud_code = get_stud_code()
    fio = fake.name()
    id = random.randint(0,len(array_ids[0][0])-1)
    group_id = array_ids[0][0][id]
    students_data.append((stud_code,fio, group_id))

studens_values = ", ".join(["%s"] * len(students_data))
insert_query = (f"INSERT INTO students (id_stud_code,fio,group_id) VALUES {studens_values}")
cursor.execute(insert_query, students_data)

# таблица Дисциплины 5.
cursor.execute('''CREATE TABLE public.disciplines
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying COLLATE pg_catalog."default",
    check_type character varying COLLATE pg_catalog."default",
    description character varying COLLATE pg_catalog."default",
    tag boolean,
    technical character varying,
    CONSTRAINT disciplines_pkey PRIMARY KEY (id)
);''')

disciplines_array = ['Облачные технологии', 'Алгоритмы компонентов цифровой обработки данных', 
'Методы системной инженерии', 'Проектирование архитектуры программного обеспечения',
'Технологии обеспечения информационной безопасности',]

disciplines_data = []
for i in range(len(disciplines_array)):
    # name + check_type + description + tag
    disciplines_data.append((disciplines_array[i], random.choice(['экзамен','зачет']), 'Описание курса',  random.choice([True, False]),random.choice(['', 'Требуется компьютерный класс'])))
disciplines_values = ", ".join(["%s"] * len(disciplines_data))

query_disciplines = (f"INSERT INTO public.disciplines (name,check_type,description,tag,technical) VALUES {disciplines_values}")
cursor.execute(query_disciplines, disciplines_data)

# таблица План для каждого года 8 семестров,каждя дисциплина, случайная специальность
cursor.execute('''CREATE TABLE public.plan
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    semestr integer,
    year integer,
    hours integer,
    discip_id integer,
    spec_id integer,
    CONSTRAINT plan_pkey PRIMARY KEY (id),
    CONSTRAINT plan_discip_id_fkey FOREIGN KEY (discip_id)
        REFERENCES public.disciplines (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT plan_spec_id_fkey FOREIGN KEY (spec_id)
        REFERENCES public.specialnost (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);''')

plan_data = []

get_array_discip_id = "SELECT array_agg(id) FROM public.disciplines"
cursor.execute(get_array_discip_id)
array_discip_ids=cursor.fetchall()

get_array_spec_id = "SELECT array_agg(id) FROM public.specialnost"
cursor.execute(get_array_spec_id)
array_spec_ids=cursor.fetchall()


years = [2019,2020,2021,2022,2023]

for i in range(len(years)):
    for sem in range(1,9):
        for disc in range(len(array_discip_ids[0][0])):
            semestr = sem
            year = years[i]
            hours = random.randint(70,100)
            discip_id = array_discip_ids[0][0][disc]
            id = random.randint(0,len(array_spec_ids[0][0])-1)
            spec_id = array_spec_ids[0][0][id]
            #semestr + year + hours + discip_id + spec_id
            plan_data.append((semestr,year,hours, discip_id, spec_id))


plan_values = ", ".join(["%s"] * len(plan_data))
insert_query = (f"INSERT INTO public.plan (semestr,year,hours,discip_id, spec_id) VALUES {plan_values}")
cursor.execute(insert_query, plan_data)

# for _ in range(kolvo_plans):
#     semestr = random.randint(1,8)
#     year = random.choice([2019,2020,2021,2022,2023])
#     hours = random.randint(70,100)
#     id = random.randint(0,len(array_discip_ids[0][0])-1)
#     discip_id = array_discip_ids[0][0][id]
#     id = random.randint(0,len(array_spec_ids[0][0])-1)
#     spec_id = array_spec_ids[0][0][id]
#     #semestr + year + hours + discip_id + spec_id
#     plan_data.append((semestr,year,hours, discip_id, spec_id))


# таблица Лекции (занятие к дисциплине)
cursor.execute('''CREATE TABLE public.lecture
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying COLLATE pg_catalog."default",
    discip_id integer,
    CONSTRAINT lecture_pkey PRIMARY KEY (id),
    CONSTRAINT lecture_discip_id_fkey FOREIGN KEY (discip_id)
        REFERENCES public.disciplines (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);''')
kolvo_lectures = 20
lecture_data = []

get_array_discip_id = "SELECT array_agg(id) FROM public.disciplines"
cursor.execute(get_array_discip_id)
array_discip_ids=cursor.fetchall()

for _ in range(kolvo_lectures):
    for i in range(len(array_discip_ids[0][0])):
        name = random.choice(['лекция','практика','лабораторная работа'])
        discip_id = array_discip_ids[0][0][i]
        #name + discip_id
        lecture_data.append((name, discip_id))

# for _ in range(kolvo_lectures):
#     name = random.choice(['лекция','практика','лабораторная работа'])
#     id = random.randint(0,len(array_ids[0][0])-1)
#     discip_id = array_ids[0][0][id]
#     #namr + discip_id
#     lecture_data.append((name, discip_id))

lecture_values = ", ".join(["%s"] * len(lecture_data))
insert_query = (f"INSERT INTO public.lecture (name,discip_id) VALUES {lecture_values}")
cursor.execute(insert_query, lecture_data)

# Таблица Расписания
cursor.execute('''CREATE TABLE public.\"timeTable\"  
    (
     id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    week integer,
    date date,
    teacher_fio character varying COLLATE pg_catalog."default",
    group_id integer,
    lecture_id integer,
    number_classroom character varying COLLATE pg_catalog."default",
    "time" time without time zone,
    CONSTRAINT "timeTable_pkey" PRIMARY KEY (id),
    CONSTRAINT "timeTable_group_id_fkey" FOREIGN KEY (group_id)
        REFERENCES public."group" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "timeTable_lecture_id_fkey" FOREIGN KEY (lecture_id)
        REFERENCES public.lecture (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
    );''')

# kolvo_raspisanie = 10
timeTable_data = []

get_array_group_id = "SELECT array_agg(id) FROM public.group"
cursor.execute(get_array_group_id)
array_group_ids=cursor.fetchall()

get_array_lecture_id = "SELECT array_agg(id) FROM public.lecture"
cursor.execute(get_array_lecture_id)
array_lecture_ids=cursor.fetchall()
# Даты на 22-23 учебный год
def get_random_date():
    start = DT.strptime('01.09.2022', '%d.%m.%Y')
    end = DT.strptime('31.05.2023', '%d.%m.%Y')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    random_date =  start + timedelta(seconds=random_second)
    random_date = str(random_date)
    return ' '.join(random_date.split(' ')[:-1])

for gr in range(len(array_group_ids[0][0])):
    for lec in range(len(array_lecture_ids[0][0])):
        week = random.randint(1,16)
        date = get_random_date()
        time = random.choice(['9:00','10:40','12:40','14:20','16:20','18:00'])
        teacher_fio = fake.name()
        group_id = array_group_ids[0][0][gr]
        lecture_id = array_lecture_ids[0][0][lec]
        number_classroom = random.randint(100,400)
        
        timeTable_data.append((week,date,time,teacher_fio, group_id,lecture_id,number_classroom))

# for _ in range(kolvo_raspisanie):
#     week = random.randint(1,16)
#     date = get_random_date()
#     time = random.choice(['9:00','10:40','12:40','14:20','16:20','18:00'])
#     teacher_fio = fake.name()
#     id = random.randint(0,len(array_group_ids[0][0])-1)
#     group_id = array_group_ids[0][0][id]
#     id = random.randint(0,len(array_lecture_ids[0][0])-1)
#     lecture_id = array_lecture_ids[0][0][id]
#     number_classroom = random.randint(100,400)
    
#     timeTable_data.append((week,date,time,teacher_fio, group_id,lecture_id,number_classroom))

timeTable_values = ", ".join(["%s"] * len(timeTable_data))
insert_query = (f"INSERT INTO public.\"timeTable\" (week,date,time,teacher_fio, group_id,lecture_id,number_classroom) VALUES {timeTable_values}")
cursor.execute(insert_query, timeTable_data)

# Таблица посещения
cursor.execute('''CREATE TABLE public.visits
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    student_id integer,
    visited boolean,
    "timeTable_id" integer,
    date_visit date,
    CONSTRAINT visits_pkey PRIMARY KEY (id),
    CONSTRAINT visits_student_id_fkey FOREIGN KEY (student_id)
        REFERENCES public.students (id_stud_code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "visits_timeTable_id_fkey" FOREIGN KEY ("timeTable_id")
        REFERENCES public."timeTable" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);''')

kolvo_visits = 500
visits_data = []

get_array_student_id = "SELECT array_agg(id_stud_code) FROM public.students"
cursor.execute(get_array_student_id)
array_student_ids=cursor.fetchall()

get_array_timeTable_id = "SELECT array_agg(id) FROM public.\"timeTable\""
cursor.execute(get_array_timeTable_id)
array_timeTable_ids=cursor.fetchall()

# for st in range(len(array_student_ids[0][0])):
#     for tt in range(len(array_timeTable_ids[0][0])):
#         student_id = array_student_ids[0][0][st]
#         visited = random.choice([True, False])
#         timeTable_id = array_timeTable_ids[0][0][tt]
#         date_visit = get_random_date()
#         visits_data.append((student_id,visited,timeTable_id,date_visit))

for _ in range(kolvo_visits):
    id = random.randint(0,len(array_student_ids[0][0])-1)
    student_id = array_student_ids[0][0][id]
    visited = random.choice([True, False])
    id = random.randint(0,len(array_timeTable_ids[0][0])-1)
    timeTable_id = array_timeTable_ids[0][0][id]
    date = get_random_date()
    
    visits_data.append((student_id,visited,timeTable_id,date))

visits_values = ", ".join(["%s"] * len(visits_data))
insert_query = (f"INSERT INTO public.visits (student_id,visited,\"timeTable_id\",date_visit) VALUES {visits_values}")
cursor.execute(insert_query, visits_data)

print("Postrges fill")

#2 Генерация значений в MongoDB (Institite, Kafedra, Specialnost, Disciplines)
client = MongoClient('localhost',27017)

db = client.university
collection = db.institute

query_for_mongo = ("SELECT i.name, k.name, s.name, d.name, d.technical FROM public.institute i,public.kafedra k,public.specialnost s, public.disciplines d,public.plan p WHERE k.institute_id=i.id AND s.kafedra_id=k.id AND p.spec_id = s.id AND p.discip_id = d.id;")
cursor.execute(query_for_mongo)
res=cursor.fetchall()

for i in range(len(res)):
    db.institute.insert_one({
        'institute':[
            {
                'name':res[i][0],
                'cafedras':[
                    {
                        'name':res[i][1],
                        'specialnosts':[
                            {
                                'name': res[i][2],
                                'disciplines':[
                                    {
                                        'name':res[i][3],
                                        'technical':res[i][4]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    })


#3 В Redis (Steudents)
redis = redis.Redis(
     host= 'localhost',
     port= '6379')

query_for_redis = ("SELECT id_stud_code,fio FROM public.students;")
cursor.execute(query_for_redis)
result=cursor.fetchall()

for i in range(len(result)):
    redis.set(str(result[i][0]),str(result[i][1]))


#4 в ES таблица Materials
kolvo_materials = 100
get_array_lecture_id = "SELECT array_agg(id) FROM public.lecture"
cursor.execute(get_array_lecture_id)
array_lecture_ids=cursor.fetchall()

def get_lecture_id():
    l_id = random.randint(0,len(array_lecture_ids[0][0])-1)
    lecture_id = array_lecture_ids[0][0][l_id]
    return lecture_id

def get_lecture_text():
    fileObj = codecs.open( "main_scripts/lecture_text/random_text.txt", "r", "utf_8_sig" )
    text = fileObj.read() 
    fileObj.close()
    
    textArray=text.split()
    textArray.append('.')
    textArray.append(',')
    textArray.append('?')
    textArray.append('!')
    textArray.append(':')
    textArray.append('-')


    newText=[]
    for i in range(200):
        random_index = random.randint(0, len(textArray))
        newText.append(textArray[random_index])
    newText=' '.join(newText)
    # print(newText)
    return newText

mappings = {
        "properties": {
            "description": {"type": "text"},
            "lecture_id": {"type": "integer"}
    }
}

index_name = "materials"

es = Elasticsearch("http://elastic:uw3yy=ACpH1pmh2EZrEK@localhost:9200")

try:
    es.indices.create(index="materials", mappings=mappings)
except:
    print("index materials exists")

docs = []
try:
    for i in range(kolvo_materials):
        docs.append({ #get_lecture_text(),
            'description': 'Тема1.Введение Тема этих лекций – понять, как создавать безопасные системы, почему компьютерные системы иногда бывают небезопасными и как можно исправить положение, если что-то пошло не так. Не существует никакого учебника на эту тему, поэтому вы должны пользоваться записями этих лекций, которые также выложены на нашем сайте, и вы, ребята, должны их заблаговременно читать. Имеется также ряд вопросов, на которые вы должны будете ответить в письменной форме, а также вы можете прислать свои собственные вопросы до 10-00 часов вечера перед лекционным днём. И когда вы придёте на лекцию, мы обсудим ваши ответы и вопросы и выясним, что собой представляет эта система, какие проблемы решает, когда это работает и когда это не работает, и хороши ли эти способы в других случаях',
            'lecture_id' : get_lecture_id()
        })
    helpers.bulk(es, docs, index=index_name)

except Exception as err:
		print("Error in creating docs in ES (materials)!!! ", err)

#5 в Neo
uri = "bolt://localhost:7687"
userName = "neo4j"
password = "root"

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))

query_select_students = ("SELECT id_stud_code,fio,group_id FROM public.students;")
cursor.execute(query_select_students)
students=cursor.fetchall()

query_select_groups = ("SELECT id, name, spec_id FROM public.group;")
cursor.execute(query_select_groups)
groups=cursor.fetchall()

query_select_specialnost = ("SELECT id,name,kafedra_id FROM public.specialnost;")
cursor.execute(query_select_specialnost)
specialnosts=cursor.fetchall()

query_select_kafedra = ("SELECT id,name,institute_id FROM public.kafedra;")
cursor.execute(query_select_kafedra)
kafedras=cursor.fetchall()

query_select_institute = ("SELECT id,name FROM public.institute;")
cursor.execute(query_select_institute)
institutes=cursor.fetchall()

query_select_disciplines = ("SELECT id,name, technical FROM public.disciplines;")
cursor.execute(query_select_disciplines)
disciplines=cursor.fetchall()

query_select_lecture = ("SELECT id, name,discip_id FROM public.lecture;")
cursor.execute(query_select_lecture)
lectures=cursor.fetchall()

query_select_timeTable = ("SELECT id, date, time, group_id, lecture_id FROM public.\"timeTable\";")
cursor.execute(query_select_timeTable)
timeTables=cursor.fetchall()

query_select_plan = ("SELECT id, semestr, year, discip_id, spec_id FROM public.plan;")
cursor.execute(query_select_plan)
plans=cursor.fetchall()


with graphDB_Driver.session() as neo_session:
    for st in range(len(students)):
        neo_session.run("CREATE (st:Student{id_stud_code:$id_stud_code, fio: $fio, group_id: $group_id})", id_stud_code = str(students[st][0]),fio = str(students[st][1]), group_id =  str(students[st][2]))
    for gr in range(len(groups)):
        neo_session.run("CREATE (g:Group{iid: $id, name: $name, spec_id: $spec_id})",  id = str(groups[gr][0]),name = str(groups[gr][1]),  spec_id = str(groups[gr][2]))
    for spec in range(len(specialnosts)):
        neo_session.run("CREATE (s:Specialnost{iid: $id, name: $name, kafedra_id: $kafedra_id})", id = str(specialnosts[spec][0]), name = str(specialnosts[spec][1]), kafedra_id = str(specialnosts[spec][2]))
    for kaf in range(len(kafedras)):
        neo_session.run("CREATE (k:Kafedra{iid: $id, name: $name, institute_id: $institute_id})", id = str(kafedras[kaf][0]), name = str(kafedras[kaf][1]), institute_id = str(kafedras[kaf][2]))
    for inst in range(len(institutes)):
        neo_session.run("CREATE (i:Institute{iid: $id, name: $name})", id = str(institutes[inst][0]), name = str(institutes[inst][1]))
    for disc in range(len(disciplines)):
        neo_session.run("CREATE (d:Disciplines{iid: $id,name: $name, technical: $technical})", id = str(disciplines[disc][0]),name = str(disciplines[disc][1]), technical = str(disciplines[disc][2]))
    for lec in range(len(lectures)):
        neo_session.run("CREATE (l:Lecture{iid:$id, name: $name, discip_id: $discip_id})",id = str(lectures[lec][0]),name = str(lectures[lec][1]), discip_id = str(lectures[lec][2]))
    for tt in range(len(timeTables)):
        neo_session.run("CREATE (t:TimeTable{iid:$id, date: $date, time: $time, group_id: $group_id, lecture_id: $lecture_id})",id = str(timeTables[tt][0]),date = str(timeTables[tt][1]), time = str(timeTables[tt][2]), group_id = str(timeTables[tt][3]), lecture_id = str(timeTables[tt][4]))
    for p in range(len(plans)):
        neo_session.run("CREATE (p:Plan{iid:$id, semestr: $semestr, year: $year, discip_id: $discip_id, spec_id: $spec_id})",id = str(plans[p][0]),semestr = str(plans[p][1]), year = str(plans[p][2]), discip_id = str(plans[p][3]), spec_id = str(plans[p][4]))

    neo_session.run("MATCH (i:Institute),(k:Kafedra) WHERE i.iid = k.institute_id  CREATE (k)-[:kafedra_institute]->(i)")
    neo_session.run("MATCH (k:Kafedra),(s:Specialnost) WHERE k.iid = s.kafedra_id CREATE (s)-[:specialnost_kafedra]->(k)")
    neo_session.run("MATCH (s:Specialnost),(g:Group) WHERE s.iid = g.spec_id CREATE (g)-[:group_specialnost]->(s)")
    neo_session.run("MATCH (g:Group),(st:Student) WHERE g.iid = st.group_id CREATE (st)-[:group_student]->(g)")
    neo_session.run("MATCH (d:Disciplines),(p:Plan) WHERE d.iid = p.discip_id CREATE (p)-[:plan_disciplina]->(d)")
    neo_session.run("MATCH (d:Disciplines),(l:Lecture) WHERE d.iid = l.discip_id CREATE (l)-[:lecture_disciplina]->(d)")
    neo_session.run("MATCH (s:Specialnost),(p:Plan) WHERE s.iid = p.spec_id CREATE (p)-[:plan_specialnost]->(s)")
    neo_session.run("MATCH (l:Lecture),(t:TimeTable) WHERE l.iid = t.lecture_id CREATE (t)-[:timeTable_lecture]->(l)")
    neo_session.run("MATCH (g:Group),(t:TimeTable) WHERE g.iid = t.group_id CREATE (t)-[:timeTable_group]->(g)")
    
    
from faker import Faker
import random
from neo4j import GraphDatabase

fake = Faker('ru_RU')

uri = "bolt://localhost:7687"
userName = "neo4j"
password = "root"

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))

students = []
for _ in range(10):
    students.append(fake.name())

groups = ['БСБО-01-19', 'БСБО-02-19','БСБО-03-19']
disciplines = ['Методы системной инженерии', 'Облачные технологии']
specialnost = ['Информационные системы и технологии', 'Прикладная математика']
kafedra = ['КБ-3','КБ-1']
institute = ['Кибербезопасности и цифровых технологий']
lecture_time = ['2022-11-11 10:40:00','2022-11-11 09:00:00']
lecture_id = [1,2,3,4]

with graphDB_Driver.session() as neo_session:
    for student in students:
        neo_session.run("CREATE (st:Student{stud_code:$stud_code, name: $name})", name = student)
    for group in groups:
        neo_session.run("CREATE (g:Group{name: $name})", name = group)
    for spec in specialnost:
        neo_session.run("CREATE (s:Specialnost{name: $name})", name = spec)
    for kaf in kafedra:
        neo_session.run("CREATE (k:Kafedra{name: $name})", name = kaf)
    for inst in institute:
        neo_session.run("CREATE (i:Institute{name: $name})", name = inst)
    for disc in disciplines:
        neo_session.run("CREATE (d:Disciplines{name: $name})", name = disc)
    for lec in lecture_time:
        neo_session.run("CREATE (l:Lecture{name: $name})", name = lec)
    

    # в первой группе:
    for r in range(0, 3):
        neo_session.run("MATCH (a:Student), (b:Group) WHERE a.name = $name_st AND b.name = $gr_name CREATE (a)-[:study_in]->(b)", name_st = students[r], gr_name = groups[0])
    
    # во второй группе:
    for r in range(3, 7):
        neo_session.run("MATCH (a:Student), (b:Group) WHERE a.name = $name_st AND b.name = $gr_name CREATE (a)-[:study_in]->(b)", name_st = students[r], gr_name = groups[1])
    
    # в третьей группе:
    for r in range(7, 10):
        neo_session.run("MATCH (a:Student), (b:Group) WHERE a.name = $name_st AND b.name = $gr_name CREATE (a)-[:study_in]->(b)", name_st = students[r], gr_name = groups[2])
    
    #первая и вторая группа на 1 спецаильности
    for gr in range(0, 2):
        for sp in range(0, 1):
            neo_session.run("MATCH (b:Group), (s:Specialnost) WHERE b.name = $name_gr AND s.name = $name_cr CREATE (b)-[:refer_to]->(s)", name_gr = groups[gr], name_cr = specialnost[sp])
     #Третья группа на 2 спецаильности
    for gr in range(2,len(groups)):
        for sp in range(1, len(specialnost)):
            neo_session.run("MATCH (b:Group), (s:Specialnost) WHERE b.name = $name_gr AND s.name = $name_spec CREATE (b)-[:refer_to]->(s)", name_gr = groups[gr], name_spec = specialnost[sp])
    #1 дисциплина на 1 специальности
    for disc in range(0, 1):
        for sp in range(0, 1):
            neo_session.run("MATCH (d:Disciplines), (s:Specialnost) WHERE d.name = $name_disc AND s.name = $name_spec CREATE (d)-[:refer_to]->(s)", name_disc = disciplines[disc], name_spec = specialnost[sp])
     #2 дисциплина на 2 специальности
    for disc in range(1, 2):
        for sp in range(1, 2):
            neo_session.run("MATCH (d:Disciplines), (s:Specialnost) WHERE d.name = $name_disc AND s.name = $name_spec CREATE (d)-[:refer_to]->(s)", name_disc = disciplines[disc], name_spec = specialnost[sp])
    
    #1 время для 1 дисциалины
    for lec in range(0, 1):
        for disc in range(0, 1):
            neo_session.run("MATCH (l:Lecture), (d:Disciplines) WHERE l.name = $name_lec AND d.name = $name_disc CREATE (l)-[:date_time]->(d)", name_lec = lecture_time[lec],name_disc = disciplines[disc])
    #2 время для 2 дисциалины
    for lec in range(1, 2):
        for disc in range(1, 2):
            neo_session.run("MATCH (l:Lecture), (d:Disciplines) WHERE l.name = $name_lec AND d.name = $name_disc CREATE (l)-[:date_time]->(d)", name_lec = lecture_time[lec],name_disc = disciplines[disc])
     
    #Информационные системы и технологии - КБ-3
    for sp in range(0,1):
        for kaf in range(0, 1):
            neo_session.run("MATCH (s:Specialnost), (k:Kafedra) WHERE s.name = $name_spec AND k.name = $name_ka CREATE (s)-[:belong_to]->(k)",name_spec = specialnost[sp], name_ka = kafedra[kaf])
    #Приклодная математика и технологии - КБ-1
    for sp in range(1,2):
        for kaf in range(1, 2):
            neo_session.run("MATCH (s:Specialnost), (k:Kafedra) WHERE s.name = $name_spec AND k.name = $name_ka CREATE (s)-[:belong_to]->(k)",name_spec = specialnost[sp], name_ka = kafedra[kaf])
    
    #КБ-3 и КБ-1 - ИКБ
    for kaf in range(0,2):
        for inst in range(0, 1):
            neo_session.run("MATCH (k:Kafedra), (i:Institute) WHERE k.name = $name_ka AND i.name = $name_inst CREATE (k)-[:part_of]->(i)", name_ka = kafedra[kaf], name_inst = institute[inst])
    
    print("Nodes added successful!")

# def get_group_name():
#     array1 = ["БСБО","БББО","БИСО","БОСО","БАСО"]
#     array2 = ["01","02","03","04","05"]
#     array3 = ["19","20","21","22"]
#     return random.choice(list(array1))+"-"+random.choice(list(array2))+"-"+random.choice(list(array3))

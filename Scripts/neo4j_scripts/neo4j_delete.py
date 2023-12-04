from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
userName = "neo4j"
password = "root"

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))

#Удалить всё
with graphDB_Driver.session() as neo_session:
        neo_session.run("MATCH (n) DETACH DELETE n")
        print("delete success")

#Удалить
# del_student = input("studen`s FIO for delete>")

# del_group = input("group for delete>")

# del_course = input("course for delete>")

# with graphDB_Driver.session() as neo_session:
#     neo_session.run("MATCH (a:Student {name: $name}) DETACH DELETE a", name = del_student)
#     neo_session.run("MATCH (b:Group {name: $name}) DETACH DELETE b", name = del_group)
#     neo_session.run("MATCH (c:Course {name: $name}) DETACH DELETE c", name = del_course)
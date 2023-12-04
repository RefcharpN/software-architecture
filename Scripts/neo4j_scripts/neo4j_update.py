from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
userName = "neo4j"
password = "root"

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))

old_student = input("studen`s FIO for update>")
new_student = input("new FIO>")

old_group = input("group for update>")
new_group = input("new group>")

old_course = input("course for update>")
new_course = input("new course>")

with graphDB_Driver.session() as neo_session:
    neo_session.run("MATCH (a:Student {name: $name_st}) SET a.name = $new_name_st", name_st = old_student, new_name_st = new_student)
    neo_session.run("MATCH (b:Group {name: $name_gr}) SET b.name = $new_name_gr", name_gr = old_group, new_name_gr = new_group)
    neo_session.run("MATCH (c:Course {name: $name_cr}) SET c.name = $new_name_cr", name_cr = old_course, new_name_cr = new_course)

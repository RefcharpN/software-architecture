from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
userName = "neo4j"
password = "root"

graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))

cqlNodeQuery  = "MATCH (n) RETURN n"

with graphDB_Driver.session() as neo_session:
    nodes = neo_session.run(cqlNodeQuery)
    for node in nodes:
        print(node)
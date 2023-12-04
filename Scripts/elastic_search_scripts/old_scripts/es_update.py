from elasticsearch import Elasticsearch

es = Elasticsearch("http://elastic:uw3yy=ACpH1pmh2EZrEK@localhost:9200")

doc ={
    "doc": {
    "course":"Разработка ПО",
    "description":"test"
    }
}

response = es.update(index='courses', id='JUWiI4QBpXLlSxbglwx0', body=doc)
print(response)
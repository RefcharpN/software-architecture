from elasticsearch import Elasticsearch, helpers

mappings = {
        "properties": {
            "course": {"type": "text"},
            "description": {"type": "text"},
    }
}

index_name = "courses"

es = Elasticsearch("http://elastic:uw3yy=ACpH1pmh2EZrEK@localhost:9200")

try:
    es.indices.create(index="courses", mappings=mappings)
except:
    print("index exists")


try:
		docs = [
        {'course': 'Алгоритмы компонентов цифровой обработки данных',
        'description': 'Описание курса1...'},
        {'course': 'Методы системной инженерии',
        'description': 'Описание курса2...'},
        {'course': 'Облачные технологии',
        'description': 'Описание курса3...'},
	    ]

		helpers.bulk(es, docs, index=index_name)
		print("docs added!!")
except Exception as err:
		print("Error in creating docs ", err)
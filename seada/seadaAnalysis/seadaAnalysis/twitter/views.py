from django.shortcuts import render

from .elasticsearchHandler import ElasticSearchUtils


def config_elasticsearch(es_host, es_port):
    _es = None
    _es = ElasticSearchUtils(es_host=es_host, es_port=es_port)
    es_connection = _es.connect_elasticsearch()
    if es_connection:
        _es.es_connection = es_connection

    return _es


def search(es, index, query):
    response = None
    try:
        response = es.es_connection.search(index=index, body=query)
    except:
        print("Error with query!!")
    return response


def index(request):
    template = 'twitter/index.html'
    context = {
        'title': 'SEADA Analysis',
    }
    return render(request, template, context)


def add_user(request):
    template = 'twitter/add_user.html'
    context = {
        'title': 'Add User',
    }
    return render(request, template, context)


def __get_complete_user_list():

    query = {
      "size": 1000,
      "query": {
        "match_all": {}
      },
      "_source": {
        "includes": ["id", "name", "screen_name", "location", "description", "url", "followers_count", "protected", "friends_count", "listed_count", "favourites_count", "created_at", "geo_enabled", "geo_enabled", "verified", "statuses_count"]
      }
    }

    __es_host = "127.0.0.1"
    __es_port = "9200"
    __index = 'twitter_user'
    es = config_elasticsearch(es_host=__es_host, es_port=__es_port)
    response = search(es=es, index=__index, query=query)

    __user_list = []

    if response:
        total = response['hits']['total']['value']
        for hit in response['hits']['hits']:
            user_list_field = []
            user_list_field.append(hit['_source']['id'])
            user_list_field.append(hit['_source']['name'])
            user_list_field.append(hit['_source']['screen_name'])
            user_list_field.append(hit['_source']['location'])
            user_list_field.append(hit['_source']['description'])
            user_list_field.append(hit['_source']['url'])
            user_list_field.append(hit['_source']['followers_count'])
            user_list_field.append(hit['_source']['protected'])
            user_list_field.append(hit['_source']['friends_count'])
            user_list_field.append(hit['_source']['listed_count'])
            user_list_field.append(hit['_source']['favourites_count'])
            user_list_field.append(hit['_source']['created_at'])
            user_list_field.append(hit['_source']['geo_enabled'])
            user_list_field.append(hit['_source']['verified'])
            user_list_field.append(hit['_source']['statuses_count'])
            __user_list.append(user_list_field)

    return __user_list


def userlist(request):

    __user_list = __get_complete_user_list()

    template = 'twitter/userlist.html'
    context = {
        'title': 'SEADA Twitter Userlist',
        'user_list': __user_list
    }
    return render(request, template, context)


def user(request, user_id):
    template = 'twitter/user.html'
    context = {
        'title': 'SEADA Twitter User',
    }
    return render(request, template, context)

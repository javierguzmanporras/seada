from django.shortcuts import render
from django.http import JsonResponse

from elasticsearch import Elasticsearch
from ElasticsearchUtils import *
from datetime import datetime


def get_num_users_protected_and_verified():
    """
    Get total of users with verified account in BBDD
    :return: int, total of users
    """
    query = {
      "size": 0,
      "aggregations": {
        "protected": {"terms": {"field": "protected"}},
        "verified": {"terms": {"field": "verified"}}
      }
    }
    es_host = "127.0.0.1"
    es_port = "9200"
    index = 'twitter_user'
    response = None
    total = 0
    verified = 0
    not_verified = 0
    verified_percentage = 0
    protected = 0
    not_protected = 0
    protected_percentage = 0

    es = config_elasticsearch(es_host=es_host, es_port=es_port)
    response = search(es=es, index=index, query=query)

    if response:
        total = response['hits']['total']['value']
        for bucket in response['aggregations']['verified']['buckets']:
            if bucket['key_as_string'] == "true":
                verified = bucket['doc_count']
            else:
                not_verified = bucket['doc_count']

        for bucket in response['aggregations']['protected']['buckets']:
            if bucket['key_as_string'] == "true":
                protected = bucket['doc_count']
            else:
                not_protected = bucket['doc_count']

        verified_percentage = (verified / total) * 100
        protected_percentage = (protected / total) * 100

    return verified_percentage, protected_percentage


def get_num(index):
    """
    Get total users storaged in BBDD
    :return: int total of users
    """
    query = {
      "size": 0,
      "query": {
        "match_all": {}
      }
    }

    value = None
    es_host = "127.0.0.1"
    es_port = "9200"
    es = config_elasticsearch(es_host=es_host, es_port=es_port)
    response = search(es=es, index=index, query=query)

    if response:
        value = response['hits']['total']['value']

    return value


def dashboard(request):

    get_time_line_data(request=None)

    __verified_percentage, __protected_percentage = get_num_users_protected_and_verified()

    template = 'dashboard/dashboard.html'
    context = {
        'title': 'Django chart.js',
        'users_card_tittle': 'Users in BBDD',
        'users_card_number': get_num(index='twitter_user'),
        'tweets_card_tittle': 'Tweets in BBDD',
        'tweets_card_number': get_num(index='twitter_tweets'),
        'protected_users_card_tittle': 'Protected',
        'protected_users_card_number': __protected_percentage,
        'verified_users_card_tittle': 'Verified',
        'verified_users_card_number': __verified_percentage
    }
    return render(request, template, context)


def get_user_list():

    query = {
      "query": {
        "match_all": {}
      },
      "_source": {
        "includes": [ "name", "screen_name"]
      }
    }

    es_host = "127.0.0.1"
    es_port = "9200"
    index = 'twitter_user'
    es = config_elasticsearch(es_host=es_host, es_port=es_port)
    response = search(es=es, index=index, query=query)

    __user_list = []
    if response:
        total = response['hits']['total']['value']
        for hit in response['hits']['hits']:
            user_list_field = []
            user_list_field.append(hit['_source']['name'])
            user_list_field.append(hit['_source']['screen_name'])
            __user_list.append(user_list_field)

    return __user_list


def user_list(request):

    __user_list = get_user_list()

    template = 'dashboard/userlist.html'
    context = {
        'title': 'Django chart.js',
        'user_list': __user_list
    }
    return render(request, template, context)


def compare_users(request):

    __user_list = False

    if request.POST:
        __user_list = request.POST.getlist('usercheck', False)

    if __user_list and (len(__user_list) > 1):
        template = 'dashboard/compare_users.html'
        context = {
            'title': 'Django chart.js',
            'user1': __user_list[0],
            'user2': __user_list[1]
        }
    else:
        template = 'dashboard/error.html'
        context = {
            'title': 'Error',
            'error_message': 'error selecting users',
            'back_to_url': 'userlist'
        }

    return render(request, template, context)


def test(request):
    template = 'dashboard/test.html'
    context = {
        'title': 'Django chart.js'
    }
    return render(request, template, context)



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


def get_chart_data(request):
    """
    only responsibility to aggregate the data the return a JSON response with the labels and data
    :param request:
    :return:
    """
    labels = ['A', 'B', 'C']
    data = ['10', '10', '10']

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def get_time_line_data(request):
    """

    :param request:
    :return:
    """

    query = {
      "query": {
        "bool": {
          "should": [
            { "match": { "user_screen_name": "complejolambda"}}
          ],
          "minimum_should_match": 1
        }
      },
      "_source": {
        "includes": [ "id", "user_screen_name", "created_at", "text"]
      }
    }

    query2 = {
      "size": 20,
      "query": {
        "bool": {
          "should": [
            { "match": { "user_screen_name": "complejolambda"}}
          ],
          "minimum_should_match": 1
        }
      },
      "sort": [
        {
          "created_at": {"order": "asc"}
        }
      ],
      "_source": {
        "includes": [ "id", "user_screen_name", "created_at", "text"]
      }
    }

    es_host = "127.0.0.1"
    es_port = "9200"
    index = 'twitter_tweets'
    es = config_elasticsearch(es_host=es_host, es_port=es_port)
    response = search(es=es, index=index, query=query2)

    labels = []
    data = []

    if response:
        hits = response['hits']['hits']
        for hit in hits:
            labels.append(hit['_source']['created_at'])
            if hit['_source']['text'].startswith("RT @"):
                #data.append(1)
                data.append("RT")
            else:
                #data.append(2)
                data.append("T")

    output_data = {
        'labels': labels,
        'data': data,
    }

    #return JsonResponse(data=output_data)
    return data, labels


def get_time_line_data_v2(request, user):
    """

    :param request:
    :return:
    """
    query = {
        "size": 20,
        "query": {
            "bool": {
                "should": [
                    {"match": {"user_screen_name": user}}
                ],
                "minimum_should_match": 1
            }
        },
        "sort": [
            {
                "created_at": {"order": "desc"}
            }
        ],
        "_source": {
            "includes": ["id", "user_screen_name", "created_at", "text"]
        }
    }

    query2 = {
      "size": 20,
      "query": {
        "bool": {
          "should": [
            { "match": {
              "user_screen_name": {
                "query": "complejolambda Victor_Fdz",
                "operator": "or"
              }}
            }
          ],
          "minimum_should_match": 1
        }
      },
      "sort": [
        {
          "created_at": {"order": "desc"}
        }
      ],
      "_source": {
        "includes": [ "id", "user_screen_name", "created_at", "text"]
      }
    }

    es_host = "127.0.0.1"
    es_port = "9200"
    index = 'twitter_tweets'
    es = config_elasticsearch(es_host=es_host, es_port=es_port)
    response = search(es=es, index=index, query=query)

    data = []

    if response:
        hits = response['hits']['hits']
        for hit in hits:
            item = {
                'x': int(datetime.strptime(hit['_source']['created_at'], '%Y-%m-%dT%H:%M:%S').strftime('%s')) * 1000,
                'description': hit['_source']['created_at'] + "\n" + hit['_source']['text'],
                'name': hit['_source']['user_screen_name'],
                'label': hit['_source']['user_screen_name'],
                # 'dataLabels': {
                #                 'color': '#78f',
                #                 'borderColor': 'blue',
                #                 'backgroundColor': '#444',
                #                 'style': {'textOutline': 0}
                # }
            }
            data.append(item)

    return JsonResponse(data, safe=False)



import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse

def get_time_line_mat(request):

    names, dates = get_time_line_data(None)

    # names = ['v2.2.4', 'v3.0.3', 'v3.0.2', 'v3.0.1', 'v3.0.0', 'v2.2.3',
    #          'v2.2.2', 'v2.2.1', 'v2.2.0', 'v2.1.2', 'v2.1.1', 'v2.1.0',
    #          'v2.0.2', 'v2.0.1', 'v2.0.0', 'v1.5.3', 'v1.5.2', 'v1.5.1',
    #          'v1.5.0', 'v1.4.3', 'v1.4.2', 'v1.4.1', 'v1.4.0']

    # dates = ['2019-02-26', '2019-02-26', '2018-11-10', '2018-11-10',
    #          '2018-09-18', '2018-08-10', '2018-03-17', '2018-03-16',
    #          '2018-03-06', '2018-01-18', '2017-12-10', '2017-10-07',
    #          '2017-05-10', '2017-05-02', '2017-01-17', '2016-09-09',
    #          '2016-07-03', '2016-01-10', '2015-10-29', '2015-02-16',
    #          '2014-10-26', '2014-10-18', '2014-08-26']

    #dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
    dates = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in dates]

    # Choose some nice levels
    #levels = np.tile([-5, 5, -3, 3, -1, 1], int(np.ceil(len(dates) / 6)))[:len(dates)]

    levels = []
    for d in names:
        if d == "T":
            levels.append(1)
        else:
            levels.append(2)

    levels = np.asarray(levels)

    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title="Tweets user 1")

    markerline, stemline, baseline = ax.stem(dates, levels,
                                             linefmt="C3-",
                                             basefmt="k-",
                                             use_line_collection=True)

    plt.setp(markerline, mec="k", mfc="w", zorder=3)

    # Shift the markers to the baseline by replacing the y-data by zeros.
    markerline.set_ydata(np.zeros(len(dates)))

    # annotate lines
    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
    for d, l, r, va in zip(dates, levels, names, vert):
        ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l) * 3),
                    textcoords="offset points", va=va, ha="right")

    # format xaxis with 4 month intervals
    # ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=4))
    ax.get_xaxis().set_major_locator(mdates.HourLocator(interval=4))
    # ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%d %b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    # remove y axis and spines
    ax.get_yaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)

    ax.margins(y=0.1)
    #plt.show()

    # Como enviaremos la imagen en bytes la guardaremos en un buffer
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)

    # Creamos la respuesta enviando los bytes en tipo imagen png
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    # Limpiamos la figura para liberar memoria
    fig.clear()

    # Añadimos la cabecera de longitud de fichero para más estabilidad
    response['Content-Length'] = str(len(response.content))

    # Devolvemos la response
    return response


def get_network_data(request):

    data = {
        "nodes": [
            {"id": "Microsoft", "group": 1},
            {"id": "Apple", "group": 2},
            {"id": "hp", "group": 2},
            {"id": "logitech", "group": 3},
        ],
        "links": [
            {"source": "Microsoft", "target": "Apple", "value": 0.5},
            {"source": "hp", "target": "Apple", "value": 0.5},
            {"source": "logitech", "target": "Apple", "value": 0.5},
        ]
    }

    data2 = {
      "nodes": [
        {"id": "Myriel", "group": 1},
        {"id": "Napoleon", "group": 1},
        {"id": "Mlle.Baptistine", "group": 1},
        {"id": "Mme.Magloire", "group": 1},
        {"id": "CountessdeLo", "group": 1},
        {"id": "Geborand", "group": 1},
        {"id": "Champtercier", "group": 1},
        {"id": "Cravatte", "group": 1},
        {"id": "Count", "group": 1},
        {"id": "OldMan", "group": 1},
        {"id": "Labarre", "group": 2},
        {"id": "Valjean", "group": 2},
        {"id": "Marguerite", "group": 3},
        {"id": "Mme.deR", "group": 2},
        {"id": "Isabeau", "group": 2},
        {"id": "Gervais", "group": 2},
        {"id": "Tholomyes", "group": 3},
        {"id": "Listolier", "group": 3},
        {"id": "Fameuil", "group": 3},
        {"id": "Blacheville", "group": 3},
        {"id": "Favourite", "group": 3},
        {"id": "Dahlia", "group": 3},
        {"id": "Zephine", "group": 3},
        {"id": "Fantine", "group": 3},
        {"id": "Mme.Thenardier", "group": 4},
        {"id": "Thenardier", "group": 4},
        {"id": "Cosette", "group": 5},
        {"id": "Javert", "group": 4},
        {"id": "Fauchelevent", "group": 0},
        {"id": "Bamatabois", "group": 2},
        {"id": "Perpetue", "group": 3},
        {"id": "Simplice", "group": 2},
        {"id": "Scaufflaire", "group": 2},
        {"id": "Woman1", "group": 2},
        {"id": "Judge", "group": 2},
        {"id": "Champmathieu", "group": 2},
        {"id": "Brevet", "group": 2},
        {"id": "Chenildieu", "group": 2},
        {"id": "Cochepaille", "group": 2},
        {"id": "Pontmercy", "group": 4},
        {"id": "Boulatruelle", "group": 6},
        {"id": "Eponine", "group": 4},
        {"id": "Anzelma", "group": 4},
        {"id": "Woman2", "group": 5},
        {"id": "MotherInnocent", "group": 0},
        {"id": "Gribier", "group": 0},
        {"id": "Jondrette", "group": 7},
        {"id": "Mme.Burgon", "group": 7},
        {"id": "Gavroche", "group": 8},
        {"id": "Gillenormand", "group": 5},
        {"id": "Magnon", "group": 5},
        {"id": "Mlle.Gillenormand", "group": 5},
        {"id": "Mme.Pontmercy", "group": 5},
        {"id": "Mlle.Vaubois", "group": 5},
        {"id": "Lt.Gillenormand", "group": 5},
        {"id": "Marius", "group": 8},
        {"id": "BaronessT", "group": 5},
        {"id": "Mabeuf", "group": 8},
        {"id": "Enjolras", "group": 8},
        {"id": "Combeferre", "group": 8},
        {"id": "Prouvaire", "group": 8},
        {"id": "Feuilly", "group": 8},
        {"id": "Courfeyrac", "group": 8},
        {"id": "Bahorel", "group": 8},
        {"id": "Bossuet", "group": 8},
        {"id": "Joly", "group": 8},
        {"id": "Grantaire", "group": 8},
        {"id": "MotherPlutarch", "group": 9},
        {"id": "Gueulemer", "group": 4},
        {"id": "Babet", "group": 4},
        {"id": "Claquesous", "group": 4},
        {"id": "Montparnasse", "group": 4},
        {"id": "Toussaint", "group": 5},
        {"id": "Child1", "group": 10},
        {"id": "Child2", "group": 10},
        {"id": "Brujon", "group": 4},
        {"id": "Mme.Hucheloup", "group": 8}
      ],
      "links": [
        {"source": "Napoleon", "target": "Myriel", "value": 1},
        {"source": "Mlle.Baptistine", "target": "Myriel", "value": 8},
        {"source": "Mme.Magloire", "target": "Myriel", "value": 10},
        {"source": "Mme.Magloire", "target": "Mlle.Baptistine", "value": 6},
        {"source": "CountessdeLo", "target": "Myriel", "value": 1},
        {"source": "Geborand", "target": "Myriel", "value": 1},
        {"source": "Champtercier", "target": "Myriel", "value": 1},
        {"source": "Cravatte", "target": "Myriel", "value": 1},
        {"source": "Count", "target": "Myriel", "value": 2},
        {"source": "OldMan", "target": "Myriel", "value": 1},
        {"source": "Valjean", "target": "Labarre", "value": 1},
        {"source": "Valjean", "target": "Mme.Magloire", "value": 3},
        {"source": "Valjean", "target": "Mlle.Baptistine", "value": 3},
        {"source": "Valjean", "target": "Myriel", "value": 5},
        {"source": "Marguerite", "target": "Valjean", "value": 1},
        {"source": "Mme.deR", "target": "Valjean", "value": 1},
        {"source": "Isabeau", "target": "Valjean", "value": 1},
        {"source": "Gervais", "target": "Valjean", "value": 1},
        {"source": "Listolier", "target": "Tholomyes", "value": 4},
        {"source": "Fameuil", "target": "Tholomyes", "value": 4},
        {"source": "Fameuil", "target": "Listolier", "value": 4},
        {"source": "Blacheville", "target": "Tholomyes", "value": 4},
        {"source": "Blacheville", "target": "Listolier", "value": 4},
        {"source": "Blacheville", "target": "Fameuil", "value": 4},
        {"source": "Favourite", "target": "Tholomyes", "value": 3},
        {"source": "Favourite", "target": "Listolier", "value": 3},
        {"source": "Favourite", "target": "Fameuil", "value": 3},
        {"source": "Favourite", "target": "Blacheville", "value": 4},
        {"source": "Dahlia", "target": "Tholomyes", "value": 3},
        {"source": "Dahlia", "target": "Listolier", "value": 3},
        {"source": "Dahlia", "target": "Fameuil", "value": 3},
        {"source": "Dahlia", "target": "Blacheville", "value": 3},
        {"source": "Dahlia", "target": "Favourite", "value": 5},
        {"source": "Zephine", "target": "Tholomyes", "value": 3},
        {"source": "Zephine", "target": "Listolier", "value": 3},
        {"source": "Zephine", "target": "Fameuil", "value": 3},
        {"source": "Zephine", "target": "Blacheville", "value": 3},
        {"source": "Zephine", "target": "Favourite", "value": 4},
        {"source": "Zephine", "target": "Dahlia", "value": 4},
        {"source": "Fantine", "target": "Tholomyes", "value": 3},
        {"source": "Fantine", "target": "Listolier", "value": 3},
        {"source": "Fantine", "target": "Fameuil", "value": 3},
        {"source": "Fantine", "target": "Blacheville", "value": 3},
        {"source": "Fantine", "target": "Favourite", "value": 4},
        {"source": "Fantine", "target": "Dahlia", "value": 4},
        {"source": "Fantine", "target": "Zephine", "value": 4},
        {"source": "Fantine", "target": "Marguerite", "value": 2},
        {"source": "Fantine", "target": "Valjean", "value": 9},
        {"source": "Mme.Thenardier", "target": "Fantine", "value": 2},
        {"source": "Mme.Thenardier", "target": "Valjean", "value": 7},
        {"source": "Thenardier", "target": "Mme.Thenardier", "value": 13},
        {"source": "Thenardier", "target": "Fantine", "value": 1},
        {"source": "Thenardier", "target": "Valjean", "value": 12},
        {"source": "Cosette", "target": "Mme.Thenardier", "value": 4},
        {"source": "Cosette", "target": "Valjean", "value": 31},
        {"source": "Cosette", "target": "Tholomyes", "value": 1},
        {"source": "Cosette", "target": "Thenardier", "value": 1},
        {"source": "Javert", "target": "Valjean", "value": 17},
        {"source": "Javert", "target": "Fantine", "value": 5},
        {"source": "Javert", "target": "Thenardier", "value": 5},
        {"source": "Javert", "target": "Mme.Thenardier", "value": 1},
        {"source": "Javert", "target": "Cosette", "value": 1},
        {"source": "Fauchelevent", "target": "Valjean", "value": 8},
        {"source": "Fauchelevent", "target": "Javert", "value": 1},
        {"source": "Bamatabois", "target": "Fantine", "value": 1},
        {"source": "Bamatabois", "target": "Javert", "value": 1},
        {"source": "Bamatabois", "target": "Valjean", "value": 2},
        {"source": "Perpetue", "target": "Fantine", "value": 1},
        {"source": "Simplice", "target": "Perpetue", "value": 2},
        {"source": "Simplice", "target": "Valjean", "value": 3},
        {"source": "Simplice", "target": "Fantine", "value": 2},
        {"source": "Simplice", "target": "Javert", "value": 1},
        {"source": "Scaufflaire", "target": "Valjean", "value": 1},
        {"source": "Woman1", "target": "Valjean", "value": 2},
        {"source": "Woman1", "target": "Javert", "value": 1},
        {"source": "Judge", "target": "Valjean", "value": 3},
        {"source": "Judge", "target": "Bamatabois", "value": 2},
        {"source": "Champmathieu", "target": "Valjean", "value": 3},
        {"source": "Champmathieu", "target": "Judge", "value": 3},
        {"source": "Champmathieu", "target": "Bamatabois", "value": 2},
        {"source": "Brevet", "target": "Judge", "value": 2},
        {"source": "Brevet", "target": "Champmathieu", "value": 2},
        {"source": "Brevet", "target": "Valjean", "value": 2},
        {"source": "Brevet", "target": "Bamatabois", "value": 1},
        {"source": "Chenildieu", "target": "Judge", "value": 2},
        {"source": "Chenildieu", "target": "Champmathieu", "value": 2},
        {"source": "Chenildieu", "target": "Brevet", "value": 2},
        {"source": "Chenildieu", "target": "Valjean", "value": 2},
        {"source": "Chenildieu", "target": "Bamatabois", "value": 1},
        {"source": "Cochepaille", "target": "Judge", "value": 2},
        {"source": "Cochepaille", "target": "Champmathieu", "value": 2},
        {"source": "Cochepaille", "target": "Brevet", "value": 2},
        {"source": "Cochepaille", "target": "Chenildieu", "value": 2},
        {"source": "Cochepaille", "target": "Valjean", "value": 2},
        {"source": "Cochepaille", "target": "Bamatabois", "value": 1},
        {"source": "Pontmercy", "target": "Thenardier", "value": 1},
        {"source": "Boulatruelle", "target": "Thenardier", "value": 1},
        {"source": "Eponine", "target": "Mme.Thenardier", "value": 2},
        {"source": "Eponine", "target": "Thenardier", "value": 3},
        {"source": "Anzelma", "target": "Eponine", "value": 2},
        {"source": "Anzelma", "target": "Thenardier", "value": 2},
        {"source": "Anzelma", "target": "Mme.Thenardier", "value": 1},
        {"source": "Woman2", "target": "Valjean", "value": 3},
        {"source": "Woman2", "target": "Cosette", "value": 1},
        {"source": "Woman2", "target": "Javert", "value": 1},
        {"source": "MotherInnocent", "target": "Fauchelevent", "value": 3},
        {"source": "MotherInnocent", "target": "Valjean", "value": 1},
        {"source": "Gribier", "target": "Fauchelevent", "value": 2},
        {"source": "Mme.Burgon", "target": "Jondrette", "value": 1},
        {"source": "Gavroche", "target": "Mme.Burgon", "value": 2},
        {"source": "Gavroche", "target": "Thenardier", "value": 1},
        {"source": "Gavroche", "target": "Javert", "value": 1},
        {"source": "Gavroche", "target": "Valjean", "value": 1},
        {"source": "Gillenormand", "target": "Cosette", "value": 3},
        {"source": "Gillenormand", "target": "Valjean", "value": 2},
        {"source": "Magnon", "target": "Gillenormand", "value": 1},
        {"source": "Magnon", "target": "Mme.Thenardier", "value": 1},
        {"source": "Mlle.Gillenormand", "target": "Gillenormand", "value": 9},
        {"source": "Mlle.Gillenormand", "target": "Cosette", "value": 2},
        {"source": "Mlle.Gillenormand", "target": "Valjean", "value": 2},
        {"source": "Mme.Pontmercy", "target": "Mlle.Gillenormand", "value": 1},
        {"source": "Mme.Pontmercy", "target": "Pontmercy", "value": 1},
        {"source": "Mlle.Vaubois", "target": "Mlle.Gillenormand", "value": 1},
        {"source": "Lt.Gillenormand", "target": "Mlle.Gillenormand", "value": 2},
        {"source": "Lt.Gillenormand", "target": "Gillenormand", "value": 1},
        {"source": "Lt.Gillenormand", "target": "Cosette", "value": 1},
        {"source": "Marius", "target": "Mlle.Gillenormand", "value": 6},
        {"source": "Marius", "target": "Gillenormand", "value": 12},
        {"source": "Marius", "target": "Pontmercy", "value": 1},
        {"source": "Marius", "target": "Lt.Gillenormand", "value": 1},
        {"source": "Marius", "target": "Cosette", "value": 21},
        {"source": "Marius", "target": "Valjean", "value": 19},
        {"source": "Marius", "target": "Tholomyes", "value": 1},
        {"source": "Marius", "target": "Thenardier", "value": 2},
        {"source": "Marius", "target": "Eponine", "value": 5},
        {"source": "Marius", "target": "Gavroche", "value": 4},
        {"source": "BaronessT", "target": "Gillenormand", "value": 1},
        {"source": "BaronessT", "target": "Marius", "value": 1},
        {"source": "Mabeuf", "target": "Marius", "value": 1},
        {"source": "Mabeuf", "target": "Eponine", "value": 1},
        {"source": "Mabeuf", "target": "Gavroche", "value": 1},
        {"source": "Enjolras", "target": "Marius", "value": 7},
        {"source": "Enjolras", "target": "Gavroche", "value": 7},
        {"source": "Enjolras", "target": "Javert", "value": 6},
        {"source": "Enjolras", "target": "Mabeuf", "value": 1},
        {"source": "Enjolras", "target": "Valjean", "value": 4},
        {"source": "Combeferre", "target": "Enjolras", "value": 15},
        {"source": "Combeferre", "target": "Marius", "value": 5},
        {"source": "Combeferre", "target": "Gavroche", "value": 6},
        {"source": "Combeferre", "target": "Mabeuf", "value": 2},
        {"source": "Prouvaire", "target": "Gavroche", "value": 1},
        {"source": "Prouvaire", "target": "Enjolras", "value": 4},
        {"source": "Prouvaire", "target": "Combeferre", "value": 2},
        {"source": "Feuilly", "target": "Gavroche", "value": 2},
        {"source": "Feuilly", "target": "Enjolras", "value": 6},
        {"source": "Feuilly", "target": "Prouvaire", "value": 2},
        {"source": "Feuilly", "target": "Combeferre", "value": 5},
        {"source": "Feuilly", "target": "Mabeuf", "value": 1},
        {"source": "Feuilly", "target": "Marius", "value": 1},
        {"source": "Courfeyrac", "target": "Marius", "value": 9},
        {"source": "Courfeyrac", "target": "Enjolras", "value": 17},
        {"source": "Courfeyrac", "target": "Combeferre", "value": 13},
        {"source": "Courfeyrac", "target": "Gavroche", "value": 7},
        {"source": "Courfeyrac", "target": "Mabeuf", "value": 2},
        {"source": "Courfeyrac", "target": "Eponine", "value": 1},
        {"source": "Courfeyrac", "target": "Feuilly", "value": 6},
        {"source": "Courfeyrac", "target": "Prouvaire", "value": 3},
        {"source": "Bahorel", "target": "Combeferre", "value": 5},
        {"source": "Bahorel", "target": "Gavroche", "value": 5},
        {"source": "Bahorel", "target": "Courfeyrac", "value": 6},
        {"source": "Bahorel", "target": "Mabeuf", "value": 2},
        {"source": "Bahorel", "target": "Enjolras", "value": 4},
        {"source": "Bahorel", "target": "Feuilly", "value": 3},
        {"source": "Bahorel", "target": "Prouvaire", "value": 2},
        {"source": "Bahorel", "target": "Marius", "value": 1},
        {"source": "Bossuet", "target": "Marius", "value": 5},
        {"source": "Bossuet", "target": "Courfeyrac", "value": 12},
        {"source": "Bossuet", "target": "Gavroche", "value": 5},
        {"source": "Bossuet", "target": "Bahorel", "value": 4},
        {"source": "Bossuet", "target": "Enjolras", "value": 10},
        {"source": "Bossuet", "target": "Feuilly", "value": 6},
        {"source": "Bossuet", "target": "Prouvaire", "value": 2},
        {"source": "Bossuet", "target": "Combeferre", "value": 9},
        {"source": "Bossuet", "target": "Mabeuf", "value": 1},
        {"source": "Bossuet", "target": "Valjean", "value": 1},
        {"source": "Joly", "target": "Bahorel", "value": 5},
        {"source": "Joly", "target": "Bossuet", "value": 7},
        {"source": "Joly", "target": "Gavroche", "value": 3},
        {"source": "Joly", "target": "Courfeyrac", "value": 5},
        {"source": "Joly", "target": "Enjolras", "value": 5},
        {"source": "Joly", "target": "Feuilly", "value": 5},
        {"source": "Joly", "target": "Prouvaire", "value": 2},
        {"source": "Joly", "target": "Combeferre", "value": 5},
        {"source": "Joly", "target": "Mabeuf", "value": 1},
        {"source": "Joly", "target": "Marius", "value": 2},
        {"source": "Grantaire", "target": "Bossuet", "value": 3},
        {"source": "Grantaire", "target": "Enjolras", "value": 3},
        {"source": "Grantaire", "target": "Combeferre", "value": 1},
        {"source": "Grantaire", "target": "Courfeyrac", "value": 2},
        {"source": "Grantaire", "target": "Joly", "value": 2},
        {"source": "Grantaire", "target": "Gavroche", "value": 1},
        {"source": "Grantaire", "target": "Bahorel", "value": 1},
        {"source": "Grantaire", "target": "Feuilly", "value": 1},
        {"source": "Grantaire", "target": "Prouvaire", "value": 1},
        {"source": "MotherPlutarch", "target": "Mabeuf", "value": 3},
        {"source": "Gueulemer", "target": "Thenardier", "value": 5},
        {"source": "Gueulemer", "target": "Valjean", "value": 1},
        {"source": "Gueulemer", "target": "Mme.Thenardier", "value": 1},
        {"source": "Gueulemer", "target": "Javert", "value": 1},
        {"source": "Gueulemer", "target": "Gavroche", "value": 1},
        {"source": "Gueulemer", "target": "Eponine", "value": 1},
        {"source": "Babet", "target": "Thenardier", "value": 6},
        {"source": "Babet", "target": "Gueulemer", "value": 6},
        {"source": "Babet", "target": "Valjean", "value": 1},
        {"source": "Babet", "target": "Mme.Thenardier", "value": 1},
        {"source": "Babet", "target": "Javert", "value": 2},
        {"source": "Babet", "target": "Gavroche", "value": 1},
        {"source": "Babet", "target": "Eponine", "value": 1},
        {"source": "Claquesous", "target": "Thenardier", "value": 4},
        {"source": "Claquesous", "target": "Babet", "value": 4},
        {"source": "Claquesous", "target": "Gueulemer", "value": 4},
        {"source": "Claquesous", "target": "Valjean", "value": 1},
        {"source": "Claquesous", "target": "Mme.Thenardier", "value": 1},
        {"source": "Claquesous", "target": "Javert", "value": 1},
        {"source": "Claquesous", "target": "Eponine", "value": 1},
        {"source": "Claquesous", "target": "Enjolras", "value": 1},
        {"source": "Montparnasse", "target": "Javert", "value": 1},
        {"source": "Montparnasse", "target": "Babet", "value": 2},
        {"source": "Montparnasse", "target": "Gueulemer", "value": 2},
        {"source": "Montparnasse", "target": "Claquesous", "value": 2},
        {"source": "Montparnasse", "target": "Valjean", "value": 1},
        {"source": "Montparnasse", "target": "Gavroche", "value": 1},
        {"source": "Montparnasse", "target": "Eponine", "value": 1},
        {"source": "Montparnasse", "target": "Thenardier", "value": 1},
        {"source": "Toussaint", "target": "Cosette", "value": 2},
        {"source": "Toussaint", "target": "Javert", "value": 1},
        {"source": "Toussaint", "target": "Valjean", "value": 1},
        {"source": "Child1", "target": "Gavroche", "value": 2},
        {"source": "Child2", "target": "Gavroche", "value": 2},
        {"source": "Child2", "target": "Child1", "value": 3},
        {"source": "Brujon", "target": "Babet", "value": 3},
        {"source": "Brujon", "target": "Gueulemer", "value": 3},
        {"source": "Brujon", "target": "Thenardier", "value": 3},
        {"source": "Brujon", "target": "Gavroche", "value": 1},
        {"source": "Brujon", "target": "Eponine", "value": 1},
        {"source": "Brujon", "target": "Claquesous", "value": 1},
        {"source": "Brujon", "target": "Montparnasse", "value": 1},
        {"source": "Mme.Hucheloup", "target": "Bossuet", "value": 1},
        {"source": "Mme.Hucheloup", "target": "Joly", "value": 1},
        {"source": "Mme.Hucheloup", "target": "Grantaire", "value": 1},
        {"source": "Mme.Hucheloup", "target": "Bahorel", "value": 1},
        {"source": "Mme.Hucheloup", "target": "Courfeyrac", "value": 1},
        {"source": "Mme.Hucheloup", "target": "Gavroche", "value": 1},
        {"source": "Mme.Hucheloup", "target": "Enjolras", "value": 1}
      ]
    }

    return JsonResponse(data, safe=False)


def __get_bar_data(user):
    query = {
        "size": 0,
        "query": {
            "bool": {
                "should": [
                    {"match": {"user_screen_name": user}}
                ],
                "minimum_should_match": 1,
                "filter": [{
                    "range": {
                        "created_at": {
                            "gte": "now-7d/d",
                            "lte": "now"
                        }
                    }
                }]
            }
        },
        "aggs": {
            "test": {
                "date_histogram": {
                    "field": "created_at",
                    "calendar_interval": "day"
                }
            }
        }
    }

    es_host = "127.0.0.1"
    es_port = "9200"
    index = 'twitter_tweets'
    es = config_elasticsearch(es_host=es_host, es_port=es_port)
    response = search(es=es, index=index, query=query)

    print(response)

    labels = []
    data = []
    if response:
        for bucket in response['aggregations']['test']['buckets']:
            labels.append(bucket['key_as_string'].split('T')[0])
            data.append(bucket['doc_count'])

    return labels, data


def get_bar_data(request, user1, user2):

    __labels, __user1_data = __get_bar_data(user1)
    _, __user2_data = __get_bar_data(user2)
    print(__labels)
    print(__user1_data)
    print(__user2_data)

    data = {
        'labels': __labels,
        'user1_data': __user1_data,
        'user1_label': user1,
        'user2_data': __user2_data,
        'user2_label': user2
    }

    return JsonResponse(data=data, safe=False)

from django.shortcuts import render
from django.http import JsonResponse

from elasticsearch import Elasticsearch

from ElasticsearchUtils__old import *
from datetime import datetime, timedelta
from textblob import TextBlob

import timer


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


def __get_user_list():

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

    __user_list = __get_user_list()

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


def __get_network_data(user1, user2, today, before):

    print(user1)
    print(user2)
    print(today)
    print(before)

    query = {
      "size": 1000,
      "query": {
        "bool": {
          "should": [
            { "multi_match": {
                "query": "RT",
                "fields": ["text.keyword"]
              }
            },
            {
              "multi_match": {
                "query": user2,
                "fields": ["text"]
              }
            }
          ],
          "minimum_should_match": 1,
          "filter": [
            {"term": {"user_screen_name": user1}},
            {"range": {
              "created_at": {
                "gte": before,
                "lte": today
              }
            }
          }]
        }
      },
      "sort": [
        {
          "created_at": {"order": "desc"}
        }
      ],
      "_source": {
        "includes": ["text"]
      }
    }

    es_host = "127.0.0.1"
    es_port = "9200"
    index = 'twitter_tweets'
    es = config_elasticsearch(es_host=es_host, es_port=es_port)
    response = search(es=es, index=index, query=query)

    print(response)

    return response['hits']['total']['value']


def get_network_data(request, user1, user2):

    today = str(datetime.now().date())
    before = str((datetime.now() - timedelta(days=14)).date())

    info_u1 = __get_network_data(user1=user1, user2=user2, today=today, before=before)
    info_u2 = __get_network_data(user1=user1, user2=user2, today=today, before=before)

    id1 = str(user1) + "," + str(info_u1) + "RT"
    id2 = str(user2) + "," + str(info_u2) + "RT"

    print(id1)
    print(id2)

    data = {
        "nodes": [
            {"id": id1},
            {"id": id2}
        ],
        "links": [
            {"source": id1, "target": id2, "value": 0.5},
            {"source": id2, "target": id1, "value": 0.5},
        ]
    }

    # data = {
    #     "nodes": [
    #         {"id": "Microsoft", "group": 1},
    #         {"id": "Apple", "group": 2},
    #         {"id": "hp", "group": 2},
    #         {"id": "logitech", "group": 3},
    #     ],
    #     "links": [
    #         {"source": "Microsoft", "target": "Apple", "value": 0.5},
    #         {"source": "hp", "target": "Apple", "value": 0.5},
    #         {"source": "logitech", "target": "Apple", "value": 0.5},
    #     ]
    # }



    return JsonResponse(data, safe=False)


def __get_bar_data(user, labels):
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
                            "gte": labels[0],
                            "lte": labels[-1]
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

    data = []

    """
    Complex code for build a list of 7 dates for 7 days.
    obtengo el bucket.
    - si la fecha del bucket coincide con la fecha de las etiquetas, añado el dato a la lista y aumento el indice
    de los buckets.
    - si la fecha no coincide, añado un cero a la lista de datos.
    """
    if response:
        if response['hits']['total']['value'] > 0:
            buckets_index = 0
            for x in range(7):
                bucket = response['aggregations']['test']['buckets'][buckets_index]
                if bucket['key_as_string'].split('T')[0] == labels[x]:
                    data.append(bucket['doc_count'])
                    if buckets_index < (len(response['aggregations']['test']['buckets']) - 1):
                        buckets_index = buckets_index + 1
                else:
                    data.append("0")
        else:
            data = [0, 0, 0, 0, 0, 0, 0]

    return data


def __get_update_bar_data(user, date):

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
                            "gte": date,
                            "lte": date,
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

    data = None
    if response:
        if response['hits']['total']['value'] > 0:
            data = response['aggregations']['test']['buckets'][0]['doc_count']
        else:
            data = '0'

    return data


def get_update_bar_data(request, user1, user2, date):

    new_date = str((datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)).date())
    __user1_data = __get_update_bar_data(user=user1, date=new_date)
    __user2_data = __get_update_bar_data(user=user2, date=new_date)

    print(__user1_data)
    print(__user2_data)

    data = {
        'user1_data': __user1_data, #_user1_data,
        'user2_data': __user2_data, #_user2_data,
        'label': new_date
    }

    return JsonResponse(data=data, safe=False)


def get_bar_data(request, user1, user2):
    __labels = []
    for day in reversed(range(7)):
        __labels.append(str((datetime.now() - timedelta(days=day)).date()))

    __user1_data = __get_bar_data(user=user1, labels=__labels)
    __user2_data = __get_bar_data(user=user2, labels=__labels)

    data = {
        'labels': __labels,
        'user1_data': __user1_data,
        'user1_label': user1,
        'user2_data': __user2_data,
        'user2_label': user2
    }

    return JsonResponse(data=data, safe=False)


def user_sentiment_analysis(request, userid):

    t = timer.Timer('user_sentiment')
    t.start()

    query = {
      "size": 10000,
      "query": {
        "match": {"user_id": userid}
      },
      "_source": {
        "includes": ["text", "user_name"]
      }
    }
    es_host = "127.0.0.1"
    es_port = "9200"
    index = 'twitter_tweets'
    es = config_elasticsearch(es_host=es_host, es_port=es_port)
    response = search(es=es, index=index, query=query)

    data_sentiment = {'negative': 0, 'neutral': 0, 'positive': 0}

    if response:
        total = response['hits']['total']['value']
        name = response['hits']['hits'][0]['_source']['user_name']
        for hit in response['hits']['hits']:
            tweet = TextBlob(hit['_source']["text"])

            if tweet.sentiment.polarity < 0:
                data_sentiment["negative"] += 1
            elif tweet.sentiment.polarity == 0:
                data_sentiment["neutral"] += 1
            else:
                data_sentiment["positive"] += 1

    dataset = [data_sentiment['negative'], data_sentiment['neutral'], data_sentiment['positive']]
    data = {
        'data': dataset,
        'title_text': "Sentiment Analysis with {} Tweets for {}".format(total, name)
    }
    elapsed_time = t.stop()
    print('[views.user_sentment_analsysis] Time to compleat: {} sec'.format(elapsed_time))
    return JsonResponse(data=data, safe=False)


def user_hour_analysis(request, userid):

    query = {
      "size": 0,
      "query": {
        "match": {"user_id": userid}
      },
      "aggs": {
        "hour_analysis": {
          "date_histogram": {
            "field": "created_at",
            "calendar_interval": "hour"
          }
        }
      }
    }

    es_host = "127.0.0.1"
    es_port = "9200"
    index = 'twitter_tweets'
    es = config_elasticsearch(es_host=es_host, es_port=es_port)
    response = search(es=es, index=index, query=query)

    __data = {}
    total = 0

    # inicialize data
    for i in range(24):
        __data[i] = 0

    # print(__data)

    if response:
        total = response['hits']['total']['value']
        for bucket in response['aggregations']['hour_analysis']['buckets']:
            date = datetime.strptime(bucket['key_as_string'], '%Y-%m-%dT%H:%M:%S.%fZ')
            __data[date.hour] = __data[date.hour] + bucket['doc_count']

        # print(__data)

    __dataset = []
    for i in range(24):
        __dataset.append(__data[i])

    # print(str(__dataset))
    data = {
        'data': __dataset,
        'title_text': "User Analysis with " + str(total) + " Tweets for " + userid,
    }

    return JsonResponse(data=data, safe=False)


def __get_user_information(userid):

    query = {
      "query": {
        "match": {"id": userid}
      }
    }

    es_host = "127.0.0.1"
    es_port = "9200"
    index = 'twitter_user'
    es = config_elasticsearch(es_host=es_host, es_port=es_port)
    response = search(es=es, index=index, query=query)

    __data = None

    if response:
        if response['hits']['total']['value'] > 0:
            __data = response['hits']['hits'][0]['_source']

    return __data


# comprobar que el usarioid existe
# obtener su información
def user_dashboard(request, userid):

    data = __get_user_information(userid)
    data['profile_image_url_https'] = data['profile_image_url_https'].replace("_normal", "")
    d = datetime.today() - datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S')

    if d.days > 0:
        data['tweets_average'] = round(float(data['statuses_count'] / (d.days * 1.0)), 2)
        data['likes_average'] = round(float(data['favourites_count'] / (d.days * 1.0)), 2)
    else:
        data['tweets_average'] = data['statuses_count']
        data['likes_average'] = data['self.favourites_count']

    template = 'dashboard/user_dashboard.html'
    context = {
        'title': 'User dashboard',
        'userid': userid,
        'data': data
    }
    return render(request, template, context)


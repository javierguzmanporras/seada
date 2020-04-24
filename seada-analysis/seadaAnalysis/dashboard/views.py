from django.shortcuts import render
from django.http import JsonResponse

from elasticsearch import Elasticsearch
from ElasticsearchUtils import *


def dashboard(request):

    get_time_line_data(request=None)

    template = 'dashboard/dashboard.html'
    context = {
        'title': 'Django chart.js'
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
          "created_at.keyword": {"order": "asc"}
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
        print("type hits: " + str(type(hits)))
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
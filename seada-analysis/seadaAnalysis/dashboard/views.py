from django.shortcuts import render
from django.http import JsonResponse


def dashboard(request):
    template = 'dashboard/dashboard.html'
    context = {
        'title': 'Django chart.js'
    }
    return render(request, template, context)


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


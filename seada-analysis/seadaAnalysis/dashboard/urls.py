from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('chart/', views.get_chart_data, name='chart_data'),
    path('timeline/', views.get_time_line_data, name='time_line_data'),
    path('timelinev2/', views.get_time_line_data_v2, name='time_line_data_v2'),
    path('timelinev2/<str:user>/', views.get_time_line_data_v2, name='time_line_data_v3'),
    path('test/', views.get_time_line_mat, name='test'),
    path('test2/', views.test, name='test2')
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user/<str:userid>', views.user_dashboard, name='user_dashboard'),
    path('user/hour_analysis/<str:userid>', views.user_hour_analysis, name='user_hour_analysis'),
    path('user/sentiment_analysis/<str:userid>', views.user_sentiment_analysis, name='user_sentiment_analysis'),
    path('userlist/', views.user_list, name='userlist'),
    path('compareusers/', views.compare_users, name='compare_users'),
    path('compareusers/timeline/<str:user>/', views.get_time_line_data_v2, name='time_line_data_v3'),
    path('compareusers/network/', views.get_network_data, name='network_data'),
    path('compareusers/network/<str:user1>/<str:user2>/', views.get_network_data, name='network_data'),
    path('compareusers/barchart/<str:user1>/<str:user2>/<str:date>', views.get_update_bar_data, name='update_bar_data'),
    path('compareusers/barchart/<str:user1>/<str:user2>', views.get_bar_data, name='bar_data'),

    path('chart/', views.get_chart_data, name='chart_data'),
    path('timeline/', views.get_time_line_data, name='time_line_data'),
    path('timelinev2/', views.get_time_line_data_v2, name='time_line_data_v2'),
    path('test/', views.get_time_line_mat, name='test'),
    path('test2/', views.test, name='test2'),
    path('test2/network/', views.get_network_data, name='network_data')
]

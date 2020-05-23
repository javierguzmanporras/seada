from django.urls import path

from . import views

app_name = 'twitter'
urlpatterns = [
    path('', views.index, name='twitter'),
    path('adduser/', views.add_user, name='adduser'),
    path('userlist/', views.userlist, name='userlist'),
    path('user/<str:user_id>', views.user, name='user'),
]
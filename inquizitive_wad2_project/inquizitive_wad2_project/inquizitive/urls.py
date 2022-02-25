from django.urls import path
from inquizitive import views


app_name = 'inquizitive'

urlpatterns = [
    path('', views.index, name='index'),
]

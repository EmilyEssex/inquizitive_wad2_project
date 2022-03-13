from django.urls import path
from inquizitive import views
from . import views


#app_name = 'inquizitive'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name ='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('inquizitive/creating_quiz/', views.creating_quiz, name='creating_quiz'),
    path('inquizitive/adding_questions/', views.adding_questions, name='adding_questions'),
 #   path('inquizitive/quiz/<slug:quiz_name_slug>/', views.show_quiz1,name='show_quiz1'),
    path('inquizitive/quiz/<slug:quiz_name_slug>/', views.show_quiz1, name='show_quiz1'),
    path('inquizitive/quiz/<slug:quiz_name_slug>/adding_questions/',views.adding_questions, name='adding_questions'),

 
]

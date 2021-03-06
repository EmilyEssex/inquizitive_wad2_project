from django.urls import path
from inquizitive import views
from . import views
#from .views import user_account
from .views import user_account
from django.conf import settings
from django.conf.urls.static import static

#app_name = 'inquizitive'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name ='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('account/', user_account, name='user_account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('account/update_image', views.update_image, name='update_image'),
    path('inquizitive/creating_quiz/', views.creating_quiz, name='creating_quiz'),
    path('inquizitive/meet_the_team/', views.meet_the_team, name='meet_the_team'),
    path('inquizitive/adding_questions/', views.adding_questions, name='adding_questions'),
 #   path('inquizitive/quiz/<slug:quiz_name_slug>/', views.show_quiz1,name='show_quiz1'),
    path('inquizitive/quiz/<slug:quiz_name_slug>/', views.show_quiz1, name='show_quiz1'),
    path('inquizitive/quiz/<slug:quiz_name_slug>/adding_questions/',views.adding_questions, name='adding_questions'),
   # path('inquizitive/<slug:quiz_name_slug>/quizResults/', views.quizResults, name='quizResults'),
    path('inquizitive/<slug:quiz_name_slug>/answerQuiz/', views.answerQuiz, name='answerQuiz'),

    
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

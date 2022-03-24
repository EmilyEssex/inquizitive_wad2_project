from django.contrib import admin
from inquizitive.models import Question, Quiz, UserProfile



class QuizAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('quizName',)}

admin.site.register(Quiz, QuizAdmin)
 
 
admin.site.register(UserProfile)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "questionText", "correctAnswer")

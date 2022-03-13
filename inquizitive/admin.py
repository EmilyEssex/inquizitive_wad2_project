from django.contrib import admin
from inquizitive.models import Question,   Quiz ,  Comment



 
# Add in this class to customise the Admin Interface 
class QuizAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('quizName',)}
# Update the registration to include this customised interface
admin.site.register(Quiz, QuizAdmin)
#admin.site.register(Quiz)
#admin.site.register(Question)
 
#admin.site.register(Score)
admin.site.register(Comment)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "questionText", "correctAnswer")
    
 
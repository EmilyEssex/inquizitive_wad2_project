from django.contrib import admin
from inquizitive.models import Question, Answer, Quiz  

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
#admin.site.register(Score)
#admin.site.register(Comment)

# Register your models here.

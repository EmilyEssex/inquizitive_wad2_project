from django.contrib import admin
from inquizitive.models import Question,   Quiz ,  Comment

admin.site.register(Quiz)
admin.site.register(Question)
 
#admin.site.register(Score)
admin.site.register(Comment)

# Register your models here.

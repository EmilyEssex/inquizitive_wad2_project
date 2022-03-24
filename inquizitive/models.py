from django.db import models
 
from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.postgres.fields.jsonb import JSONField
#from inquizitive.models import Quiz
 

# Create your models here.
class UserProfile(models.Model):
    # links UserProfile to a user model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # scores = models.ManyToManyField(Scores) #changed this from userscores to scores
    # ratings = models.ManyToManyField(Ratings) #changed this from user ratings to ratings
    
    profile = models.ImageField(default='default.jpg', upload_to='profile_images')

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return self.user.username
    # quiz = models.ManyToManyField('quizzes')

    
DIFFICULTY_CHOICES=[
    ('easy', 'Easy'),
    ('moderate', 'Moderate'),
    ('hard', 'Hard'),
    ]

class Quiz(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user=models.ForeignKey(User, on_delete=models.PROTECT, related_name='quizzes', null=True, default="")
    
   # creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="default value")
    quizName= models.CharField(max_length=128, null=True, unique=True)
    quizSubject= models.CharField(max_length=128,null=True)
    quizDifficulty = models.CharField(max_length=10, choices=(DIFFICULTY_CHOICES), default= DIFFICULTY_CHOICES[0])
    scoreToPass=models.IntegerField(default=0)
    numOfQue=models.IntegerField(default=1)
    #quizQuestions=models.ManyToManyField(Question)
    likes = models.ManyToManyField(User, related_name=("quiz_likes"))
    slug = models.SlugField(unique=True)
    passcodeBool=models.BooleanField
    passcode=models.CharField(max_length=128, blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.quizName) 
        super(Quiz, self).save(*args, **kwargs)
        
    def process_likes(self):
        print(self.likes)
        self.likes += 1
        
 
    class Meta:
        verbose_name_plural = 'quizzes'
    def __str__(self):
        return self.quizName
    def get_quiz_questions(self):
        return self.question_set.all()
    
 #New for likes    
#class Like(models.Model): 
   # user = models.ForeignKey(User, on_delete=models.CASCADE)
   # quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)   
    
    
    
class Question(models.Model):
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="question", null=True)
    questionText= models.CharField(max_length=500, unique=False)
    questionMarks=models.IntegerField(default=1)
    optiona=models.CharField(max_length=500,null=True)
    optionb=models.CharField(max_length=500,null=True)
    optionc=models.CharField(max_length=500,null=True)
    optiond=models.CharField(max_length=500,null=True)
    optionsList=[optiona,optionb,optionc,optiond]
    correctAnswer=models.CharField(max_length=500)
    class Meta:
        verbose_name_plural = 'questions'
    def __str__(self):
        return self.questionText
 
 
 
 
class Comment(models.Model):
     commentText= models.CharField(max_length=500, null=True)
    # quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE) 
     user=models.ForeignKey(User, on_delete=models.CASCADE) 
     #finalScore=models.FloatField(defualt=0)
     class Meta:
        verbose_name_plural = 'comments'
     def __str__(self):
        return self.comment_text
    
 
 



 
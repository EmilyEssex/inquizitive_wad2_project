from django.db import models
import json
from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    # links UserProfile to a user model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #scores = models.ManyToManyField(Scores) #changed this from userscores to scores
    # ratings = models.ManyToManyField(Ratings) #changed this from user ratings to ratings

    profile_pic = models.ImageField(default='default.jpg', upload_to='media/profile_images/')


    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return self.user.username
    # quiz = models.ManyToManyField('quizzes')


DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('moderate', 'Moderate'),
    ('hard', 'Hard'),
]


class Quiz(models.Model):
 
    user=models.ForeignKey(User, on_delete=models.PROTECT, related_name='quizzes', null=True, default="")
    quizName= models.CharField(max_length=128, null=True, unique=True)
    quizSubject= models.CharField(max_length=128,null=True)
    quizDifficulty = models.CharField(max_length=10, choices=(DIFFICULTY_CHOICES), default= DIFFICULTY_CHOICES[0])
    scoreToPass=models.IntegerField(default=0)
    numOfQue=models.IntegerField(default=1)
    likes = models.ManyToManyField(User, related_name=("quiz_likes"))
    slug = models.SlugField(unique=True)
 
 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.quizName)
        super(Quiz, self).save(*args, **kwargs)


 

    class Meta:
        verbose_name_plural = 'quizzes'

    def __str__(self):
        return self.quizName

    def get_quiz_questions(self):
        return self.question_set.all()

 

 
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="question", null=True)
    questionText = models.CharField(max_length=500, unique=True)
    questionMarks = models.IntegerField(default=1)

 
    optiona = models.CharField(max_length=500, null=True)
    optionb = models.CharField(max_length=500, null=True)
    optionc = models.CharField(max_length=500, null=True)
    optiond = models.CharField(max_length=500, null=True)
    optionsList = [optiona, optionb, optionc, optiond]
    correctAnswer = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'questions'

    def __str__(self):
        return self.questionText
 


 


class Scores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    # default score? If unattempted
    score = models.FloatField(default=0)

    class Meta:
       verbose_name_plural = "scores"

    def __str__(self):
     return self.score
 

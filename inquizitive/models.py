from django.db import models
 
from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import json
#from inquizitive.models import Quiz, Answer, Question
 
 

 
# Create your models here.
 
#RATING_OPTIONS= ("easy", "medium","hard")

    
class Answer(models.Model):
    answerText= models.CharField(max_length=500, null=True)
    #question=models.ForeignKey(Question , on_delete=models.CASCADE, related_name="answer")
    correctAnswer=models.BooleanField(default=False)
    #user=models.ForeignKey(User, on_delete=models.CASCADE)
 
    class Meta:
        verbose_name_plural = 'answers'
    def __str__(self):
        return self.answerText
  

    
DIFFICULTY_CHOICES=[
    ('easy', 'Easy'),
    ('moderate', 'Moderate'),
    ('hard', 'Hard'),
    ]
class Quiz(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    quizName= models.CharField(max_length=128, unique=True)
    quizSubject= models.CharField(max_length=128)
    
    privateStatus =models.BooleanField(default=False,help_text="Should this quiz only be accessible by a certain group of people?")
  
    uniquePasscode=models.CharField(max_length=128, unique=True, default="none")
    # will be the average rating
    quizDifficulty = models.CharField(max_length=10, choices=(DIFFICULTY_CHOICES))
    scoreToPass=models.IntegerField()
    #quizQuestions=models.ManyToManyField(Question)
    class Meta:
        verbose_name_plural = 'quizzes'
    def __str__(self):
        return self.quizName
    def get_quiz_questions(self):
        return self.question_set.all()
    
class Question(models.Model):
    questionText= models.CharField(max_length=500, unique=True)
    answerOptions=models.ManyToManyField(Answer)
    questionMarks=models.IntegerField()
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="question")
    
 
    class Meta:
        verbose_name_plural = 'questions'
    def __str__(self):
        return self.questionText
    def get_questions(self):
        for field_name in self.fields:
            if field_name.startswith('interest_'):
                yield self[field_name]
  #  def get_question_answers(self):
      #  return self.answer_set.all()
     #  
class Comment(models.Model):
     commentText= models.CharField(max_length=500, null=True)
     quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE) 
     user=models.ForeignKey(User, on_delete=models.CASCADE) 
     #finalScore=models.FloatField(defualt=0)
     class Meta:
        verbose_name_plural = 'comments'
     def __str__(self):
        return self.comment_text
    
 
 

class Scores(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    # default score? If unattempted
    score = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Scores"

    def __str__(self):
        return self.score
    
    
# i think well remove this as we said the create will choose the difficulty level instead
class Ratings(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    # default rating should just be unrated??
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Ratings"

    def __str__(self):
        return self.rating

class UserProfile(models.Model):
    # links UserProfile to a user model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    quiz = models.ManyToManyField(Quiz)
    scores = models.ManyToManyField(Scores) #changed this from userscores to scores
    ratings = models.ManyToManyField(Ratings) #changed this from user ratings to ratings

    profile = models.ImageField(upload_to = 'profile images', blank=True)

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return self.user.username

 
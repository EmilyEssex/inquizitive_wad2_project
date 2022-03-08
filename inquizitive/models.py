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
    quiz = models.ManyToManyField('quizzes')
   # scores = models.ManyToManyField(Scores) #changed this from userscores to scores
   # ratings = models.ManyToManyField(Ratings) #changed this from user ratings to ratings
#
    profile = models.ImageField(upload_to = 'profile images', blank=True)

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return self.user.username
  
class Answer(models.Model):
    answerText= models.CharField(max_length=500, blank=True, null=True)
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
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    quizName= models.CharField(max_length=128, default="default value")
    quizSubject= models.CharField(max_length=128, default="default value")
    
    #privateStatus =models.BooleanField(default=False,help_text="Should this quiz only be accessible by a certain group of people?")
  
    # uniquePasscode=models.CharField(max_length=128, unique=True,blank=True, null=True)
   
    quizDifficulty = models.CharField(max_length=10, choices=(DIFFICULTY_CHOICES), default= DIFFICULTY_CHOICES[0])
    scoreToPass=models.IntegerField(default=0)
    #quizQuestions=models.ManyToManyField(Question)
    class Meta:
        verbose_name_plural = 'quizzes'
    def __str__(self):
        return self.quizName
    def get_quiz_questions(self):
        return self.question_set.all()
    
class Question(models.Model):
    questionText= models.CharField(max_length=500, unique=True )
    questionMarks=models.IntegerField(default=1)
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="question")
    
    #{ "choices" : [option 1, option 2, option 3, option 4], "correct_index" : 2 }
    answers = models.JSONField( )
 
    
 
    class Meta:
        verbose_name_plural = 'questions'
    def __str__(self):
        return self.questionText
 
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
    
 
 

#class Scores(models.Model):
   # user = models.ForeignKey(User, on_delete=models.CASCADE)
    #quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    # default score? If unattempted
    #score = models.FloatField(default=0)

   # class Meta:
    #    verbose_name_plural = "Scores"

   # def __str__(self):
      #  return self.score
    
    
# i think well remove this as we said the create will choose the difficulty level instead
#class Ratings(models.Model): 
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    # default rating should just be unrated??
    #rating = models.IntegerField()

    #class Meta:
    #    verbose_name_plural = "Ratings"

    #def __str__(self):
    #    return self.rating


 
from django.db import models
 
from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import json


def main():
    mock_dict={"quizId" :["option1", "option2","option3"], "quizId" :["option1", "option2","option3"]}

    json1=json.dumps(mock_dict)
    print (json1)
    
if __name__ == "__main__":
    main()

 
 

 
# Create your models here.
 
#RATING_OPTIONS= ("easy", "medium","hard")

    
class Answer(models.Model):
    answer_text= models.CharField(max_length=500, null=True)
   # question=models.ForeignKey(Question , on_delete=models.CASCADE)
    correct_answer=models.BooleanField(default=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
 
    class Meta:
        verbose_name_plural = 'answers'
    def __str__(self):
        return self.answer_text

class Question(models.Model):
    question_text= models.CharField(max_length=500, unique=True)
    answer_options=models.ManyToManyField(Answer)
    #slug = models.SlugField(unique=True)
   # def save(self, *args, **kwargs):
        #self.slug = slugify(self.text) 
        #super(Question, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'questions'
    def __str__(self):
        return self.question_text

class Quiz(models.Model):
    name= models.CharField(max_length=128, unique=True)
    subject= models.CharField(max_length=128)
    private =models.BooleanField(default=False)
    question_text= models.JSONFIELD()
    answer_text= models.JSONFIELD()
    if private:
        uniqueCode=models.CharField(max_length=128, unique=True)
    # will be the average rating
    rating = models.CharField(max_length=10)
    quiz_questions=models.ManyToManyField(Question)
    class Meta:
        verbose_name_plural = 'quizzes'
    def __str__(self):
        return self.name

    
class Comment(models.model):
     comment_text= models.CharField(max_length=500, null=True)
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
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Scores"

    def __str__(self):
        return self.score

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

    quiz = models.OneToManyField(Quiz)
    scores = models.OneToManyField(Scores) #changed this from userscores to scores
    ratings = models.OneToManyField(Ratings) #changed this from user ratings to ratings

    profile = models.ImageField(upload_to = 'profile images', blank=True)

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return self.user.username

 

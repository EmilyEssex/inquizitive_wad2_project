from django.db import models
from django.contrib.auth import User
import json

# Create your models here.

class Scores(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    # default score? If unattempted
    score = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Scores"

    def __str__(self):
        #return self.score

class Ratings(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    # default rating should just be unrated??
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Ratings"

    def __str__(self):
        #return self.rating

class UserProfile(models.Model):
    # links UserProfile to a user model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    quiz = models.OneToManyField(Quiz)
    scores = models.OneToManyField(UserScores)
    ratings = models.OneToManyField(QuizRatings)

    profile = models.ImageField(upload_to = 'profile images', blank=True)

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return self.user.username



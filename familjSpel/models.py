from django.db import models
from django.contrib.auth.models import User 

class GameSession(models.Model):
    code     = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    question = models.CharField(max_length=200)
    state = models.IntegerField()
    master = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    voting_done = models.BooleanField()

class PlayerStatus(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    points  = models.IntegerField()
    answer  = models.CharField(max_length=100)
    votes   = models.IntegerField(default=0)
    done    = models.BooleanField()
    session = models.ForeignKey(GameSession, related_name="players", on_delete=models.CASCADE)




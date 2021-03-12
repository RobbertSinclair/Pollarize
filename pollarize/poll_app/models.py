from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    profileImage = models.ImageField()

class Polls(models.Model):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=300, null=False)
    answer1 = models.CharField(max_length=200, null=False)
    answer2 = models.CharField(max_length=200, null=False)
    votes1 = models.IntegerField(default=0)
    votes2 = models.IntegerField(default=0)

class Comments(models.Model):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Polls, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    votes = models.IntegerField(default=0)
    parent = models.ForeignKey("self", null=True, related_name="comments", on_delete=models.CASCADE)

class VotesIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Polls, on_delete=models.CASCADE)
    option = models.BooleanField()



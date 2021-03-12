from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    profileImage = models.ImageField(null=True)

class Poll(models.Model):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=300, null=False)
    slug = models.SlugField(max_length=300, default="")
    answer1 = models.CharField(max_length=200, null=False)
    answer2 = models.CharField(max_length=200, null=False)
    votes1 = models.IntegerField(default=0)
    votes2 = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        super(Poll, self).save(*args, **kwargs)

    def __str__(self):
        return self.question

class Comment(models.Model):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    votes = models.IntegerField(default=0)
    parent = models.ForeignKey("self", null=True, related_name="comments", on_delete=models.CASCADE)

class VotesIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.BooleanField()



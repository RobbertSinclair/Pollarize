from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    profile_image = models.ImageField(null=True, upload_to='profile_images', blank=True, default="default.png")

    def __str__(self):
        return self.user.username



class Poll(models.Model):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=300, null=False)
    poll_slug = models.SlugField(max_length=300, default="")
    answer1 = models.CharField(max_length=200, null=False)
    answer2 = models.CharField(max_length=200, null=False)
    votes1 = models.IntegerField(default=0)
    votes2 = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        if self.votes1 < 0:
            self.votes1 = 0
        if self.votes2 < 0:
            self.votes2 
        super(Poll, self).save(*args, **kwargs)

    def __str__(self):
        return self.question

class Comment(models.Model):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    votes = models.IntegerField(default=0)
    parent = models.ForeignKey("self", null=True, related_name="comments", on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        if self.parent == self:
            self.parent = None
        super(Comment, self).save(*args, **kwargs) 
    
    def __str__(self):
        return self.comment

class VotesIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.CharField(max_length=100)
    vote_time = models.DateTimeField('date voted', default=timezone.now)


# This is a linker model to only give a user one upvote or downvote
class VotesInComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    old_votes = models.IntegerField(default=0)



from django.contrib import admin
from poll_app.models import UserProfile, Poll, Comment, VotesIn  

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Poll)
admin.site.register(Comment)
admin.site.register(VotesIn)


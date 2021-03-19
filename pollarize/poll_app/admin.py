from django.contrib import admin
from poll_app.models import UserProfile, Poll, Comment, VotesIn, VotesInComment  

class PollAdmin(admin.ModelAdmin):
    prepopulated_fields = {'poll_slug':('question',)}


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Poll, PollAdmin)
admin.site.register(Comment)
admin.site.register(VotesIn)
admin.site.register(VotesInComment)


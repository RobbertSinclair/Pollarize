from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from poll_app.models import Poll, Comment, User, VotesIn
import json
import random

# Create your views here.

def index(request):
    return HttpResponse("<h1>Pollarize</h1>")


# JSON views here
class JSONRandomPoll(View):

    def get(self, request):
        try:
            the_poll = Poll.objects.all()[random.randint(0, len(Poll.objects.all())-1)]
            the_user = the_poll.submitter
            dictionary = {
                "question": the_poll.question, 
                "submitter": the_user.username, 
                "answer1": the_poll.answer1, 
                "answer2": the_poll.answer2,
                "votes1": the_poll.votes1,
                "votes2": the_poll.votes2
                }
            return JsonResponse(dictionary)
        except IndexError:
            return JsonResponse({})

class JSONPollByPopularity(View):

    def get(self, request):
        dictionary = {"polls": []}
        the_polls = [(poll, poll.votes1 + poll.votes2) for poll in Poll.objects.all()]
        the_polls = sorted(the_polls, key=lambda x: x[1])
        for poll in the_polls:
            poll = poll[0]
            poll_dict = {
                "question": poll.question,
                "submitter": poll.submitter.username,
                "answer1": poll.answer1,
                "answer2": poll.answer2,
                "votes1": poll.votes1,
                "votes2": poll.votes2
            }
            dictionary["polls"].append(poll_dict)
        return JsonResponse(dictionary)









        

    







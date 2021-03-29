from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.views import View
from poll_app.models import Poll, Comment, UserProfile, VotesIn, VotesInComment
from poll_app.forms import CreatePollForm, UserProfileForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse
import json
import random

# Create your views here.

def index(request):
    return redirect("poll_app:home")

def homepage(request):
    recent = Poll.objects.order_by('-pub_date')[:3]
    polls = Poll.objects.all()

    popular_polls = popular(polls)[:3]
    pollarizing_polls = pollarizing(polls)[:3]

    context_dict = {"recent": recent,
                    "popular": popular_polls,
                    "pollarizing": pollarizing_polls}

    response = render(request, 'poll_app/index.html', context=context_dict)
    return response

def popular(polls):
    popular = [(poll, poll.votes1 + poll.votes2) for poll in polls]
    popular = sorted(popular, key=lambda x: x[1], reverse=True)
    return [poll[0] for poll in popular]

def pollarizing(polls):
    pollarizing = [(poll, abs(((poll.votes1 / (poll.votes1 + poll.votes2)) * 100) - 50)) for poll in polls]
    pollarizing = sorted(pollarizing, key=lambda x: x[1])
    return [poll[0] for poll in pollarizing]

def about(request):
    return render(request, "poll_app/about.html")

def rankings(request):
    recent = Poll.objects.order_by('-pub_date')[:10]
    polls = Poll.objects.all()

    popular_polls = popular(polls)[:10]
    pollarizing_polls = pollarizing(polls)[:10]

    champion = pollarizing_polls[0]

    context_dict = {"champion": champion,
                    "recent": recent,
                    "popular": popular_polls,
                    "pollarizing": pollarizing_polls}

    response = render(request, 'poll_app/rankings.html', context=context_dict)
    return response

def random_poll(request):
    polls = Poll.objects.all()
    the_poll = random.choice(polls)
    the_slug = the_poll.poll_slug
    if request.user.is_authenticated:
        return redirect("poll_app:vote", poll_slug=the_slug)
    else:
        return redirect("poll_app:results", poll_slug=the_slug)

def create(request):
    context_dict = {}
    form = CreatePollForm()
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('poll_app:login'))
    if request.method == "POST":
        form = CreatePollForm(request.POST)
        if form.is_valid():
            poll_list = Poll.objects.order_by("id")
            obj = form.save(commit=False)
            obj.submitter = user
            obj.pub_date = timezone.now()
            obj.poll_slug = slugify(obj.question)
            obj.save()
            return redirect(reverse("poll_app:vote", kwargs={'poll_slug': obj.poll_slug}))
        else:
            print(form.errors)
    context_dict['form'] = form

    return render(request, "poll_app/create.html", context=context_dict)

def search(request):
    return render(request, "poll_app/search.html")

def register(request):
    form = UserProfileForm()

    if request.method == 'POST':
        print(request.POST)
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('poll_app:homepage'))
        else:
            print(form.errors)
    context_dict = {'form': form}
    
    return render(request, 'poll_app/register.html', context_dict)

def login(request):
    return render(request, "poll_app/login.html")

#This is a placeholder view. Feel free to replace with a logout view.
def logout(request):
    return render(request, "poll_app/logout.html")

def account(request):
    return render(request, "poll_app/account.html")

def vote(request, poll_slug):
    poll = Poll.objects.get(poll_slug=poll_slug)
    context_dict = {"poll": poll}
    return render(request, "poll_app/vote.html", context=context_dict)

def user(request, user_id):

    profile = UserProfile.objects.get(id=user_id)
    polls = Poll.objects.filter(submitter=profile.id)

    polls = pollarizing(polls)

    context_dict = {"profile": profile,
                    "user_polls": polls}

    champion = pollarizing(Poll.objects.all())[0].submitter

    if profile.id == champion.id:
        context_dict["is_champion"] = True

    no_polls = len(polls)
    if no_polls == 1:
        context_dict["no_polls"] = "1 poll"
    else:
        context_dict["no_polls"] = str(no_polls) + " polls"

    no_votes = 0
    for poll in polls:
        no_votes += (poll.votes1 + poll.votes2)

    if no_votes < 1000:
        votesString = str(no_votes) + " votes"
    elif no_votes < 1000000:
        votesString = str(round((no_votes / 1000), 1)) + "K votes"
    else:
        votesString = str(round((no_votes / 1000000), 1)) + "M votes"

    context_dict["no_votes"] = votesString

    response = render(request, 'poll_app/user.html', context=context_dict)
    return response


    #Test code
    return render(request, "poll_app/rankings.html", context=context_dict)

class ResultsView(View):

    def get(self, request, poll_slug):
        user = request.user
        context_dict = {}
        try:
            comment_list = []
            poll = Poll.objects.get(poll_slug=poll_slug)
            comments = Comment.objects.filter(poll=poll, parent=None).order_by("-votes")
            try:
                votes_in = VotesIn.objects.get(poll=poll, user=user)
                context_dict["votes_in"] = votes_in
            except:
                pass
            for comment in comments:
                comment_dict = {}
                submitter = comment.submitter
                try:
                    submitter_vote_in = VotesIn.objects.get(poll=poll, user=submitter)
                    comment_dict["submitter_vote"] = submitter_vote_in
                except:
                    pass
                user_profile = UserProfile.objects.get(user=submitter)
                comment_dict["comment"] = comment
                comment_dict["children"] = len(Comment.objects.filter(parent=comment))
                comment_dict["image"] = user_profile.profile_image.url
                comment_list.append(comment_dict)
            context_dict["poll"] = poll
            context_dict["comments"] = comment_list
            return render(request, "poll_app/comment.html", context=context_dict)
        except Poll.DoesNotExist:
            raise Http404("Poll question doesn't exist")


class VoteView(View):

    def get(self, request, poll_slug):
        context_dict = {}
        try:
            poll = Poll.objects.get(poll_slug=poll_slug)
            context_dict["poll"] = poll
            return render(request, "poll_app/vote.html", context=context_dict)
        except Poll.DoesNotExist:
            raise Http404("Poll question doesn't exist")



# JSON views here

class JSONPollResults(View):
    def get(self, request, poll_slug):
        try:
            the_poll = Poll.objects.get(poll_slug=poll_slug)
            dictionary = {
                "answer1": the_poll.answer1,
                "votes1": the_poll.votes1,
                "answer2": the_poll.answer2,
                "votes2": the_poll.votes2
            }
            return JsonResponse(dictionary)
        except Poll.DoesNotExist:
            raise Http404("Poll doesn't exist")



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

class JSONComments(View):

    def get(self, request, poll_slug):
        

        try:
            poll = Poll.objects.get(poll_slug=poll_slug)
            
            dictionary = {"poll": poll.question, "comments": []}
            
            comments = Comment.objects.filter(poll=poll, parent=None).order_by("-votes")

            for comment in comments:
                the_user = comment.submitter
                user_profile = UserProfile.objects.get(user=the_user)
                new_object = { 
                    "id": comment.id, 
                    "comment": comment.comment, 
                    "submitter": the_user.username,
                    "profile_image": user_profile.profile_image.url, 
                    "votes": comment.votes, 
                    "parent": comment.parent
                    }
                dictionary["comments"].append(new_object)
        
        except Comment.DoesNotExist:
            raise Http404("Comments were not found")

        except Poll.DoesNotExist:
            raise Http404("Poll does not exist")

        return JsonResponse(dictionary)

    def post(self, request, poll_slug):
        comment = request.POST["comment"]
        return HttpResponse(comment)

def add_comment(request):
    context_dict = {}
    if request.method == "POST":
        print(request.POST)
        username = request.POST["submitter"]
        comment = request.POST["comment"]
        poll_slug = request.POST["poll"]
        children = int(request.POST["children"])
        parent = request.POST["parent"]
        if parent != "":
            parent = int(parent)
            the_parent = Comment.objects.get(id=parent)
        else:
            the_parent = None

        

        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)

        the_poll = Poll.objects.get(poll_slug=poll_slug)

        new_comment = Comment.objects.create(submitter=user, comment=comment, poll=the_poll, parent=the_parent)
        new_comment.save()

        context_dict["profile_image"] = user_profile.profile_image.url
        context_dict["comment_id"] = new_comment.id
        context_dict["children"] = children + 1
        context_dict["message"] = "SUCCESS"

        return JsonResponse(context_dict)

def add_comment_votes(request):
    context_dict = {}
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        comment_id = request.POST["id"]
        votes = request.POST["votes"]
        poll_slug = request.POST["poll_slug"]
        vote_amount = int(request.POST["vote_amount"])
        the_poll = Poll.objects.get(poll_slug=poll_slug)
        the_comment = Comment.objects.get(id=comment_id)
        try:
            votes_in = VotesInComment.objects.get(user=user, poll=the_poll, comment=the_comment)
            old_vote = votes_in.old_votes
            if old_vote == 1:
                the_comment.votes -= 1
            else:
                the_comment.votes += 1
            voted_before = True
            votes_in.delete()
        except VotesInComment.DoesNotExist:
            votes_in = VotesInComment.objects.create(user=user, poll=the_poll, comment=the_comment)
            votes_in.old_votes = vote_amount
            votes_in.save()
            the_comment.votes += vote_amount
            voted_before = False
        the_comment.save()
        context_dict = {"votes": the_comment.votes, "voted_before": voted_before }
        return JsonResponse(context_dict)



class JSONChildComments(View):

    def get(self, request, comment_id):
        
        try:
            parent_comment = Comment.objects.get(id=comment_id)
            

            dictionary = {"parent": parent_comment.id, "poll_question": parent_comment.poll.question, "comments":[]}
            
            child_comments = Comment.objects.filter(parent=parent_comment).order_by("-votes")

            for comment in child_comments:
                the_user = comment.submitter
                user_profile = UserProfile.objects.get(user=the_user)
                new_object = { 
                    "id": comment.id, 
                    "comment": comment.comment, 
                    "submitter": the_user.username, 
                    "profile_image": user_profile.profile_image.url, 
                    "votes": comment.votes,
                    }
                dictionary["comments"].append(new_object)

        except Comment.DoesNotExist:
            raise Http404("no_comment")

        return JsonResponse(dictionary)


def JSONAddVote(request):
    context_dict = {}
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        poll_slug = request.POST["poll_slug"]
        answer_id = request.POST["answer_id"]
        the_answer = request.POST["the_answer"]
        the_poll = Poll.objects.get(poll_slug=poll_slug)
        try:
            vote_in = VotesIn.objects.get(poll=the_poll, user=user)
            old_answer = vote_in.option
            vote_in.option = the_answer
            if old_answer != the_answer:
                if answer_id == "answer1":
                    the_poll.votes2 -= 1
                    the_poll.votes1 += 1
                else:
                    the_poll.votes1 -= 1
                    the_poll.votes2 += 1
        except VotesIn.DoesNotExist:
            vote_in = VotesIn.objects.create(poll=the_poll, user=user, option=the_answer)
            if answer_id == "answer1":
                the_poll.votes1 += 1
            else:
                the_poll.votes2 += 1
        finally:
            vote_in.save()
            the_poll.save()
    return HttpResponse("Success")

def JSONSearch(request):
    context_dict = {"polls": []}
    if request.method == "POST":
        search_term = request.POST["search_term"]
        the_polls = Poll.objects.filter(question__contains=search_term)
        for poll in the_polls:
            poll_dict = {
                "question": poll.question,
                "question_link": reverse('poll_app:results', kwargs={"poll_slug": poll.poll_slug})
            }
            context_dict["polls"].append(poll_dict)
        return JsonResponse(context_dict)




    
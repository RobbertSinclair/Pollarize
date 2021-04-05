from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.views import View
from poll_app.models import Poll, Comment, UserProfile, VotesIn, VotesInComment
from poll_app.forms import CreatePollForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse
from django.db.utils import IntegrityError
import random
from django.contrib.auth import authenticate, login, logout
import re

# Create your views here.


# Sort polls by popularity and return sorted list
def popular(polls):
    popular = [(poll, poll.votes1 + poll.votes2) for poll in polls]
    popular = sorted(popular, key=lambda x: x[1], reverse=True)
    return [poll[0] for poll in popular]


# Sort polls by pollarizing (closeness to 50/50 answer rate) and return sorted list
def pollarizing(polls):
    # Calculate and sort by difference of percentage of option 1 with 50% (ascending order)
    pollarizing = [(poll, pollarizing_score(poll)) for poll in popular(polls)]
    pollarizing = sorted(pollarizing, key=lambda x: x[1])
    return [poll[0] for poll in pollarizing]


# Calculate score of each poll for pollarizing
def pollarizing_score(poll):
    total = poll.votes1 + poll.votes2
    if total == 0:
        return 100
    return abs(((poll.votes1 / (total)) * 100) - 50)


# Sort polls by recency and exclude future polls (with publish time after current time)
def recent_polls(polls):
    polls = polls.order_by('-pub_date')
    return list(polls)


# Format votes string on about page depending on number of votes
def votes_string(no_votes):
    if no_votes < 1000:
        return str(no_votes) + " votes"
    # Round to nearest 100 with more than 1,000 votes
    elif no_votes < 1000000:
        return str(round((no_votes / 1000), 1)) + "K votes"
    # Round to nearest 100,000 with more than 1,000,000 votes
    else:
        return str(round((no_votes / 1000000), 1)) + "M votes"



#Empty URL redirects to homepage
def index(request):
    return redirect("poll_app:home")


def homepage(request):
    # Get all polls not from the future
    polls = Poll.objects.filter(pub_date__lt=timezone.now())

    # Get recent polls
    recent = recent_polls(polls)[:3]

    # Get pollarizing and popular polls
    popular_polls = popular(polls)[:3]
    pollarizing_polls = pollarizing(polls)[:3]

    #Populate dictionary
    context_dict = {"recent": recent,
                    "popular": popular_polls,
                    "pollarizing": pollarizing_polls}

    #Create response render
    response = render(request, 'poll_app/index.html', context=context_dict)
    return response


#About page
def about(request):
    return render(request, "poll_app/about.html")


def rankings(request):

    polls = Poll.objects.filter(pub_date__lt=timezone.now())
    # Get recent polls
    recent = recent_polls(polls)[:10]

    # Get pollarizing and popular polls
    popular_polls = popular(polls)[:10]
    pollarizing_polls = pollarizing(polls)

    #Get most pollarizing poll as champion to show separately on page
    champion = pollarizing_polls[0]

    # Remove champion poll from secondary list if there are enough polls to fill space
    if len(pollarizing_polls) > 10:
        pollarizing_polls = pollarizing_polls[1:11]
    else:
        pollarizing_polls = pollarizing_polls[:10]

    #Populate dictionary
    context_dict = {"champion": champion,
                    "recent": recent,
                    "popular": popular_polls,
                    "pollarizing": pollarizing_polls}

    #Create response render
    response = render(request, 'poll_app/rankings.html', context=context_dict)
    return response

def random_poll(request):
    # Get a random poll
    polls = Poll.objects.filter(pub_date__lt=timezone.now())
    the_poll = random.choice(polls)
    the_slug = the_poll.poll_slug

    return redirect("poll_app:vote", poll_slug=the_slug)

@login_required
def create(request):
    #Initialise dictionary, form and user
    context_dict = {}

    form = CreatePollForm()
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('poll_app:login'))
    form = CreatePollForm(request.POST or None)
    if form.is_valid():
        poll_list = Poll.objects.order_by("id")
        if request.method == 'POST':
            obj = form.save(commit=False)
            obj.submitter = user
            obj.pub_date = timezone.now()
            obj.poll_slug = slugify(obj.question)
            obj.save(force_insert=True)
            obj.save(update_fields=['question','answer1','answer2'])
            
            form = CreatePollForm()
            poll = Poll.objects.get(id=(obj.id))
            context_dict = {"poll": poll}
            return redirect("poll_app:vote", poll_slug=obj.poll_slug)
            
    context_dict['form'] = form

    if request.method == 'POST':
        #Get form information and create poll object
        form = CreatePollForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.submitter = user
            obj.pub_date = timezone.now()
            obj.poll_slug = slugify(obj.question)
            obj.save()
            #Redirect to vote page
            return redirect(reverse("poll_app:vote", kwargs={'poll_slug': obj.poll_slug}))

        else:
            print(form.errors)

    #If not POST request, show create form
    context_dict['form'] = form
    return render(request, "poll_app/create.html", context=context_dict)

def search(request):

    #Define list of stopwords not considered by the search
    stopwords = ["a", "and", "by", "be", "to", "the", "of", "that", "i", "not", "for", "on", "as", "do", "at", "but"]
    #Maximum number of polls and accounts in results
    poll_results_limit = 10
    account_results_limit = 10

    if request.method == 'POST':
        #Get search input
        query = request.POST.get('query')
        #If empty, show results page
        if len(query) == 0:
            return redirect(reverse("poll_app:rankings"))

        #If query is exact match for a poll, go to polls vote page
        try:
            poll = Poll.objects.get(question=query)
            if (poll.pub_date > timezone.now()):
                raise Http404("Can't access poll")
            return redirect(reverse("poll_app:vote", kwargs={'poll_slug': poll.poll_slug}))

        except Poll.DoesNotExist:
            #Get all polls and accounts
            polls = Poll.objects.filter(pub_date__lt=timezone.now())
            polls = popular(polls)
            users = UserProfile.objects.all()

            #Initialise lists
            found_polls = []
            found_users = []

            #Split search into individual words
            query_args = query.lower().split(" ")
            for arg in query_args:
                #Search all non-stopwords
                if not arg in stopwords:
                    #Don't loop if maximum number of polls already found
                    if len(found_polls) <= poll_results_limit:
                        for poll in polls:
                            #If we find a new match, add it to the list
                            if not (poll in found_polls) and re.search(arg, poll.question, re.IGNORECASE):
                                found_polls.append(poll)
                                #Break if we've found enough polls
                                if len(found_polls) >= poll_results_limit:
                                    break

                    # Don't loop if maximum number of accounts already found
                    if len(found_users) <= account_results_limit:
                        for acc in users:
                            # If we find a new match, add it to the list
                            if not (acc in found_users) and re.search(arg, acc.user.username, re.IGNORECASE):
                                found_users.append(acc)
                                # Break if we've found enough polls
                                if len(found_users) >= account_results_limit:
                                    break
            #Build dictionary and return search page
            context_dict = {
                "query": query,
                "polls": found_polls,
                "users": found_users
            }
            return render(request, "poll_app/search.html", context=context_dict)

    #Return empty search page if there is no post
    return render(request, "poll_app/search.html")

def register(request):
    #Initialise form
    form = UserProfileForm()

    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        #Create new user from form values
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            try:
                user_profile.user = request.user
                user_profile.save()
            except IntegrityError:
                the_file = request.FILES["profile_image"]
                old_profile = UserProfile.objects.get(user=request.user)
                old_profile.profile_image = the_file
                old_profile.save()

            return redirect(reverse('poll_app:home'))
        else:
            print(form.errors)
    else:
        #If user has no profile picture, set it to the default
        user = request.user
        if user.is_authenticated:
            profile = UserProfile.objects.get_or_create(user=request.user)[0]
            if not profile.profile_image:
                profile.profile_image = 'default.png'
                profile.save()

    context_dict = {'form': form}
    return render(request, 'poll_app/registration.html', context_dict)

def login_view(request, error=None):
    if request.method == 'POST':
        #Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        #Check credentials
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('poll_app:home'))
            else:
                #Re-render login page with error if account disabled
                return render(request, 'poll_app/login.html',
                context={"error": "Your Pollarize account is disabled."})
        else:
            # Re-render login page with error if password doesn't match
            return render(request, 'poll_app/login.html', context = {"error": "Your username and password don't match, try again"})
    else:
        return render(request, 'poll_app/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('poll_app:home'))

@login_required
def account(request):
    #Get user profile
    user = request.user
    profile = UserProfile.objects.get(user=user)
    context_dict = {"profile": profile}

    if request.method == 'POST':
        #Check if password is correct
        password = request.POST.get('password')
        user = authenticate(username=user.username, password=password)

        #If correct, log out and delete account
        if user:
            logout(request)
            try:
                user_to_delete = User.objects.get(username=user.username)
                user_to_delete.delete()
            except:
                print("User not found")

            return redirect(reverse('poll_app:home'))
        else:
            #Re-render account page with error if password is wrong
            context_dict["error"] = "Couldn't delete account, did you enter your password correctly?"

    #Build dictionary and render page
    context_dict["polls"] = len(Poll.objects.filter(submitter=user))
    context_dict["votes_in"] = len(VotesIn.objects.filter(user=user))
    context_dict["comments"] = len(Comment.objects.filter(submitter=user))
    return render(request, "poll_app/account.html", context=context_dict)


def vote(request, poll_slug):

    #Check poll exists and get poll info
    try:
        poll = Poll.objects.get(poll_slug=poll_slug)
        if(poll.pub_date > timezone.now()):
            raise Http404("Can't access poll")
        context_dict = {"poll": poll}
    except Poll.DoesNotExist:
        raise Http404("Poll Does not exist")

    # Redirect to results or vote page depending on if logged in
    if request.user.is_authenticated:
        return render(request, "poll_app/vote.html", context=context_dict)
    else:
        return redirect("poll_app:results", poll_slug=poll_slug)

def user(request, user_id):

    # Get user and all their polls
    profile = UserProfile.objects.get(id=user_id)
    polls = Poll.objects.filter(submitter=profile.id, pub_date__lt=timezone.now())

    # Sort by pollarizing
    polls = pollarizing(polls)

    # Create and populate dictionary
    context_dict = {"profile": profile,
                    "user_polls": polls}

    # Check if user is pollarize champion
    champion = pollarizing(Poll.objects.all())[0].submitter
    if profile.id == champion.id:
        context_dict["is_champion"] = True

    # Format text for number of polls
    no_polls = len(polls)
    if no_polls == 1:
        context_dict["no_polls"] = "1 poll"
    else:
        context_dict["no_polls"] = str(no_polls) + " polls"

    #Get total number of votes on all user polls
    no_votes = 0
    for poll in polls:
        no_votes += (poll.votes1 + poll.votes2)

    #Fill dictionary and return response
    context_dict["no_votes"] = votes_string(no_votes)
    response = render(request, 'poll_app/user.html', context=context_dict)
    return response

class ResultsView(View):

    def get(self, request, poll_slug):
        user = request.user
        context_dict = {}
        try:
            #Get all comments for given poll
            comment_list = []
            poll = Poll.objects.get(poll_slug=poll_slug)
            comments = Comment.objects.filter(poll=poll, parent=None).order_by("-votes")
            #Check if user has voted in poll
            try:
                votes_in = VotesIn.objects.get(poll=poll, user=user)
                context_dict["votes_in"] = votes_in
            except:
                pass
            #Build up dictionary of information for each comment
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
        #Return 404 if poll doesn't exist
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
            #Get and return poll information
            the_poll = Poll.objects.get(poll_slug=poll_slug)
            votes_in = VotesIn.objects.filter(poll=the_poll).order_by("-vote_time")
            latest = votes_in[0]
            dictionary = {
                "answer1": the_poll.answer1,
                "votes1": the_poll.votes1,
                "answer2": the_poll.answer2,
                "votes2": the_poll.votes2,
                "latest_user": latest.user.username,
                "latest_option": latest.option,
            }
            return JsonResponse(dictionary)
        except IndexError:
            #If no latest vote, return the other information
            dictionary = {
                "answer1": the_poll.answer1,
                "votes1": the_poll.votes1,
                "answer2": the_poll.answer2,
                "votes2": the_poll.votes2
            }
            return JsonResponse(dictionary)
        except Poll.DoesNotExist:
            #Raise 404 if poll doesn't exist
            raise Http404("Poll doesn't exist")



class JSONRandomPoll(View):

    def get(self, request):
        try:
            #Get a random poll and return its details
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
            #Get all non-reply comments for poll
            comments = Comment.objects.filter(poll=poll, parent=None).order_by("-votes")

            for comment in comments:
                the_user = comment.submitter
                user_profile = UserProfile.objects.get(user=the_user)
                VoteIn = VotesIn.objects.get(user=the_user, poll=poll)
                new_object = { 
                    "id": comment.id, 
                    "comment": comment.comment, 
                    "submitter": the_user.username,
                    "profile_image": user_profile.profile_image.url, 
                    "votes": comment.votes, 
                    "parent": comment.parent,
                    }
                try:
                    #Get commenters vote in poll
                    VoteIn = VotesIn.objects.get(user=the_user, poll=poll)
                    new_object["option"] = VoteIn.option
                except VotesIn.DoesNotExist:
                    new_object["option"] = None
                dictionary["comments"].append(new_object)
        #404 if comments or polls don't exist
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
    #Create comment from POST info
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
        #Return response to js file
        context_dict["profile_image"] = user_profile.profile_image.url
        context_dict["comment_id"] = new_comment.id
        context_dict["children"] = children + 1
        try:
            vote_in = VotesIn.objects.get(user=user, poll=the_poll)
            context_dict["vote_option"] = vote_in.option
        except VotesIn.DoesNotExist:
            context_dict["vote_option"] = None
        context_dict["message"] = "SUCCESS"

        return JsonResponse(context_dict)

def add_comment_votes(request):
    context_dict = {}
    user = request.user
    #Get POST information
    if request.method == "POST" and user.is_authenticated:
        comment_id = request.POST["id"]
        votes = request.POST["votes"]
        poll_slug = request.POST["poll_slug"]
        vote_amount = int(request.POST["vote_amount"])
        the_poll = Poll.objects.get(poll_slug=poll_slug)
        the_comment = Comment.objects.get(id=comment_id)
        try:
            #Change vote value depending on last vote
            votes_in = VotesInComment.objects.get(user=user, poll=the_poll, comment=the_comment)
            old_vote = votes_in.old_votes
            if old_vote == 1:
                the_comment.votes -= 1
            else:
                the_comment.votes += 1
            voted_before = True
            votes_in.delete()
            #If no previous vote, create one
        except VotesInComment.DoesNotExist:
            votes_in = VotesInComment.objects.create(user=user, poll=the_poll, comment=the_comment)
            votes_in.old_votes = vote_amount
            votes_in.save()
            the_comment.votes += vote_amount
            voted_before = False
        the_comment.save()
        context_dict = {"votes": the_comment.votes, "voted_before": voted_before, "message": "SUCCESS" }
        return JsonResponse(context_dict)
    #Return login redirect if user is not logged in
    elif request.method == "POST" and not user.is_authenticated:
        context_dict = {"redirect_url": reverse("poll_app:login"), "message": "FAILURE"}
        return JsonResponse(context_dict)

def get_comment_votes(request, comment_id):
    context_dict = {}
    user = request.user
    #Get the current logged in users previous vote on a comment
    the_comment = Comment.objects.get(id=comment_id)
    the_poll = the_comment.poll
    if user.is_authenticated:
        try:
            votes_in = VotesInComment.objects.get(user=user, poll=the_poll, comment=the_comment)
            print(votes_in)
            context_dict["vote"] = votes_in.old_votes
        except VotesInComment.DoesNotExist:
            context_dict["vote"] = 0
    return JsonResponse(context_dict)



class JSONChildComments(View):

    def get(self, request, comment_id):
        
        try:
            parent_comment = Comment.objects.get(id=comment_id)
            

            dictionary = {"parent": parent_comment.id, "poll_question": parent_comment.poll.question, "comments":[]}
            #Get all child comments and create dictionary of their information
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
                try:
                    vote_in = VotesIn.objects.get(poll=parent_comment.poll, user=comment.submitter)
                    new_object["vote_option"] = vote_in.option
                except VotesIn.DoesNotExist:
                    new_object["vote_option"] = None

                if request.user.is_authenticated:
                    try:
                        user_vote = VotesInComment.objects.get(poll=parent_comment.poll, user=request.user, comment=comment)
                        new_object["user_vote"] = user_vote.old_votes
                    except VotesInComment.DoesNotExist:
                        new_object["user_vote"] = 0
                else:
                    new_object["user_vote"] = 0
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
        #Create link between user and poll
        try:
            vote_in = VotesIn.objects.get(poll=the_poll, user=user)
            old_answer = vote_in.option
            print(old_answer)
            vote_in.option = the_answer
            print(the_answer)
            #Update polls total votes
            if old_answer != the_answer:
                if answer_id == "answer1":
                    the_poll.votes2 -= 1
                    the_poll.votes1 += 1
                else:
                    the_poll.votes1 -= 1
                    the_poll.votes2 += 1
        #Create new object if first vote
        except VotesIn.DoesNotExist:
            vote_in = VotesIn.objects.create(poll=the_poll, user=user, option=the_answer)
            if answer_id == "answer1":
                the_poll.votes1 += 1
            else:
                the_poll.votes2 += 1
        finally:
            #Save vote
            vote_in.vote_time = timezone.now()
            vote_in.save()
            the_poll.save()
    return HttpResponse("Success")

def JSONSearch(request):
    #Compile list of matching polls and send response back
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

def JSONGetCurrentUser(request):
    #Send username of current user
    user = request.user
    context_dict = {"authenticated": user.is_authenticated}
    if user.is_authenticated:
        context_dict["username"] = user.username
    else:
        context_dict["username"] = None
    return JsonResponse(context_dict)

def JSONDeleteComment(request):
    #Delete comment if it exists
    if request.method == "POST":
        comment_id = request.POST["comment_id"]
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return HttpResponse("Success")
        except Comment.DoesNotExist:
            raise Http404("Comment Not Found")

    
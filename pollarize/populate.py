import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pollarize.settings")

from django.utils import timezone
from datetime import timedelta
from django.utils import timezone
import django
django.setup()
from poll_app.models import UserProfile, Comment, Poll, VotesIn
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import random

def populate():

    #List of accounts
    users = [
        {"username": "AdminUser", "password": "adminPass", "superuser": True},
        {"username": "Adamanatite", "password": "testPass1", "superuser": False},
        {"username": "ogra", "password": "testPass2", "superuser": False},
        {"username": "RobbertSinclair", "password": "testPass3", "superuser": False},
        {"username": "Ciaran-Carr", "password": "testPass4", "superuser": False},
        {"username": "PollMaster71", "password": "testPass5", "superuser": False}
    ]

    #List of polls
    polls = [
        {"question": "Does Pineapple belong on a pizza?", "answer1": "Yes", "answer2": "No", "votes1": random.randint(0, 100), "votes2": random.randint(0, 100), "submitter": "Adamanatite", "pub_date": (timezone.now())},
        {"question": "Star Wars or Star Trek?", "answer1": "Star Wars", "answer2": "Star Trek", "votes1": random.randint(501, 9999), "votes2": random.randint(501, 9999), "submitter": "ogra", "pub_date": (timezone.now() - timedelta(days=4))},
        {"question": "What are your thoughts on Marmite?", "answer1": "Love it", "answer2": "Hate it", "votes1": random.randint(500001, 999999), "votes2": random.randint(500001, 999999), "submitter": "RobbertSinclair", "pub_date": (timezone.now() - timedelta(days=3))},
        {"question": "Marvel or DC?", "answer1": "Marvel", "answer2": "DC Comics", "votes1": 932000, "votes2": 932001, "submitter": "Adamanatite", "pub_date": (timezone.now() - timedelta(days=random.randint(1, 28)))},
        {"question": "Can we keep this 50/50?", "answer1": "Yes", "answer2": "Yes but grey", "votes1": 300000, "votes2": 300000, "submitter": "PollMaster71", "pub_date": (timezone.now() - timedelta(days=10))},
        {"question": "can someone pleas vote on my poll please", "answer1": "Yes", "answer2": "No ur poll sucks", "votes1": 0, "votes2": 0, "submitter": "Adamanatite", "pub_date": (timezone.now())},
        {"question": "Who would win?", "answer1": "Every pokemon", "answer2": "One billion lions", "votes1": 13286, "votes2": 7400, "submitter": "Ciaran-Carr", "pub_date": (timezone.now() - timedelta(days=random.randint(1, 28)))},
        {"question": "How many holes does a straw have?", "answer1": "One Hole", "answer2": "Two Holes", "votes1": 1005993, "votes2": 410112, "submitter": "ogra", "pub_date": (timezone.now() - timedelta(days=random.randint(1, 28)))},
        {"question": "Is water wet?", "answer1": "Yes", "answer2": "No", "votes1": random.randint(99999, 999999), "votes2": random.randint(99999, 999999), "submitter": "RobbertSinclair", "pub_date": (timezone.now() + timedelta(days=random.randint(1, 28)))},
        {"question": "Which party are you voting?", "answer1": "Democrat", "answer2": "Republican", "votes1": random.randint(500001, 999999), "votes2": random.randint(500001, 999999), "submitter": "PollMaster71", "pub_date": (timezone.now() - timedelta(days=random.randint(1, 28)))},
        {"question": "Should education be mandatory?", "answer1": "Yes", "answer2": "No", "votes1": random.randint(500001, 999999), "votes2": random.randint(500001, 999999), "submitter": "ogra", "pub_date": (timezone.now() - timedelta(days=random.randint(1, 28)))}
    ]

    #List of poll comments
    comments = [
        {"id": 1, "submitter": "Adamanatite", "poll_question": "Does Pineapple belong on a pizza?", "comment": "I love pineapple on pizza. It is the tastiest thing on a pizza", "votes": 16, "parent": None},
        {"id": 2, "submitter": "ogra", "poll_question": "Does Pineapple belong on a pizza?", "comment": "You are wrong in so many ways.", "votes": 2, "parent": 1},
        {"id": 3, "submitter": "RobbertSinclair", "poll_question": "Does Pineapple belong on a pizza?", "comment": "I agree with the statement", "votes": 4, "parent": 1},
        {"id": 4, "submitter": "ogra", "poll_question": "Does Pineapple belong on a pizza?", "comment": "I think that pineapple on a pizza is a crime on humanity", "votes": 5, "parent": None},
        {"id": 5, "submitter": "Ciaran-Carr", "poll_question": "Does Pineapple belong on a pizza?", "comment": "It is all down to preference. I don't really like it but I think it belongs on a pizza", "votes": 1, "parent": None},
        {"id": 6, "submitter": "Ciaran-Carr", "poll_question": "Star Wars or Star Trek?", "comment": "Obi Wan never told you what happened to your father", "votes": 3, "parent": None},
        {"id": 7, "submitter": "Adamanatite", "poll_question": "Star Wars or Star Trek?", "comment": "He told me enough, he told me you killed him", "votes": 3, "parent": 6},
        {"id": 8, "submitter": "PollMaster71", "poll_question": "What are your thoughts on Marmite?", "comment": "I absolutely hate it!", "votes": 2, "parent": None},
        {"id": 9, "submitter": "Adamanatite", "poll_question": "What are your thoughts on Marmite?", "comment": "I love it", "votes": 3, "parent": None},
        {"id": 10, "submitter": "ogra", "poll_question": "Marvel or DC?", "comment": "Superman is a boring character", "votes": 25, "parent": None},
        {"id": 11, "submitter": "Adamanatite", "poll_question": "Marvel or DC?", "comment": "I disagree, he's just portrayed that way in many movies", "votes": 11, "parent": 10},
        {"id": 12, "submitter": "PollMaster71", "poll_question": "Who would win?", "comment": "One billion is a lot of lions", "votes": 1400, "parent": None},
        {"id": 13, "submitter": "Adamanatite", "poll_question": "Who would win?", "comment": "There are many legendary pokemon who could destroy any planet, lions have no chance", "votes": 15400, "parent": None},
        {"id": 14, "submitter": "RobbertSinclair", "poll_question": "Should education be mandatory?", "comment": "WAD2 should be mandatory!", "votes": 1654, "parent": None},
        {"id": 15, "submitter": "Adamanatite", "poll_question": "Should education be mandatory?", "comment": "I prefer ADS2", "votes": -511, "parent": 14},
        {"id": 16, "submitter": "Ciaran-Carr", "poll_question": "Should education be mandatory?", "comment": "Completely agree", "votes": 1225, "parent": 14}
    ]

    #List of user votes
    votes_in = [
        {"user": "Adamanatite", "poll": "Does Pineapple belong on a pizza?", "option": "Yes"},
        {"user": "ogra", "poll": "Does Pineapple belong on a pizza?", "option": "No"},
        {"user": "RobbertSinclair", "poll": "Does Pineapple belong on a pizza?", "option": "Yes"},
        {"user": "Ciaran-Carr", "poll": "Does Pineapple belong on a pizza?", "option": "Yes"},
        {"user": "Ciaran-Carr", "poll": "Star Wars or Star Trek?", "option": "Star Wars"},
        {"user": "Adamanatite", "poll": "Star Wars or Star Trek?", "option": "Star Wars"},
        {"user": "PollMaster71", "poll": "What are your thoughts on Marmite?", "option": "Hate it"},
        {"user": "Adamanatite", "poll": "What are your thoughts on Marmite?", "option": "Love it"},
        {"user": "Adamanatite", "poll": "Marvel or DC?", "option": "DC Comics"},
        {"user": "ogra", "poll": "Marvel or DC?", "option": "Marvel"},
        {"user": "PollMaster71", "poll": "Who would win?", "option": "One billion lions"},
        {"user": "Adamanatite", "poll": "Who would win?", "option": "Every pokemon"},
        {"user": "Adamanatite", "poll": "Should education be mandatory?", "option": "Yes"},
        {"user": "RobbertSinclair", "poll": "Should education be mandatory?", "option": "Yes"},
        {"user": "Ciaran-Carr", "poll": "Should education be mandatory?", "option": "Yes"},
        {"user": "PollMaster71", "poll": "Is water wet?", "option": "Yes"}
    ]

    #Add all information to database
    for user in users:
        u = add_user(user)
        print(f"{user['username']} created")

    for poll in polls:
        p = add_poll(poll)
        print(f"Poll with question {poll['question']} created")

    for comment in comments:
        c = add_comment(comment)
        print(f"Comment id {comment['id']} created")

    for vote_in in votes_in:
        v = add_votes_in(vote_in)
        print(f"Votes In element with Username: {vote_in['user']} on Poll: {vote_in['poll']} created")

    
def add_user(user):
    u = User.objects.create_user(user["username"], password=user["password"])
    u.is_superuser = user["superuser"]
    u.is_staff = user["superuser"]
    u.save()
    profile = UserProfile.objects.create(user=u)
    profile.save()
    return u

def add_poll(poll):
    submitter = User.objects.get(username=poll["submitter"])
    slug = slugify(poll["question"])
    p = Poll.objects.get_or_create(
        question=poll["question"], 
        answer1=poll["answer1"],
        answer2=poll["answer2"],
        votes1=poll["votes1"],
        votes2=poll["votes2"],
        submitter=submitter,
        poll_slug=slug,
        pub_date=poll["pub_date"]
        )[0]
    p.save()
    return p

def add_comment(comment):
    if comment["parent"] != None:
        parent_comment = Comment.objects.get(id=comment["parent"])
    else:
        parent_comment = None
    poll = Poll.objects.get(question=comment["poll_question"])
    user = User.objects.get(username=comment["submitter"])
    c = Comment.objects.get_or_create(
        id=comment["id"],
        submitter=user,
        comment=comment["comment"],
        votes=comment["votes"],
        poll=poll,
        parent=parent_comment
        )[0]
    
    return c

def add_votes_in(vote_in):
    user = User.objects.get(username=vote_in['user'])
    poll = Poll.objects.get(question=vote_in['poll'])
    v = VotesIn.objects.get_or_create(
        user=user,
        poll=poll,
        option=vote_in['option']
    )[0]
    return v


if __name__ == "__main__":
    print("Starting Pollarize population script...")
    populate()
    



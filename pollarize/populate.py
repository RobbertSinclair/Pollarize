import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pollarize.settings")

from django.utils import timezone
from datetime import timedelta
from django.utils import timezone
import django
django.setup()
from poll_app.models import UserProfile, Comment, Poll
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import random

def populate():
    
    users = [
        {"username": "AdminUser", "password": "adminPass", "superuser": True},
        {"username": "testUser1", "password": "testPass1", "superuser": False},
        {"username": "testUser2", "password": "testPass2", "superuser": False},
        {"username": "testUser3", "password": "testPass3", "superuser": False},
        {"username": "testUser4", "password": "testPass4", "superuser": False},
        {"username": "testUser5", "password": "testPass5", "superuser": False}
    ]
    
    polls = [
        {"question": "Does Pineapple belong on a pizza?", "answer1": "Yes", "answer2": "No", "votes1": random.randint(0, 100), "votes2": random.randint(0, 100), "submitter": "testUser1"},
        {"question": "Star Wars or Star Trek?", "answer1": "Star Trek", "answer2": "Star Wars", "votes1": random.randint(501, 9999), "votes2": random.randint(501, 9999), "submitter": "testUser2", "pub_date": (timezone.now() - timedelta(days=1))},
        {"question": "What are your thoughts on Marmite?", "answer1": "Love it", "answer2": "Hate it", "votes1": random.randint(500001, 999999), "votes2": random.randint(500001, 999999), "submitter": "testUser3", "pub_date": (timezone.now() - timedelta(days=3))}
    ]

    comments = [
        {"id": 1, "submitter": "testUser1", "poll_question": "Does Pineapple belong on a pizza?", "comment": "I love pineapple on pizza. It is the tastiest thing on a pizza", "votes": 16, "parent": None},
        {"id": 2, "submitter": "testUser2", "poll_question": "Does Pineapple belong on a pizza?", "comment": "You are wrong in so many ways.", "votes": 2, "parent": 1},
        {"id": 3, "submitter": "testUser3", "poll_question": "Does Pineapple belong on a pizza?", "comment": "I agree with the statement", "votes": 4, "parent": 1},
        {"id": 4, "submitter": "testUser2", "poll_question": "Does Pineapple belong on a pizza?", "comment": "I think that pineapple on a pizza is a crime on humanity", "votes": 5, "parent": None},
        {"id": 5, "submitter": "testUser3", "poll_question": "Does Pineapple belong on a pizza?", "comment": "It is all down to preference. I don't really like it but I think it belongs on a pizza", "votes": 1, "parent": None},
        {"id": 6, "submitter": "testUser4", "poll_question": "Star Wars or Star Trek?", "comment": "Obi Wan never told you what happened to your father", "votes": 3, "parent": None},
        {"id": 7, "submitter": "testUser1", "poll_question": "Star Wars or Star Trek?", "comment": "He told me enough, he told me you killed him", "votes": 3, "parent": 6},
        {"id": 8, "submitter": "testUser5", "poll_question": "What are your thoughts on Marmite?", "comment": "I absolutely hate it!", "votes": 2, "parent": None},
        {"id": 9, "submitter": "testUser1", "poll_question": "What are your thoughts on Marmite?", "comment": "I love it", "votes": 3, "parent": None}
    ]

    for user in users:
        u = add_user(user)
        print(f"{user['username']} created")

    for poll in polls:
        p = add_poll(poll)
        print(f"Poll with question {poll['question']} created")

    for comment in comments:
        c = add_comment(comment)
        print(f"Comment id {comment['id']} created")

    
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
        poll_slug=slug
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

if __name__ == "__main__":
    print("Starting Pollarize population script...")
    populate()
    



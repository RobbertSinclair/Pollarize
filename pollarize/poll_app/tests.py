from django.test import TestCase
from poll_app.models import UserProfile, Poll, VotesIn, VotesInComment, Comment
from django.contrib.auth.models import User
from django.urls import reverse
import json

class PollModelTests(TestCase):

    def test_slug_creation(self):
        user = User(username="testUser1", password="testPass1")
        user.save()
        the_poll = Poll(question="Random Test Poll", submitter=user, answer1="left", answer2="right")
        the_poll.save()

        self.assertEqual(the_poll.slug, 'random-test-poll')

    def test_total_votes(self):
        user = User(username="testUser1", password="testPass1")
        user.save()
        the_poll = Poll(question="Random Test Poll", submitter=user, answer1="left", answer2="right")
        the_poll.save()
        
        self.assertEqual(the_poll.votes1 + the_poll.votes2, 0)

    def test_votes_not_negative(self):
        user = User(username="testUser1", password="testPass1")
        user.save()
        the_poll = Poll(question="Random Test Poll", submitter=user, answer1="left", votes1=-1, votes2=0)
        the_poll.save()

        self.assertEqual((the_poll.votes1 >= 0), True)
        self.assertEqual((the_poll.votes2 >= 0), True)

class CommentModelTests(TestCase):

    def setUp(self):
        self.the_user = User.objects.create(username="testUserComments", password="testCommPass")
        self.the_user.save()

    def check_comment_belongs_to_poll(self):
        the_comment = Comment(comment="Hello World", poll=None, user=self.the_user, votes=0)

        self.assertEqual(the_comment.poll, True)



#JSON View Tests

class JSONRepliesViewTests(TestCase):

    def setUp(self):
        the_user = User.objects.get_or_create(username="JSONRepliesUser", password="json")[0]
        
        the_user.save()
        user_profile = UserProfile.objects.get_or_create(user=the_user)[0]
        user_profile.save()
        the_poll = Poll.objects.get_or_create(question="Test Poll", submitter=the_user, answer1="left", answer2="right", votes1=0, votes2=1)[0]
        the_poll.save()
        the_comment = Comment.objects.get_or_create(poll=the_poll, submitter=the_user, comment="TestComm1", votes=0)[0]
        the_comment.parent = the_comment
        the_comment.save()
        the_reply = Comment.objects.get_or_create(poll=the_poll, submitter=the_user, comment="TestReply", votes=0, parent=the_comment)[0]
        the_reply.save()

    def test_correct_response(self):
        the_comment = Comment.objects.get(comment="TestComm1")
        print(the_comment.id)
        response = self.client.get(reverse("poll_app:json-child-comments", args=[the_comment.id]))
        json_dict = json.loads(response.content)
        the_replies = Comment.objects.filter(parent=the_comment.id)
        reply_count = len(the_replies)
        print(reply_count)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_dict["comments"]), reply_count)
        self.assertEqual(json_dict["parent"], the_comment.id)
        self.assertEqual(json_dict["poll_question"], the_comment.poll.question)

    def test_404_with_invalid_comment(self):
        response = self.client.get(reverse("poll_app:json-child-comments", args=[9999999999]))
        self.assertEqual(response.status_code, 404)

    def test_ensure_that_replies_are_not_the_same_as_the_parent(self):
        the_comment = Comment.objects.get(comment="TestComm1")
        response = self.client.get(reverse("poll_app:json-child-comments", args=[the_comment.id]))
        json_dict = json.loads(response.content)
        the_replies = Comment.objects.filter(parent=the_comment.id)
        self.assertEqual(response.status_code, 200)
        for reply in json_dict["comments"]:
            self.assertEqual((reply["id"] == the_comment.id), False)
        
class JSONPollResultsTests(TestCase):

    def setUp(self):
        user = User.objects.get_or_create(username="testUser", password="testPass")[0]
        user.save()
        profile = UserProfile.objects.get_or_create(user=user)[0]
        profile.save()
        the_poll = Poll.objects.create(question="The Question for this test", answer1="left", answer2="right", user=user)
        the_poll.save()
    
    def test_correct_response(self):
        the_poll = Poll.objects.get(question="The Question for this test")
        print(the_poll)
        the_slug = the_poll.poll_slug
        print(the_slug)
        response = self.client.get(reverse("poll_app:json-results", kwargs={"poll_slug": the_slug}))
        self.assertEqual(response.status_code, 200)
        json_dict = json.loads(response.content)
        print(json_dict)



    


        

# Create your tests here.

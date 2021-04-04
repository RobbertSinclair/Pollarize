from django.test import TestCase, Client
from poll_app.models import UserProfile, Poll, VotesIn, VotesInComment, Comment
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
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
        self.the_poll = Poll(question="Random Test Poll", submitter=self.the_user, answer1="left", votes1=-1, votes2=0)
        self.the_poll.save()

    def test_check_comment_belongs_to_poll(self):
        the_comment = Comment(comment="Hello World", poll=self.the_poll, submitter=self.the_user, votes=0)
        the_comment.save()
        self.assertEqual((the_comment.poll != None), True)

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
        the_poll = Poll.objects.create(id=250, question="The Question for this test", answer1="left", answer2="right", submitter=user)
        the_poll.poll_slug = slugify(the_poll.question)
        the_poll.save()
    
    def test_correct_response(self):
        slug = slugify("The Question for this test")
        the_poll = Poll.objects.get(id=250)
        print(the_poll)
        the_slug = the_poll.poll_slug
        print(the_slug)
        response = self.client.get(reverse("poll_app:json-results", kwargs={"poll_slug": slug}))
        self.assertEqual(response.status_code, 200)
        json_dict = json.loads(response.content)
        self.assertEqual(json_dict["answer1"], the_poll.answer1)
        self.assertEqual(json_dict["votes1"], the_poll.votes1)
        self.assertEqual(json_dict["answer2"], the_poll.answer2)
        self.assertEqual(json_dict["votes2"], the_poll.votes2)

class JSONAddComment(TestCase):

    def setUp(self):
        self.user = User.objects.get_or_create(username="testUser", password="testPass")[0]
        self.user.save()
        self.profile = UserProfile.objects.get_or_create(user=self.user)[0]
        self.profile.save()
        self.poll = Poll.objects.get_or_create(id=251, question="The Question for this test", answer1="left", answer2="right", submitter=self.user)[0]
        self.poll.poll_slug = slugify(self.poll.question)
        self.poll.save()

    def test_update_comment(self):
        test_data = {
            "comment": "Hello World",
            "poll": self.poll.poll_slug,
            "submitter": self.user.username,
            "parent": "",
            "children": 0
        }
        print(test_data)
        slug = self.poll.poll_slug
        response = self.client.post(reverse("poll_app:add-comment"), test_data)
        self.assertEqual(response.status_code, 200)
        try:
            the_comment = Comment.objects.get(poll=self.poll, submitter=self.user, comment=test_data["comment"])
            exists = True
        except Comment.DoesNotExist:
            exists = False
        self.assertEqual(exists, True)

class ResultView(TestCase):

    def setUp(self):
        self.the_user = User.objects.get_or_create(username="testUser", password="testPass")[0]
        self.the_user.save()
        self.the_user_profile = UserProfile.objects.get_or_create(user=self.the_user)[0]
        self.the_user_profile.save()
        self.the_poll = Poll.objects.get_or_create(submitter=self.the_user, question="Test Poll", answer1="Yes", answer2="No")[0]
        self.the_poll.poll_slug = slugify(self.the_poll.question)
        self.the_poll.save()
        self.main_comment = Comment.objects.get_or_create(submitter=self.the_user, poll=self.the_poll, comment="Main Comment", votes=0)[0]
        self.main_comment.save()
        self.reply_comment = Comment.objects.get_or_create(submitter=self.the_user, poll=self.the_poll, comment="Reply Comment", votes=0, parent=self.main_comment)[0]
        self.reply_comment.save()
        self.other_main_comment = Comment.objects.get_or_create(submitter=self.the_user, poll=self.the_poll, comment="Other Main Comment", votes=0, parent=None)[0]
        self.other_main_comment.save()

    def test_404_if_poll_doesnt_exist(self):
        response = self.client.get(reverse("poll_app:results", kwargs={"poll_slug": "does-not-exist"}))
        self.assertEqual(response.status_code, 404)

    def test_poll_details_in_result_view(self):
        response = self.client.get(reverse("poll_app:results", kwargs={"poll_slug": self.the_poll.poll_slug}))
        self.assertEqual(response.status_code, 200)
        the_context = response.context
        self.assertEqual(the_context["poll"], self.the_poll)
    
    def test_poll_main_poll_comments_are_in_context(self):
        response = self.client.get(reverse("poll_app:results", kwargs={"poll_slug": self.the_poll.poll_slug}))
        self.assertEqual(response.status_code, 200)
        the_context = response.context
        print(response.context["comments"])
        self.assertEqual(len(the_context["comments"]), 2)
        for comment in the_context["comments"]:
            self.assertEqual(comment["comment"].parent, None)

class VoteView(TestCase):

    def setUp(self):
        self.user = User.objects.get_or_create(username="testUser", password="testPass")[0]
        self.user.save()
        self.client.force_login(self.user)
        self.profile = UserProfile.objects.get_or_create(user=self.user)[0]
        self.profile.save()
        self.poll = Poll.objects.get_or_create(submitter=self.user, question="Test Poll", answer1="Yes", answer2="No")[0]
        self.poll.poll_slug = slugify(self.poll.question)
        self.poll.save()

    def test_404_if_poll_does_not_exist(self):
        response = self.client.get(reverse("poll_app:vote", kwargs={"poll_slug": "does-not-exist"}))
        self.assertEqual(response.status_code, 404)

    def test_poll_details_in_context(self):
        response = self.client.get(reverse("poll_app:vote", kwargs={"poll_slug": self.poll.poll_slug}))
        self.assertEqual(response.status_code, 200)
        the_context = response.context
        self.assertEqual(the_context["poll"], self.poll)

    def test_poll_redirects_if_no_user_logs_in(self):
        self.client.logout()
        response = self.client.get(reverse("poll_app:vote", kwargs={"poll_slug": self.poll.poll_slug}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("poll_app:results", kwargs={"poll_slug": self.poll.poll_slug}))

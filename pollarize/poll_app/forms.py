from django import forms
from poll_app.models import UserProfile, Poll, Comment
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    comment = forms.CharField(help_text="Enter your comment here.")
    votes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ('comment',)

class PollForm(forms.ModelForm):
    question = forms.CharField(help_text="Enter a question")
    answer1 = forms.CharField(help_text="Answer 1")
    answer2 = forms.CharField(help_text="Answer 2")
    votes1 = forms.CharField(widget=forms.HiddenInput(), initial=0)
    votes2 = forms.CharField(widget=forms.HiddenInput(), initial=0)
    poll_slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Poll
        exclude = ('submitter',)

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('picture',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget.forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password",)




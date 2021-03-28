from django import forms
from poll_app.models import UserProfile, Poll, Comment
from django.contrib.auth.forms import User
from django.utils import timezone



class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('profile_image',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password",)

class CreatePollForm(forms.ModelForm):
    # user input
    question = forms.CharField(max_length=128, help_text="Please enter the poll question.") 
    answer1 = forms.CharField(max_length=5000, help_text="Please enter the first option.") 
    answer2 = forms.CharField(max_length=5000, help_text="Please enter the second option.") 

    # hidden fields
    votes1 = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    votes2 = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    poll_slug = forms.SlugField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Poll
        fields = ['question', 'answer1', 'answer2']


from django.urls import path
from poll_app import views
from poll_app.views import JSONRandomPoll, JSONPollByPopularity, JSONComments, JSONChildComments, TestView

app_name = "poll-app"

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:poll_slug>/test/", TestView.as_view(), name="test"),
    path("json/random/", JSONRandomPoll.as_view(), name="json-random"),
    path("json/poll-popular/", JSONPollByPopularity.as_view(), name="json-popularity"),
    path("json/<slug:poll_slug>/comments/", JSONComments.as_view(), name="json-comments"),
    path("json/<int:comment_id>/child-comments/", JSONChildComments.as_view(), name="json-child-comments"),
    path("json/add-comment/", views.add_comment, name="add-comment")
    
]
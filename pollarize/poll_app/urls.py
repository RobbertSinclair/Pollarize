from django.urls import path
from poll_app import views
from poll_app.views import JSONRandomPoll, JSONPollByPopularity, JSONComments, JSONChildComments

app_name = "poll-app"

urlpatterns = [
    path("", views.index, name="index"),
    path("json/random", JSONRandomPoll.as_view(), name="json-random"),
    path("json/poll-popular", JSONPollByPopularity.as_view(), name="json-popularity"),
    path("json/<slug:poll_slug>/comments", JSONComments.as_view(), name="json-comments"),
    path("json/<int:comment_id>/child-comments", JSONChildComments.as_view(), name="json-child-comments")
    
]
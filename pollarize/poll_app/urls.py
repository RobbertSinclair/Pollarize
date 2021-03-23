from django.urls import path
from poll_app import views
from poll_app.views import JSONRandomPoll, JSONPollByPopularity, JSONComments, JSONChildComments, ResultsView, add_votes, JSONPollResults

app_name = "poll_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:poll_slug>/results/", ResultsView.as_view(), name="results"),
    path("json/random/", JSONRandomPoll.as_view(), name="json-random"),
    path("json/poll-popular/", JSONPollByPopularity.as_view(), name="json-popularity"),
    path("json/<slug:poll_slug>/comments/", JSONComments.as_view(), name="json-comments"),
    path("json/<int:comment_id>/child-comments/", JSONChildComments.as_view(), name="json-child-comments"),
    path("json/add-comment/", views.add_comment, name="add-comment"),
    path("json/add-vote/", views.add_votes, name="add-vote"),
    path("json/<slug:poll_slug>/results/", JSONPollResults.as_view(), name="json-results")
    
]
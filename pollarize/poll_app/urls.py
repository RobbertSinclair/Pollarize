from django.urls import path
from poll_app import views
from poll_app.views import JSONRandomPoll, JSONPollByPopularity, JSONComments, JSONChildComments, ResultsView, JSONPollResults, VoteView, JSONAddVote

app_name = "poll_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.homepage, name="home"),
    path("about/", views.about, name="about"),
    path("rankings/", views.rankings, name="rankings"),
    path("random-poll/", views.random_poll, name="random"),
    path("create-poll/", views.create, name="create"),
    path("search/", views.search, name="search"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("account/", views.account, name="account"),
    path("<slug:poll_slug>/vote/", views.vote, name="vote"),
    path("user/<int:user_id>/", views.user, name="user"),
    path("<slug:poll_slug>/results/", ResultsView.as_view(), name="results"),
    path("json/random/", JSONRandomPoll.as_view(), name="json-random"),
    path("json/poll-popular/", JSONPollByPopularity.as_view(), name="json-popularity"),
    path("json/<slug:poll_slug>/comments/", JSONComments.as_view(), name="json-comments"),
    path("json/<int:comment_id>/child-comments/", JSONChildComments.as_view(), name="json-child-comments"),
    path("json/add-comment/", views.add_comment, name="add-comment"),
    path("json/add-comment-vote/", views.add_comment_votes, name="add-vote"),
    path("json/<slug:poll_slug>/results/", JSONPollResults.as_view(), name="json-results"),
    path("json/add-vote/", views.JSONAddVote, name="json-add-vote"),
    path("json/search/", views.JSONSearch, name="json-search")
    
]
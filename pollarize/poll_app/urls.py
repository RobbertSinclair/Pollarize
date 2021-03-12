from django.urls import path
from poll_app import views
from poll_app.views import JSONRandomPoll, JSONPollByPopularity

app_name = "poll-app"

urlpatterns = [
    path("", views.index, name="index"),
    path("json/random", JSONRandomPoll.as_view(), name="json-random"),
    path("json/poll-popular", JSONPollByPopularity.as_view(), name="json-popularity"),
    
]
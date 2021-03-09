from django.urls import path
from poll_app import views

app_name = "poll-app"

urlpatterns = [
    path("", views.index, name="index")
]
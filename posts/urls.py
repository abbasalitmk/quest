from django.urls import path
from . import views
from accounts.views import signin


urlpatterns = [
    path("", signin, name="login"),
    path("home/", views.home, name="home"),
    path("ask/", views.create_question, name="ask"),
    path("question/<int:question_id>/", views.show_question, name="question"),
    path("answer/<int:question_id>/", views.answer_question, name="answer"),
    path("like/<int:answer_id>/", views.like, name="like"),


]

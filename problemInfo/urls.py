from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProblemPost.as_view()),
]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.TestProblem.as_view()),
]
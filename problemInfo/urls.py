from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProblemInfoView.as_view()),
]

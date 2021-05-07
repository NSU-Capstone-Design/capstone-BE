from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProblemInfoView.as_view()),
    path('userLevel/', views.UserProblemInfo.as_view())
]
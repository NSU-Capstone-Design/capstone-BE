from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProbList.as_view()),
    path('<int:pk>/', views.ProblemDetailView.as_view()),
    path('userLevel/', views.UserProblemInfo.as_view()),
]

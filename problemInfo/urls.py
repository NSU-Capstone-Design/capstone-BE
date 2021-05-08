from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProblemInfoView.as_view()),
    path('<int:pk>/', views.ProblemDetailView.as_view()),
]
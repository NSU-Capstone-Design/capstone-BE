from django.urls import path
from .views import SolvePassView, SolveSuccessView

urlpatterns = [
    path('success/', SolveSuccessView.as_view()),
    path('pass/', SolvePassView.as_view()),
]

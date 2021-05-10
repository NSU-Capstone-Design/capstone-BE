from django.urls import path
from .views import SolvePassView, SolveSuccessView, MySolvedProbsView, MyPassProbsView

urlpatterns = [
    path('success/', SolveSuccessView.as_view()),
    path('pass/', SolvePassView.as_view()),
    path('correct_probs/', MySolvedProbsView.as_view()),
    path('pass_probs/', MyPassProbsView.as_view())
]

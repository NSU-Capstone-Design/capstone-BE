from django.urls import path
from .views import LevelTestProblemListView, LevelTestProblemView

urlpatterns = [
    path('level_test_probs/', LevelTestProblemListView.as_view()),
    path('level_test_prob/', LevelTestProblemView.as_view()),
]

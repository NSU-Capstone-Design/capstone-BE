from django.urls import path
from .views import LevelTestProblemListView, LevelTestProblemView, CreateLevelView

urlpatterns = [
    path('level_test_probs/', LevelTestProblemListView.as_view()),  # 레벨 테스트 문제 리스트
    path('level_test_prob/', LevelTestProblemView.as_view()),  # 레벨테스트 문제 평가
    path('create_level/', CreateLevelView.as_view()),  # 사용자 레벨 설정
]


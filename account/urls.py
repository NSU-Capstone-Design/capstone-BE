from django.urls import path

from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('create/', views.create_user),
    path('test/', views.TestView.as_view(), name='test'),
    path('myInfo/', views.UserInfoView.as_view(), name='myInfo'),
    path('level/', views.UserLevelView.as_view(), name='levelTestCheck'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

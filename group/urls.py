from django.urls import path

from . import views

urlpatterns = [
    path('gmlist/', views.GroupManageListAPIView.as_view(), name='gmlist'),
    path('gmdetail/', views.GroupManageDetailAPIView.as_view(), name='gmdetail'),
    path('grouplist/', views.GroupListAPIView.as_view(), name='grouplist'),
    path('groupdetail/', views.GroupDetailAPIView.as_view(), name='groupdetail'),
]
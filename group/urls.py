from django.urls import path

from . import views

urlpatterns = [
    path('grouplist/<int:pk>/gmlist', views.GroupManageListAPIView.as_view(), name='gmlist'),
    path('gmdetail/', views.GroupManageDetailAPIView.as_view(), name='gmdetail'),
    path('grouplist/', views.GroupListAPIView.as_view(), name='grouplist'),
    path('grouplist/<int:pk>', views.GroupDetailAPIView.as_view(), name='groupdetail'),
]
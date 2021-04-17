from django.urls import path
from . import views


urlpatterns = [
    path('getlist/', views.post_list),
    path('getcomment/', views.post_comment),
]

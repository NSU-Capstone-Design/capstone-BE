from django.urls import path
from . import views


urlpatterns = [
    path('getlist/', views.get_posts),
]
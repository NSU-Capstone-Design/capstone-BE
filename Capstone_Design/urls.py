
from django.contrib import admin
from django.urls import path, include

from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('problem/', include('problemInfo.urls')),
    path('users/', include('account.urls')),
    path('level/', include('levelTest.urls')),
    path('groups/', include('group.urls')),
]

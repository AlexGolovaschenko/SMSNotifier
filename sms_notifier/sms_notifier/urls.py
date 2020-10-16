
from django.contrib import admin
from django.urls import path, include

from home.views import home, settings

urlpatterns = [
    path('', home, name='home'),
    path('settings/', settings, name='settings'),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
]

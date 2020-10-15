
from django.contrib import admin
from django.urls import path

from home.views import home, settings

urlpatterns = [
    path('', home, name='home'),
    path('settings/', settings, name='settings'),
    path('admin/', admin.site.urls),
]

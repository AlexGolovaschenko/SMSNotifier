from django.urls import path

from .views import update_events_list

app_name = 'connector'

urlpatterns = [
	path('update-events/', update_events_list, name = 'update-events' )
]
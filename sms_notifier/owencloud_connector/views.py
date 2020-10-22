from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CloudConnector, CloudEvent
from .connector import OwenCloudConnector


@login_required
def update_events_list(request):
    user = request.user
    cloud_connector = CloudConnector.objects.get(user = user)
    cloud_token = cloud_connector.token
    cloud_domain = cloud_connector.domain
    connector = OwenCloudConnector(debug = False, token = cloud_token, user_domain=cloud_domain)
    # read events list
    events_list = connector.getEventsList()
    
    # update or create events
    for event in events_list:
        if CloudEvent.objects.filter(cloud_connector = cloud_connector, event_id = event['id']).exists():
            obj = CloudEvent.objects.get(cloud_connector = cloud_connector, event_id = event['id'])
            obj.event_id = event['id']
            obj.device_id = 1,
            obj.event_description = event['message']
        else:
            CloudEvent.objects.create(
                cloud_connector = cloud_connector, 
                event_id = event['id'], 
                device_id = 1,
                event_description = event['message'] )

    messages.success(request, f'Список событий OwenCloud успешно обновлен.')
    redirect_path = request.GET.get('next')
    if redirect_path:
        return redirect(redirect_path)
    else:
        return redirect('home')




from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CloudConnector, CloudEvent
from .connector import OwenCloudConnector


@login_required
def update_events_list(request):
    message = ''
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
            obj.device_id = event.get("device_id", 1),
            obj.event_description = event['message']
        else:
            CloudEvent.objects.create(
                cloud_connector = cloud_connector, 
                event_id = event['id'], 
                device_id = event.get("device_id", 1),
                event_description = event['message'] )
            message += '<br/>Событие OwenCloud id="%s" было добавлено' %(event['id'])

    # clear not existing events
    ev_ids = []
    for event in events_list:
        ev_ids.append(str(event['id']))
    all_obj = CloudEvent.objects.filter(cloud_connector = cloud_connector)
    for obj in all_obj:
        if str(obj.event_id) not in ev_ids:
            print('Cloud event %s has been removed' %(obj.event_id))
            message += '<br/>Событие OwenCloud id="%s" было удалено' %(obj.event_id)
            obj.delete()


    messages.success(request, f'<b>Список событий OwenCloud успешно обновлен.</b>' + message)
    redirect_path = request.GET.get('next')
    if redirect_path:
        return redirect(redirect_path)
    else:
        return redirect('home')




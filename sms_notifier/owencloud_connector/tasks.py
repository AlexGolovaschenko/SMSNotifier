from __future__ import absolute_import, unicode_literals
from celery import shared_task

from .connector import OwenCloudConnector
from .models import CloudConnector, CloudEvent


@shared_task(name = "print_msg_with_name")
def print_message(name, *args, **kwargs):
    print("Celery is working!! {} have implemented it correctly.".format(name))


@shared_task(name = "read_owencloud_events_state")
def read_owencloud_events_state():
    print("Update OwenCloud events state")
    connectors = CloudConnector.objects.all()
    for c in connectors:
        connector = OwenCloudConnector(debug = False, token = c.token, user_domain=c.domain)  

        # read events list
        events = connector.getEventsList(just_active = True)

        # update events state
        for ev in events:
            if CloudEvent.objects.filter(cloud_connector = c, event_id = ev['id']).exists():
                ev_obj = CloudEvent.objects.get(cloud_connector = c, event_id = ev['id'])
                if ev["status"] == 1:
                    if not ev_obj.is_active:
                        ev_obj.is_active = True
                        ev_obj.save()
                        print('Event %s activated' %(ev_obj.event_id)) 
                else:
                    if ev_obj.is_active:
                        ev_obj.is_active = False 
                        ev_obj.save()
                        print('Event %s deactivated' %(ev_obj.event_id))                  



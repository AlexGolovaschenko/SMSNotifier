from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.utils import timezone

from .connector import OwenCloudConnector
from .models import CloudConnector, CloudEvent

from notifier.models import Notifier, Event, EventRecord

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
                        create_event_record(c, ev_obj)
                        print('Event %s activated' %(ev_obj.event_id)) 
                else:
                    if ev_obj.is_active:
                        ev_obj.is_active = False 
                        ev_obj.save()
                        set_event_finished(c, ev_obj)
                        print('Event %s deactivated' %(ev_obj.event_id))                  


def create_event_record(user, cloud_event):
    try:
        nf = Notifier.objects.get(user=user)
        event = Event.objects.get(notifier = nf, cloud_event_id=cloud_event)
        new_record = EventRecord.objects.create(event=event)
        new_record.save()
    except:
        print('Cant create evetn record')

def set_event_finished(user, cloud_event):
    try:
        nf = Notifier.objects.get(user=user)
        event = Event.objects.get(notifier = nf, cloud_event_id=cloud_event)
        old_record = EventRecord.objects.get(event=event)
        old_record.fall_dt = timezone.now()
    except:
        print('Cant finde related event record')
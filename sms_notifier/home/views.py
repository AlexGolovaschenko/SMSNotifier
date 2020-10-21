from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from owencloud_connector.models import CloudConnector, CloudEvent 

def home(request):
	return render(request, 'home/home.html')


@login_required
def settings(request):
	user = request.user
	connector = CloudConnector.objects.get(user=user)
	cloud_events = CloudEvent.objects.filter(cloud_connector = connector)

	context = {
		'connector': connector,
		'cloud_events': cloud_events
	}
	return render(request, 'home/settings.html', context)
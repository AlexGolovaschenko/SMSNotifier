from django.db import models
from django.contrib.auth.models import User

CLOUD_DOMAIN_RU = 'RU'
CLOUD_DOMAIN_UA = 'UA'
CLOUD_DOMAINS = {
	(CLOUD_DOMAIN_RU, 'RU'), 
	(CLOUD_DOMAIN_UA, 'UA'),
}

class CloudConnector(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	domain = models.CharField(max_length=2, choices=CLOUD_DOMAINS, default=CLOUD_DOMAIN_RU)
	token = models.CharField(max_length=200, blank=False, null=False)

	def __str__(self):
		return str(self.user.username) + ' коннектор'

	class Meta:
		verbose_name = 'Коннектор OwenCloud'
		verbose_name_plural = 'Коннекторы OwenCloud'


class CloudEvent(models.Model):
	cloud_connector = models.ForeignKey(CloudConnector, on_delete = models.CASCADE, verbose_name='Id коннектора')
	event_id = models.CharField(max_length=200, verbose_name='Id события в OwenCloud')
	device_id = models.CharField(max_length=200, verbose_name='Id устройства')	
	event_description = models.CharField(max_length=200, verbose_name='Описание события') 

	def __str__(self):
		return self.event_description

	class Meta:
		verbose_name = 'Событие OwenCloud'
		verbose_name_plural = 'События OwenCloud'
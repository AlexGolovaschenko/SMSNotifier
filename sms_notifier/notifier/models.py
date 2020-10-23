from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe

from datetime import time

from phonenumber_field.modelfields import PhoneNumberField

from owencloud_connector.models import CloudEvent


SMS_RU = 'SMS.RU'
SMS_SERVICES = {
	(SMS_RU, 'SMS.RU'),
}


class Notifier(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	sms_service = models.CharField(max_length=20, blank=False, null=False, choices=SMS_SERVICES, verbose_name='Сервис рассылки СМС')
	sms_service_token = models.CharField(max_length=200, blank=False, null=False, verbose_name='Токен подключения к СМС сервису')

	def __str__(self):
		return str(self.user.username) + ' уведомления'

	class Meta:
		verbose_name = 'Уведомление'
		verbose_name_plural = 'Уведомления'

	@property
	def sms_service_link(self):
		if self.sms_service == SMS_RU:
			return mark_safe('<a href="https://sms.ru/"> %s <a/>' %(SMS_RU))


class Event(models.Model):
	notifier = models.ForeignKey(Notifier, on_delete = models.CASCADE)
	cloud_event_id = models.ForeignKey(CloudEvent, null=True, on_delete = models.SET_NULL, verbose_name='Id события OwenCloud')
	description = models.CharField(max_length=200, verbose_name='Описание события')
	activate_registration = models.BooleanField(default=True, verbose_name='Включить регистрацию')
	activate_notification = models.BooleanField(default=False, verbose_name='Включить оповещение')

	class Meta:
		verbose_name = 'Событие'
		verbose_name_plural = 'События'


class Recipient(models.Model):
	event = models.ForeignKey(Event, verbose_name='Событие', on_delete = models.CASCADE)
	tel_number = PhoneNumberField(null=False, blank=False)

	en_notification_time_range = models.BooleanField(default=False)
	start_time_range = models.TimeField(auto_now=False, auto_now_add=False, default=time(hour=0, minute=0) )
	end_time_range = models.TimeField(auto_now=False, auto_now_add=False, default=time(hour=0, minute=0) )


class EventRecord(models.Model):
	event = models.ForeignKey(Event, on_delete = models.CASCADE)
	raise_dt = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Начало события')
	fall_dt = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, verbose_name='Завершение события')

	processing = models.BooleanField(default=False, verbose_name='В обработке')
	done = models.BooleanField(default=False, verbose_name='Обработано')
	sended = models.BooleanField(default=False, verbose_name='Отправлено')
	received = models.BooleanField(default=False, verbose_name='Доставлено') 
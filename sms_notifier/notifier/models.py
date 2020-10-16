from django.db import models
from django.contrib.auth.models import User

from datetime import time

from phonenumber_field.modelfields import PhoneNumberField


SMS_SERVICES = {
	('SMS_1', 'SMS service 1 (test)'),
}


class Notifier(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	sms_service = models.CharField(max_length=20, blank=False, null=False, choices=SMS_SERVICES, verbose_name='Сервис рассылки СМС')


class Event(models.Model):
	notifier = models.ForeignKey(Notifier, on_delete = models.CASCADE)
	description = models.CharField(max_length=200, verbose_name='Описание события')
	activate_registration = models.BooleanField(default=False, verbose_name='Включить регистрацию')
	activate_notification = models.BooleanField(default=False, verbose_name='Включить оповещение')


class Recipient(models.Model):
	event = models.ForeignKey(Event, verbose_name='Событие', on_delete = models.CASCADE)
	tel_number = PhoneNumberField(null=False, blank=False)

	en_notification_time_range = models.BooleanField(default=False)
	start_time_range = models.TimeField(auto_now=False, auto_now_add=False, default=time(hour=0, minute=0) )
	end_time_range = models.TimeField(auto_now=False, auto_now_add=False, default=time(hour=0, minute=0) )


class EventRecord(models.Model):
	event = models.ForeignKey(Event, on_delete = models.CASCADE)
	raise_dt = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Начало события')
	fall_dt = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Завершение события')

	processing = models.BooleanField(default=False, verbose_name='В обработке')
	done = models.BooleanField(default=False, verbose_name='Обработано')
	sended = models.BooleanField(default=False, verbose_name='Отправлено')
	received = models.BooleanField(default=False, verbose_name='Доставлено') 
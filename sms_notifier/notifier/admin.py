from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe

from .models import Notifier, Event, Recipient


class RecipientInline(admin.TabularInline):
    model = Recipient
    extra = 0 


class EventInline(admin.TabularInline):
    model = Event
    extra = 0 
    readonly_fields = ('link',)

    def link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,  
                                              instance._meta.model_name ),
                      args=(instance.id,))
        return mark_safe("<a href='%s'>Edit</a>" % url)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # queriset for select cloud_event_id just in events what related to current user
        field = super(EventInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'cloud_event_id':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(cloud_connector__user__exact = request._obj_.user)  
            else:
                field.queryset = field.queryset.none()
        return field


class EventAdmin(admin.ModelAdmin):
    inlines = [RecipientInline]
    class Meta:
        model = Event

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class NotifierAdmin(admin.ModelAdmin):
    inlines = [EventInline]

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(NotifierAdmin, self).get_form(request, obj, **kwargs)

    class Meta:
        model = Notifier

    class Media:
        css = {'all': ('owencloud_connector/css/custom_admin.css', )}




admin.site.register(Notifier, NotifierAdmin)
admin.site.register(Event, EventAdmin)








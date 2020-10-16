from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe
from .models import CloudConnector, CloudEvent

class CloudEventInline(admin.TabularInline):
    model = CloudEvent
    can_delete = False
    readonly_fields = ('event_id', 'device_id', 'event_description', 'link')
    extra = 0

    def link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,  
                                              instance._meta.model_name ),
                      args=(instance.id,))

        return mark_safe("<a href='%s'>Edit</a>" % url)

    def has_add_permission(self, request, obj):
        return False


class CloudConnectorAdmin(admin.ModelAdmin):
    inlines = [CloudEventInline, ]

    class Meta:
        model = CloudConnector

    class Media:
        css = {
            'all': ('owencloud_connector/css/custom_admin.css', )     # Include extra css
        }

class CloudEventAdmin(admin.ModelAdmin):
    model = CloudEvent
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

admin.site.register(CloudConnector, CloudConnectorAdmin)
admin.site.register(CloudEvent, CloudEventAdmin)

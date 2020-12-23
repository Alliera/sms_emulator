from django.contrib import admin

from sms_emulator_core.models import Enterprise, SMSMessage


class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ['name', 'webhook_url']
    ordering = ['name']
    search_fields = ['name']


class SMSMessageAdmin(admin.ModelAdmin):
    list_display = [
        'from_sender', 'to_receiver', 'text', 'enterprise__name',
        'direction', 'create_datetime'
    ]
    ordering = ['creation']
    search_fields = ['to_receiver', 'enterprise__name']

    @staticmethod
    def create_datetime(obj):
        return obj.creation.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def enterprise__name(obj):
        return obj.enterprise.name


admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(SMSMessage, SMSMessageAdmin)

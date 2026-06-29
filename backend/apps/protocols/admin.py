from django.contrib import admin
from .models import Protocol


@admin.register(Protocol)
class ProtocolAdmin(admin.ModelAdmin):
    list_display  = ['protocol_number', 'title', 'principal_investigator',
                     'tenant', 'risk_level', 'status', 'created_at']
    list_filter   = ['status', 'risk_level', 'tenant']
    search_fields = ['title', 'protocol_number']

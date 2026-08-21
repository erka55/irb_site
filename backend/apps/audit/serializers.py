from rest_framework import serializers

from apps.audit.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuditLog

        fields = [
            "id",
            "tenant",
            "actor",
            "event_id",
            "occurred_at",
            "action",
            "entity_type",
            "entity_id",
            "payload",
            "ip_address",
            "user_agent",
            "created_at",
        ]

        read_only_fields = fields

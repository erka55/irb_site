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


class AuditLogFilterSerializer(serializers.Serializer):

    actor_id = serializers.UUIDField(
        required=False,
    )

    action = serializers.CharField(
        required=False,
    )

    entity_type = serializers.CharField(
        required=False,
    )

    entity_id = serializers.UUIDField(
        required=False,
    )

    event_id = serializers.UUIDField(
        required=False,
    )

    occurred_from = serializers.DateTimeField(
        required=False,
    )

    occurred_to = serializers.DateTimeField(
        required=False,
    )

    def validate(self, attrs):
        occurred_from = attrs.get(
            "occurred_from",
        )

        occurred_to = attrs.get(
            "occurred_to",
        )

        if (
            occurred_from is not None
            and occurred_to is not None
            and occurred_from > occurred_to
        ):
            raise serializers.ValidationError(
                "occurred_from must be earlier than or equal to occurred_to."
            )

        return attrs

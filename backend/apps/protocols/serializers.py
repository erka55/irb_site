from rest_framework import serializers

from apps.protocols.models import Protocol


class ProtocolSerializer(serializers.ModelSerializer):

    class Meta:
        model = Protocol

        fields = [
            "id",
            "tenant",
            "title",
            "protocol_number",
            "principal_investigator",
            "risk_level",
            "status",
            "summary",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
        ]

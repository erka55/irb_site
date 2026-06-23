from apps.protocols.enums import (
    ProtocolStatus,
)

from apps.protocols.models import (
    Protocol,
)

from apps.protocols.services.versioning import (
    ProtocolVersionService,
)


class ProtocolCreateService:

    @staticmethod
    def create_protocol(
        *,
        tenant,
        title,
        protocol_number,
        principal_investigator,
        risk_level,
        summary="",
        created_by,
    ):
        protocol = Protocol.objects.create(
            tenant=tenant,
            title=title,
            protocol_number=protocol_number,
            principal_investigator=principal_investigator,
            risk_level=risk_level,
            status=ProtocolStatus.DRAFT,
            summary=summary,
        )

        ProtocolVersionService.create_snapshot(
            protocol=protocol,
            user=created_by,
        )

        return protocol

from apps.protocols.models import ProtocolVersion

class ProtocolVersionService:

    @staticmethod
    def create_snapshot(
        protocol,
        user,
    ):
        """
        Create immutable protocol snapshot.
        """

        latest_version = (
            ProtocolVersion.objects
            .filter(protocol=protocol)
            .order_by("-created_at")
            .first()
        )

        if latest_version:

            current_number = int(
                latest_version.version_number.lstrip("v")
            )

            next_number = current_number + 1

        else:

            next_number = 1

        snapshot = {
            "id": str(protocol.id),
            "title": protocol.title,
            "protocol_number": protocol.protocol_number,
            "status": protocol.status,
            "risk_level": protocol.risk_level,
            "summary": protocol.summary,
            "tenant_id": str(protocol.tenant_id),
            "principal_investigator_id": (
                protocol.principal_investigator_id
            ),
        }

        return ProtocolVersion.objects.create(
            protocol=protocol,
            version_number=f"v{next_number}",
            snapshot=snapshot,
            created_by=user,
        )

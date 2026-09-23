from apps.compliance.models import (
    ConflictOfInterestDeclaration,
    ConflictOfInterestRecusal,
)
from apps.users.models import Membership


class ConflictOfInterestDeclarationService:

    @staticmethod
    def declare(
        *,
        tenant,
        protocol,
        declarant,
        conflict_types,
        description,
        declared_at,
        signature_reference="",
    ) -> ConflictOfInterestDeclaration:

        if protocol.tenant_id != tenant.id:
            raise ValueError(
                "Protocol belongs to a different tenant."
            )

        if not Membership.objects.filter(
            user_id=declarant.id,
            tenant_id=tenant.id,
            is_active=True,
        ).exists():
            raise ValueError(
                "Declarant does not have an active membership in the tenant."
            )

        if not isinstance(conflict_types, list):
            raise ValueError(
                "conflict_types must be a list."
            )

        if not description or not description.strip():
            raise ValueError(
                "Description is required."
            )

        return ConflictOfInterestDeclaration.objects.create(
            tenant=tenant,
            protocol=protocol,
            declarant=declarant,
            conflict_types=conflict_types,
            description=description.strip(),
            declared_at=declared_at,
            signature_reference=signature_reference,
        )

    @staticmethod
    def has_conflict(
        *,
        protocol,
        declarant,
    ) -> bool:
        return ConflictOfInterestDeclaration.objects.filter(
            tenant_id=protocol.tenant_id,
            protocol_id=protocol.id,
            declarant_id=declarant.id,
        ).exists()

    @staticmethod
    def can_participate_in_vote(
        *,
        protocol,
        declarant,
    ) -> bool:
        return not ConflictOfInterestDeclarationService.has_conflict(
            protocol=protocol,
            declarant=declarant,
        )


class ConflictOfInterestRecusalService:

    @staticmethod
    def recuse(
        *,
        tenant,
        declaration,
        agenda,
        participant,
        recused_at,
        note="",
    ) -> ConflictOfInterestRecusal:

        if declaration.tenant_id != tenant.id:
            raise ValueError(
                "Declaration belongs to a different tenant."
            )

        if agenda.meeting.tenant_id != tenant.id:
            raise ValueError(
                "Agenda belongs to a different tenant."
            )

        if participant.meeting_id != agenda.meeting_id:
            raise ValueError(
                "Participant does not belong to the agenda meeting."
            )

        if participant.user_id != declaration.declarant_id:
            raise ValueError(
                "Participant does not match the conflict declaration."
            )

        if agenda.protocol_id != declaration.protocol_id:
            raise ValueError(
                "Agenda protocol does not match the conflict declaration."
            )

        if not ConflictOfInterestDeclarationService.has_conflict(
            protocol=agenda.protocol,
            declarant=participant.user,
        ):
            raise ValueError(
                "Participant does not have a conflict of interest "
                "for this protocol."
            )

        return ConflictOfInterestRecusal.objects.create(
            tenant=tenant,
            declaration=declaration,
            agenda=agenda,
            participant=participant,
            recused_at=recused_at,
            note=note.strip(),
        )

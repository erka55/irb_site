from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from apps.compliance.models import (
    ConflictOfInterestDeclaration,
    ConflictOfInterestRecusal,
    MeetingMinutesRecusal,
)
from apps.compliance.services.coi_service import (
    ConflictOfInterestDeclarationService,
    ConflictOfInterestRecusalService,
    MeetingMinutesRecusalService,
)
from apps.core.models import RoleChoices
from apps.meetings.models import (
    AttendanceStatus,
    Meeting,
    MeetingAgenda,
    MeetingMinutes,
    MeetingParticipant,
    MeetingStatus,
    MeetingType,
    ParticipantRole,
)
from apps.protocols.enums import RiskLevel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import Membership, User


class ConflictOfInterestDeclarationServiceTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="T001",
            name="Test Tenant",
        )

        self.other_tenant = Tenant.objects.create(
            code="T002",
            name="Other Tenant",
        )

        self.declarant = User.objects.create_user(
            email="declarant@example.com",
            password="test-password",
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="test-password",
        )

        Membership.objects.create(
            user=self.declarant,
            tenant=self.tenant,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Test Protocol",
            protocol_number="IRB-TEST-001",
            principal_investigator=self.declarant,
            risk_level=RiskLevel.LOW,
            summary="Test protocol summary",
        )

        self.other_protocol = Protocol.objects.create(
            tenant=self.other_tenant,
            title="Other Protocol",
            protocol_number="IRB-TEST-002",
            principal_investigator=self.other_user,
            risk_level=RiskLevel.LOW,
            summary="Other protocol summary",
        )

        self.meeting = Meeting.objects.create(
            tenant=self.tenant,
            title="Test IRB Meeting",
            meeting_type=MeetingType.REGULAR,
            status=MeetingStatus.SCHEDULED,
            meeting_date=timezone.now(),
            chair=self.declarant,
        )

        self.participant = MeetingParticipant.objects.create(
            meeting=self.meeting,
            user=self.declarant,
            role=ParticipantRole.REVIEWER,
            attendance_status=AttendanceStatus.PRESENT,
        )

        self.agenda = MeetingAgenda.objects.create(
            meeting=self.meeting,
            protocol=self.protocol,
            order=1,
        )

    def test_declare_creates_declaration(self):
        declared_at = timezone.now()

        declaration = ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=declared_at,
            signature_reference="signature/ref/001",
        )

        self.assertIsNotNone(declaration.pk)
        self.assertEqual(declaration.tenant, self.tenant)
        self.assertEqual(declaration.protocol, self.protocol)
        self.assertEqual(declaration.declarant, self.declarant)
        self.assertEqual(declaration.conflict_types, ["financial"])
        self.assertEqual(
            declaration.description,
            "Financial relationship with the research sponsor.",
        )
        self.assertEqual(declaration.declared_at, declared_at)
        self.assertEqual(
            declaration.signature_reference,
            "signature/ref/001",
        )

        self.assertEqual(
            ConflictOfInterestDeclaration.objects.count(),
            1,
        )

    def test_declare_rejects_protocol_from_different_tenant(self):
        with self.assertRaisesMessage(
            ValueError,
            "Protocol belongs to a different tenant.",
        ):
            ConflictOfInterestDeclarationService.declare(
                tenant=self.tenant,
                protocol=self.other_protocol,
                declarant=self.declarant,
                conflict_types=["financial"],
                description="Conflict description.",
                declared_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestDeclaration.objects.exists()
        )

    def test_declare_rejects_declarant_without_active_membership(self):
        inactive_user = User.objects.create_user(
            email="inactive@example.com",
            password="test-password",
        )

        Membership.objects.create(
            user=inactive_user,
            tenant=self.tenant,
            role=RoleChoices.REVIEWER,
            is_active=False,
        )

        with self.assertRaisesMessage(
            ValueError,
            "Declarant does not have an active membership in the tenant.",
        ):
            ConflictOfInterestDeclarationService.declare(
                tenant=self.tenant,
                protocol=self.protocol,
                declarant=inactive_user,
                conflict_types=["financial"],
                description="Conflict description.",
                declared_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestDeclaration.objects.exists()
        )

    def test_declare_rejects_declarant_from_different_tenant(self):
        Membership.objects.create(
            user=self.other_user,
            tenant=self.other_tenant,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        with self.assertRaisesMessage(
            ValueError,
            "Declarant does not have an active membership in the tenant.",
        ):
            ConflictOfInterestDeclarationService.declare(
                tenant=self.tenant,
                protocol=self.protocol,
                declarant=self.other_user,
                conflict_types=["financial"],
                description="Conflict description.",
                declared_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestDeclaration.objects.exists()
        )

    def test_declare_rejects_non_list_conflict_types(self):
        with self.assertRaisesMessage(
            ValueError,
            "conflict_types must be a list.",
        ):
            ConflictOfInterestDeclarationService.declare(
                tenant=self.tenant,
                protocol=self.protocol,
                declarant=self.declarant,
                conflict_types="financial",
                description="Conflict description.",
                declared_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestDeclaration.objects.exists()
        )

    def test_declare_rejects_blank_description(self):
        with self.assertRaisesMessage(
            ValueError,
            "Description is required.",
        ):
            ConflictOfInterestDeclarationService.declare(
                tenant=self.tenant,
                protocol=self.protocol,
                declarant=self.declarant,
                conflict_types=["financial"],
                description="   ",
                declared_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestDeclaration.objects.exists()
        )

    def test_declare_strips_description(self):
        declaration = ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="  Conflict description.  ",
            declared_at=timezone.now(),
        )

        self.assertEqual(
            declaration.description,
            "Conflict description.",
        )

    def test_has_conflict_returns_true_for_declared_protocol_and_user(self):
        ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=timezone.now(),
        )

        self.assertTrue(
            ConflictOfInterestDeclarationService.has_conflict(
                protocol=self.protocol,
                declarant=self.declarant,
            )
        )

    def test_has_conflict_returns_false_without_declaration(self):
        self.assertFalse(
            ConflictOfInterestDeclarationService.has_conflict(
                protocol=self.protocol,
                declarant=self.declarant,
            )
        )

    def test_has_conflict_is_scoped_to_protocol_and_declarant(self):
        ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=timezone.now(),
        )

        self.assertFalse(
            ConflictOfInterestDeclarationService.has_conflict(
                protocol=self.protocol,
                declarant=self.other_user,
            )
        )

        self.assertFalse(
            ConflictOfInterestDeclarationService.has_conflict(
                protocol=self.other_protocol,
                declarant=self.declarant,
            )
        )

    def test_can_participate_in_vote_returns_false_with_conflict(self):
        ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=timezone.now(),
        )

        self.assertFalse(
            ConflictOfInterestDeclarationService.can_participate_in_vote(
                protocol=self.protocol,
                declarant=self.declarant,
            )
        )

    def test_can_participate_in_vote_returns_true_without_conflict(self):
        self.assertTrue(
            ConflictOfInterestDeclarationService.can_participate_in_vote(
                protocol=self.protocol,
                declarant=self.declarant,
            )
        )

    def test_create_recusal(self):
        declaration = ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=timezone.now(),
        )

        recused_at = timezone.now()

        recusal = ConflictOfInterestRecusal.objects.create(
            tenant=self.tenant,
            declaration=declaration,
            agenda=self.agenda,
            participant=self.participant,
            recused_at=recused_at,
            note="Participant left the meeting during discussion.",
        )

        self.assertIsNotNone(recusal.pk)
        self.assertEqual(recusal.tenant, self.tenant)
        self.assertEqual(recusal.declaration, declaration)
        self.assertEqual(recusal.agenda, self.agenda)
        self.assertEqual(recusal.participant, self.participant)
        self.assertEqual(recusal.recused_at, recused_at)
        self.assertEqual(
            recusal.note,
            "Participant left the meeting during discussion.",
        )

        self.assertEqual(
            ConflictOfInterestRecusal.objects.count(),
            1,
        )


class ConflictOfInterestRecusalServiceTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="T101",
            name="Recusal Test Tenant",
        )

        self.other_tenant = Tenant.objects.create(
            code="T102",
            name="Other Recusal Tenant",
        )

        self.declarant = User.objects.create_user(
            email="recusal-declarant@example.com",
            password="test-password",
        )

        self.other_user = User.objects.create_user(
            email="recusal-other@example.com",
            password="test-password",
        )

        Membership.objects.create(
            user=self.declarant,
            tenant=self.tenant,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        Membership.objects.create(
            user=self.other_user,
            tenant=self.tenant,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Recusal Protocol",
            protocol_number="IRB-RECUSAL-001",
            principal_investigator=self.declarant,
            risk_level=RiskLevel.LOW,
            summary="Recusal test protocol",
        )

        self.other_protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Other Recusal Protocol",
            protocol_number="IRB-RECUSAL-002",
            principal_investigator=self.other_user,
            risk_level=RiskLevel.LOW,
            summary="Other recusal test protocol",
        )

        self.other_tenant_protocol = Protocol.objects.create(
            tenant=self.other_tenant,
            title="Other Tenant Protocol",
            protocol_number="IRB-RECUSAL-003",
            principal_investigator=self.other_user,
            risk_level=RiskLevel.LOW,
            summary="Other tenant protocol",
        )

        self.meeting = Meeting.objects.create(
            tenant=self.tenant,
            title="Recusal Test Meeting",
            meeting_type=MeetingType.REGULAR,
            status=MeetingStatus.IN_PROGRESS,
            meeting_date=timezone.now(),
            chair=self.declarant,
        )

        self.other_meeting = Meeting.objects.create(
            tenant=self.tenant,
            title="Other Recusal Meeting",
            meeting_type=MeetingType.REGULAR,
            status=MeetingStatus.IN_PROGRESS,
            meeting_date=timezone.now(),
            chair=self.declarant,
        )

        self.other_tenant_meeting = Meeting.objects.create(
            tenant=self.other_tenant,
            title="Other Tenant Meeting",
            meeting_type=MeetingType.REGULAR,
            status=MeetingStatus.IN_PROGRESS,
            meeting_date=timezone.now(),
            chair=self.other_user,
        )

        self.participant = MeetingParticipant.objects.create(
            meeting=self.meeting,
            user=self.declarant,
            role=ParticipantRole.REVIEWER,
            attendance_status=AttendanceStatus.PRESENT,
        )

        self.other_participant = MeetingParticipant.objects.create(
            meeting=self.other_meeting,
            user=self.declarant,
            role=ParticipantRole.REVIEWER,
            attendance_status=AttendanceStatus.PRESENT,
        )

        self.other_user_participant = MeetingParticipant.objects.create(
            meeting=self.meeting,
            user=self.other_user,
            role=ParticipantRole.REVIEWER,
            attendance_status=AttendanceStatus.PRESENT,
        )

        self.other_tenant_participant = MeetingParticipant.objects.create(
            meeting=self.other_tenant_meeting,
            user=self.other_user,
            role=ParticipantRole.REVIEWER,
            attendance_status=AttendanceStatus.PRESENT,
        )

        self.agenda = MeetingAgenda.objects.create(
            meeting=self.meeting,
            protocol=self.protocol,
            order=1,
        )

        self.other_meeting_agenda = MeetingAgenda.objects.create(
            meeting=self.other_meeting,
            protocol=self.protocol,
            order=1,
        )

        self.other_tenant_agenda = MeetingAgenda.objects.create(
            meeting=self.other_tenant_meeting,
            protocol=self.other_tenant_protocol,
            order=1,
        )

        self.other_protocol_agenda = MeetingAgenda.objects.create(
            meeting=self.meeting,
            protocol=self.other_protocol,
            order=2,
        )

        self.declaration = ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=timezone.now(),
        )

    def test_recuse_creates_recusal(self):
        recused_at = timezone.now()

        recusal = ConflictOfInterestRecusalService.recuse(
            tenant=self.tenant,
            declaration=self.declaration,
            agenda=self.agenda,
            participant=self.participant,
            recused_at=recused_at,
            note="Participant left during protocol discussion.",
        )

        self.assertIsNotNone(recusal.pk)
        self.assertEqual(recusal.tenant, self.tenant)
        self.assertEqual(recusal.declaration, self.declaration)
        self.assertEqual(recusal.agenda, self.agenda)
        self.assertEqual(recusal.participant, self.participant)
        self.assertEqual(recusal.recused_at, recused_at)
        self.assertEqual(
            recusal.note,
            "Participant left during protocol discussion.",
        )

        self.assertEqual(
            ConflictOfInterestRecusal.objects.count(),
            1,
        )

    def test_recuse_rejects_declaration_from_different_tenant(self):
        other_declaration = ConflictOfInterestDeclaration.objects.create(
            tenant=self.other_tenant,
            protocol=self.other_tenant_protocol,
            declarant=self.other_user,
            conflict_types=["financial"],
            description="Conflict in another tenant.",
            declared_at=timezone.now(),
        )

        with self.assertRaisesMessage(
            ValueError,
            "Declaration belongs to a different tenant.",
        ):
            ConflictOfInterestRecusalService.recuse(
                tenant=self.tenant,
                declaration=other_declaration,
                agenda=self.agenda,
                participant=self.participant,
                recused_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestRecusal.objects.exists()
        )

    def test_recuse_rejects_agenda_from_different_tenant(self):
        with self.assertRaisesMessage(
            ValueError,
            "Agenda belongs to a different tenant.",
        ):
            ConflictOfInterestRecusalService.recuse(
                tenant=self.tenant,
                declaration=self.declaration,
                agenda=self.other_tenant_agenda,
                participant=self.participant,
                recused_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestRecusal.objects.exists()
        )

    def test_recuse_rejects_participant_from_different_meeting(self):
        with self.assertRaisesMessage(
            ValueError,
            "Participant does not belong to the agenda meeting.",
        ):
            ConflictOfInterestRecusalService.recuse(
                tenant=self.tenant,
                declaration=self.declaration,
                agenda=self.agenda,
                participant=self.other_participant,
                recused_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestRecusal.objects.exists()
        )

    def test_recuse_rejects_participant_who_is_not_declarant(self):
        with self.assertRaisesMessage(
            ValueError,
            "Participant does not match the conflict declaration.",
        ):
            ConflictOfInterestRecusalService.recuse(
                tenant=self.tenant,
                declaration=self.declaration,
                agenda=self.agenda,
                participant=self.other_user_participant,
                recused_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestRecusal.objects.exists()
        )

    def test_recuse_rejects_agenda_with_different_protocol(self):
        with self.assertRaisesMessage(
            ValueError,
            "Agenda protocol does not match the conflict declaration.",
        ):
            ConflictOfInterestRecusalService.recuse(
                tenant=self.tenant,
                declaration=self.declaration,
                agenda=self.other_protocol_agenda,
                participant=self.participant,
                recused_at=timezone.now(),
            )

        self.assertFalse(
            ConflictOfInterestRecusal.objects.exists()
        )

    def test_recuse_rejects_duplicate_recusal(self):
        ConflictOfInterestRecusalService.recuse(
            tenant=self.tenant,
            declaration=self.declaration,
            agenda=self.agenda,
            participant=self.participant,
            recused_at=timezone.now(),
            note="Initial recusal",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ConflictOfInterestRecusalService.recuse(
                    tenant=self.tenant,
                    declaration=self.declaration,
                    agenda=self.agenda,
                    participant=self.participant,
                    recused_at=timezone.now(),
                    note="Duplicate recusal",
                )

        self.assertEqual(
            ConflictOfInterestRecusal.objects.count(),
            1,
        )

class MeetingMinutesRecusalModelTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="T201",
            name="Minutes Test Tenant",
        )

        self.declarant = User.objects.create_user(
            email="minutes-declarant@example.com",
            password="test-password",
        )

        Membership.objects.create(
            user=self.declarant,
            tenant=self.tenant,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Minutes Protocol",
            protocol_number="IRB-MINUTES-001",
            principal_investigator=self.declarant,
            risk_level=RiskLevel.LOW,
            summary="Minutes recusal test protocol",
        )

        self.meeting = Meeting.objects.create(
            tenant=self.tenant,
            title="Minutes Test Meeting",
            meeting_type=MeetingType.REGULAR,
            status=MeetingStatus.IN_PROGRESS,
            meeting_date=timezone.now(),
            chair=self.declarant,
        )

        self.participant = MeetingParticipant.objects.create(
            meeting=self.meeting,
            user=self.declarant,
            role=ParticipantRole.REVIEWER,
            attendance_status=AttendanceStatus.PRESENT,
        )

        self.agenda = MeetingAgenda.objects.create(
            meeting=self.meeting,
            protocol=self.protocol,
            order=1,
        )

        self.declaration = ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=timezone.now(),
        )

        self.recusal = ConflictOfInterestRecusalService.recuse(
            tenant=self.tenant,
            declaration=self.declaration,
            agenda=self.agenda,
            participant=self.participant,
            recused_at=timezone.now(),
            note="Participant left during protocol discussion.",
        )

        self.minutes = MeetingMinutes.objects.create(
            tenant=self.tenant,
            meeting=self.meeting,
            content=(
                "The conflicted participant left the meeting "
                "during discussion of the protocol."
            ),
            recorded_at=timezone.now(),
        )

    def test_create_meeting_minutes_recusal(self):
        recorded_at = timezone.now()

        minutes_recusal = MeetingMinutesRecusal.objects.create(
            tenant=self.tenant,
            minutes=self.minutes,
            recusal=self.recusal,
            recorded_at=recorded_at,
        )

        self.assertIsNotNone(minutes_recusal.pk)
        self.assertEqual(minutes_recusal.tenant, self.tenant)
        self.assertEqual(minutes_recusal.minutes, self.minutes)
        self.assertEqual(minutes_recusal.recusal, self.recusal)
        self.assertEqual(
            minutes_recusal.recorded_at,
            recorded_at,
        )

        self.assertEqual(
            self.minutes.recusals.count(),
            1,
        )

        self.assertEqual(
            self.recusal.minutes_record,
            minutes_recusal,
        )

class MeetingMinutesRecusalServiceTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="T202",
            name="Minutes Service Tenant",
        )
        self.declarant = User.objects.create_user(
            email="minutes-service@example.com",
            password="test-password",
        )
        Membership.objects.create(
            user=self.declarant,
            tenant=self.tenant,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )
        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Minutes Service Protocol",
            protocol_number="IRB-MINUTES-SVC-001",
            principal_investigator=self.declarant,
            risk_level=RiskLevel.LOW,
            summary="Minutes service test protocol",
        )
        self.meeting = Meeting.objects.create(
            tenant=self.tenant,
            title="Minutes Service Meeting",
            meeting_type=MeetingType.REGULAR,
            status=MeetingStatus.IN_PROGRESS,
            meeting_date=timezone.now(),
            chair=self.declarant,
        )
        self.participant = MeetingParticipant.objects.create(
            meeting=self.meeting,
            user=self.declarant,
            role=ParticipantRole.REVIEWER,
            attendance_status=AttendanceStatus.PRESENT,
        )
        self.agenda = MeetingAgenda.objects.create(
            meeting=self.meeting,
            protocol=self.protocol,
            order=1,
        )
        self.declaration = ConflictOfInterestDeclarationService.declare(
            tenant=self.tenant,
            protocol=self.protocol,
            declarant=self.declarant,
            conflict_types=["financial"],
            description="Financial relationship with the research sponsor.",
            declared_at=timezone.now(),
        )
        self.recusal = ConflictOfInterestRecusalService.recuse(
            tenant=self.tenant,
            declaration=self.declaration,
            agenda=self.agenda,
            participant=self.participant,
            recused_at=timezone.now(),
            note="Participant left during protocol discussion.",
        )
        self.minutes = MeetingMinutes.objects.create(
            tenant=self.tenant,
            meeting=self.meeting,
            content=(
                "The conflicted participant left the meeting "
                "during discussion of the protocol."
            ),
            recorded_at=timezone.now(),
        )

    def test_record_creates_minutes_recusal(self):
        recorded_at = timezone.now()

        minutes_recusal = MeetingMinutesRecusalService.record(
            tenant=self.tenant,
            minutes=self.minutes,
            recusal=self.recusal,
            recorded_at=recorded_at,
        )

        self.assertIsNotNone(minutes_recusal.pk)
        self.assertEqual(minutes_recusal.tenant, self.tenant)
        self.assertEqual(minutes_recusal.minutes, self.minutes)
        self.assertEqual(minutes_recusal.recusal, self.recusal)
        self.assertEqual(minutes_recusal.recorded_at, recorded_at)

    def test_record_rejects_tenant_mismatch(self):
        other_tenant = Tenant.objects.create(
            code="T203",
            name="Other Minutes Tenant",
        )

        with self.assertRaises(ValueError):
            MeetingMinutesRecusalService.record(
                tenant=other_tenant,
                minutes=self.minutes,
                recusal=self.recusal,
                recorded_at=timezone.now(),
            )

    def test_record_rejects_minutes_from_different_meeting(self):
        other_meeting = Meeting.objects.create(
            tenant=self.tenant,
            title="Other Meeting",
            meeting_type=MeetingType.REGULAR,
            status=MeetingStatus.IN_PROGRESS,
            meeting_date=timezone.now(),
            chair=self.declarant,
        )
        other_minutes = MeetingMinutes.objects.create(
            tenant=self.tenant,
            meeting=other_meeting,
            content="Other meeting minutes.",
            recorded_at=timezone.now(),
        )

        with self.assertRaises(ValueError):
            MeetingMinutesRecusalService.record(
                tenant=self.tenant,
                minutes=other_minutes,
                recusal=self.recusal,
                recorded_at=timezone.now(),
            )

    def test_record_rejects_duplicate_recording(self):
        recorded_at = timezone.now()

        MeetingMinutesRecusal.objects.create(
            tenant=self.tenant,
            minutes=self.minutes,
            recusal=self.recusal,
            recorded_at=recorded_at,
        )

        with self.assertRaises(ValueError):
            MeetingMinutesRecusalService.record(
                tenant=self.tenant,
                minutes=self.minutes,
                recusal=self.recusal,
                recorded_at=timezone.now(),
            )

    def test_record_preserves_recorded_at(self):
        recorded_at = timezone.now()

        minutes_recusal = MeetingMinutesRecusalService.record(
            tenant=self.tenant,
            minutes=self.minutes,
            recusal=self.recusal,
            recorded_at=recorded_at,
        )

        self.assertEqual(minutes_recusal.recorded_at, recorded_at)

    def test_record_preserves_reverse_relations(self):
        minutes_recusal = MeetingMinutesRecusalService.record(
            tenant=self.tenant,
            minutes=self.minutes,
            recusal=self.recusal,
            recorded_at=timezone.now(),
        )

        self.assertEqual(self.minutes.recusals.get(), minutes_recusal)
        self.assertEqual(self.recusal.minutes_record, minutes_recusal)

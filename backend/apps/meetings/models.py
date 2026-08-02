from django.db import models
from apps.core.models import BaseModel

class MeetingStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Scheduled"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"

class MeetingType(models.TextChoices):
    REGULAR = "regular", "Regular"
    EXPEDITED = "expedited", "Expedited"
    EMERGENCY = "emergency", "Emergency"

class ParticipantRole(models.TextChoices):
    CHAIR = "chair", "Chair"
    REVIEWER = "reviewer", "Reviewer"
    SECRETARY = "secretary", "Secretary"
    GUEST = "guest", "Guest"

class AttendanceStatus(models.TextChoices):
    INVITED = "invited", "Invited"
    PRESENT = "present", "Present"
    ABSENT = "absent", "Absent"
    EXCUSED = "excused", "Excused"

class Meeting(BaseModel):
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="meetings",
    )

    title = models.CharField(max_length=255)

    meeting_type = models.CharField(
        max_length=20,
        choices=MeetingType.choices,
        default=MeetingType.REGULAR,
    )

    status = models.CharField(
        max_length=20,
        choices=MeetingStatus.choices,
        default=MeetingStatus.SCHEDULED,
    )

    meeting_date = models.DateTimeField()

    location = models.CharField(
        max_length=255,
        blank=True,
    )

    chair = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="chaired_meetings",
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["-meeting_date"]
        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"

    def __str__(self):
        return f"{self.title} ({self.meeting_date.date()})"

class MeetingParticipant(BaseModel):
    meeting = models.ForeignKey(
        "meetings.Meeting",
        on_delete=models.CASCADE,
        related_name="participants",
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="meeting_participations",
    )

    role = models.CharField(
        max_length=20,
        choices=ParticipantRole.choices,
        default=ParticipantRole.REVIEWER,
    )

    attendance_status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.INVITED,
    )

    class Meta:
        ordering = ["meeting", "user"]
        constraints = [
            models.UniqueConstraint(
                fields=["meeting", "user"],
                name="unique_meeting_participant",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.meeting}"

class MeetingAgenda(BaseModel):
    meeting = models.ForeignKey(
        "meetings.Meeting",
        on_delete=models.CASCADE,
        related_name="agenda_items",
    )

    protocol = models.ForeignKey(
        "protocols.Protocol",
        on_delete=models.CASCADE,
        related_name="meeting_agendas",
    )

    order = models.PositiveIntegerField()

    presenter = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="presented_agenda_items",
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["meeting", "order"]
        constraints = [
            models.UniqueConstraint(
                fields=["meeting", "order"],
                name="unique_meeting_agenda_order",
            ),
            models.UniqueConstraint(
                fields=["meeting", "protocol"],
                name="unique_meeting_protocol",
            ),
        ]

    def __str__(self):
        return f"{self.meeting} - Item {self.order}"

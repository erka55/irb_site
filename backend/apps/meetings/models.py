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

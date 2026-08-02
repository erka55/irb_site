from apps.meetings.models import (
    AttendanceStatus,
    Meeting,
    MeetingParticipant,
    ParticipantRole,
    MeetingStatus,
)


class ParticipantService:

    @staticmethod
    def add_participant(
        meeting: Meeting,
        user,
        role=ParticipantRole.REVIEWER,
    ):
        participant, created = MeetingParticipant.objects.get_or_create(
            meeting=meeting,
            user=user,
            defaults={
                "role": role,
            },
        )

        if not created:
            raise ValueError("Participant already exists.")

        return participant

    @staticmethod
    def remove_participant(participant: MeetingParticipant):
        if participant.meeting.status != MeetingStatus.SCHEDULED:
            raise ValueError(
                "Participants can only be removed before the meeting starts."
            )

        participant.delete()

    @staticmethod
    def mark_attendance(
        participant: MeetingParticipant,
        attendance_status,
    ):
        participant.attendance_status = attendance_status
        participant.save(update_fields=["attendance_status"])

        return participant

from apps.meetings.models import (
    AttendanceStatus,
    Meeting,
    MeetingParticipant,
)


class QuorumService:

    @staticmethod
    def present_participants(meeting: Meeting):
        return MeetingParticipant.objects.filter(
            meeting=meeting,
            attendance_status=AttendanceStatus.PRESENT,
        )

    @staticmethod
    def total_participants(meeting: Meeting):
        return MeetingParticipant.objects.filter(
            meeting=meeting,
        ).count()

    @staticmethod
    def present_count(meeting: Meeting):
        return QuorumService.present_participants(
            meeting,
        ).count()

    @staticmethod
    def has_quorum(
        meeting: Meeting,
        minimum_ratio: float = 0.5,
    ):
        total = QuorumService.total_participants(
            meeting,
        )

        if total == 0:
            return False

        present = QuorumService.present_count(
            meeting,
        )

        return (present / total) >= minimum_ratio

    @staticmethod
    def attendance_percentage(meeting: Meeting):
        total = QuorumService.total_participants(
            meeting,
        )

        if total == 0:
            return 0

        present = QuorumService.present_count(
            meeting,
        )

        return round(
            (present / total) * 100,
            2,
        )

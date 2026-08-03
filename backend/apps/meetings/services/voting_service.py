from django.db import transaction

from apps.meetings.models import (
    MeetingAgenda,
    MeetingParticipant,
    MeetingVote,
    VoteChoice,
)


class VotingService:

    @staticmethod
    @transaction.atomic
    def cast_vote(
        agenda: MeetingAgenda,
        participant: MeetingParticipant,
        vote: VoteChoice,
        comment: str = "",
    ):
        meeting_vote, created = MeetingVote.objects.get_or_create(
            agenda=agenda,
            participant=participant,
            defaults={
                "vote": vote,
                "comment": comment,
            },
        )

        if not created:
            raise ValueError("Participant has already voted.")

        return meeting_vote

    @staticmethod
    @transaction.atomic
    def update_vote(
        meeting_vote: MeetingVote,
        vote: VoteChoice,
        comment: str = "",
    ):
        meeting_vote.vote = vote
        meeting_vote.comment = comment
        meeting_vote.save(
            update_fields=[
                "vote",
                "comment",
            ]
        )

        return meeting_vote

    @staticmethod
    def get_votes_for_agenda(
        agenda: MeetingAgenda,
    ):
        return MeetingVote.objects.filter(
            agenda=agenda,
        )

    @staticmethod
    def count_votes(
        agenda: MeetingAgenda,
    ):
        votes = VotingService.get_votes_for_agenda(
            agenda,
        )

        results = {
            choice: 0
            for choice, _ in VoteChoice.choices
        }

        for vote in votes:
            results[vote.vote] += 1

        return results

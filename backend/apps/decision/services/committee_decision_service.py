from collections import Counter

from apps.decision.models import Decision
from apps.meetings.models import (
    MeetingStatus,
    VoteChoice,
)
from apps.decision.services.decision_service import DecisionService
from apps.decision.services.publication_service import (
    DecisionPublicationService,
)


class CommitteeDecisionService:
    """
    Creates official IRB decisions from completed committee meetings.
    """

    @classmethod
    def create_from_agenda(cls, agenda):
        """
        Create an official Decision from a completed
        meeting agenda item.
        """

        cls.validate_agenda(agenda)

        decision_type = cls.determine_decision_type(agenda)

        decision = DecisionService.create_draft(
            protocol_id=agenda.protocol.id,
            decision_type=decision_type,
        )

        # Generate the official decision letter.
        DecisionPublicationService.generate_letter(decision)

        return decision

    @classmethod
    def validate_agenda(cls, agenda):
        """
        Validate whether the agenda item is eligible
        for decision creation.
        """

        if agenda is None:
            raise ValueError("Agenda item is required.")

        if agenda.meeting.status != MeetingStatus.COMPLETED:
            raise ValueError(
                "Meeting must be completed before creating a decision."
            )

        if not agenda.votes.exists():
            raise ValueError(
                "No votes have been recorded for this agenda item."
            )

        if Decision.objects.filter(protocol=agenda.protocol).exists():
            raise ValueError(
                f"Decision already exists for protocol {agenda.protocol.pk}."
            )

        return True

    @classmethod
    def determine_decision_type(cls, agenda):
        """
        Determine the final DecisionType from
        committee voting results.
        """

        votes = list(agenda.votes.all())

        if not votes:
            raise ValueError(
                "No votes have been recorded."
            )

        counter = Counter(v.vote for v in votes)

        most_common = counter.most_common()

        highest_count = most_common[0][1]

        winners = [
            vote
            for vote, count in most_common
            if count == highest_count
        ]

        if len(winners) > 1:
            raise ValueError(
                "Committee vote resulted in a tie."
            )

        winning_vote = winners[0]

        mapping = {
            VoteChoice.APPROVE:
                Decision.DecisionType.APPROVED,

            VoteChoice.APPROVE_WITH_CHANGES:
                Decision.DecisionType.CONDITIONAL_APPROVAL,

            VoteChoice.REVISIONS_REQUIRED:
                Decision.DecisionType.REVISION_REQUIRED,

            VoteChoice.REJECT:
                Decision.DecisionType.REJECTED,
        }

        if winning_vote == VoteChoice.ABSTAIN:
            raise ValueError(
                "Cannot determine a decision from abstentions only."
            )

        return mapping[winning_vote]

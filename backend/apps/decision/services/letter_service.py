from apps.decision.models import DecisionLetter


class LetterService:

    @staticmethod
    def generate_letter(
        decision,
        generated_by,
    ):
        return DecisionLetter.objects.create(
            decision=decision,
            generated_by=generated_by,
        )

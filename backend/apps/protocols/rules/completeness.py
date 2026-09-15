from dataclasses import dataclass

from apps.protocols.enums import SubmissionDocumentType


@dataclass(frozen=True)
class SubmissionCompletenessContext:
    uses_questionnaire_or_interview: bool = False
    is_ai_or_cyber_research: bool = False


@dataclass(frozen=True)
class SubmissionCompletenessResult:
    is_complete: bool
    missing_document_types: frozenset[SubmissionDocumentType]


class SubmissionCompletenessRules:
    REQUIRED_DOCUMENT_TYPES = frozenset(
        {
            SubmissionDocumentType.RESEARCH_INTRODUCTION,
            SubmissionDocumentType.METHODOLOGY,
            SubmissionDocumentType.RISK_ASSESSMENT,
            SubmissionDocumentType.INFORMED_CONSENT,
            SubmissionDocumentType.DATA_PROTECTION_PLAN,
            SubmissionDocumentType.PI_SIGNATURE,
        }
    )

    CONDITIONAL_DOCUMENT_TYPES = frozenset(
        {
            SubmissionDocumentType.QUESTIONNAIRE,
            SubmissionDocumentType.AI_CYBER_ASSESSMENT,
        }
    )


class SubmissionCompletenessEvaluator:

    @classmethod
    def evaluate(
        cls,
        uploaded_document_types,
        context: SubmissionCompletenessContext,
    ) -> SubmissionCompletenessResult:
        required_document_types = set(
            SubmissionCompletenessRules.REQUIRED_DOCUMENT_TYPES
        )

        if context.uses_questionnaire_or_interview:
            required_document_types.add(
                SubmissionDocumentType.QUESTIONNAIRE
            )

        if context.is_ai_or_cyber_research:
            required_document_types.add(
                SubmissionDocumentType.AI_CYBER_ASSESSMENT
            )

        missing_document_types = frozenset(
            required_document_types - set(uploaded_document_types)
        )

        return SubmissionCompletenessResult(
            is_complete=not missing_document_types,
            missing_document_types=missing_document_types,
        )

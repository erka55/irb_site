from django.test import SimpleTestCase

from apps.protocols.enums import SubmissionDocumentType
from apps.protocols.rules.completeness import (
    SubmissionCompletenessContext,
    SubmissionCompletenessEvaluator,
    SubmissionCompletenessResult,
    SubmissionCompletenessRules,
)

class SubmissionCompletenessRulesTests(SimpleTestCase):

    def test_required_document_types(self):
        expected = {
            SubmissionDocumentType.RESEARCH_INTRODUCTION,
            SubmissionDocumentType.METHODOLOGY,
            SubmissionDocumentType.RISK_ASSESSMENT,
            SubmissionDocumentType.INFORMED_CONSENT,
            SubmissionDocumentType.DATA_PROTECTION_PLAN,
            SubmissionDocumentType.PI_SIGNATURE,
        }

        self.assertEqual(
            SubmissionCompletenessRules.REQUIRED_DOCUMENT_TYPES,
            frozenset(expected),
        )

    def test_conditional_document_types(self):
        expected = {
            SubmissionDocumentType.QUESTIONNAIRE,
            SubmissionDocumentType.AI_CYBER_ASSESSMENT,
        }

        self.assertEqual(
            SubmissionCompletenessRules.CONDITIONAL_DOCUMENT_TYPES,
            frozenset(expected),
        )


class SubmissionCompletenessContextTests(SimpleTestCase):

    def test_default_context(self):
        context = SubmissionCompletenessContext()

        self.assertFalse(context.uses_questionnaire_or_interview)
        self.assertFalse(context.is_ai_or_cyber_research)

    def test_context_accepts_conditional_flags(self):
        context = SubmissionCompletenessContext(
            uses_questionnaire_or_interview=True,
            is_ai_or_cyber_research=True,
        )

        self.assertTrue(context.uses_questionnaire_or_interview)
        self.assertTrue(context.is_ai_or_cyber_research)

class SubmissionCompletenessResultTests(SimpleTestCase):

    def test_complete_result(self):
        result = SubmissionCompletenessResult(
            is_complete=True,
            missing_document_types=frozenset(),
        )

        self.assertTrue(result.is_complete)
        self.assertEqual(result.missing_document_types, frozenset())

    def test_incomplete_result(self):
        result = SubmissionCompletenessResult(
            is_complete=False,
            missing_document_types=frozenset(
                {
                    SubmissionDocumentType.METHODOLOGY,
                    SubmissionDocumentType.RISK_ASSESSMENT,
                }
            ),
        )

        self.assertFalse(result.is_complete)
        self.assertEqual(
            result.missing_document_types,
            frozenset(
                {
                    SubmissionDocumentType.METHODOLOGY,
                    SubmissionDocumentType.RISK_ASSESSMENT,
                }
            ),
        )

class SubmissionCompletenessEvaluatorTests(SimpleTestCase):

    def test_all_required_documents_are_complete(self):
        uploaded_documents = (
            SubmissionCompletenessRules.REQUIRED_DOCUMENT_TYPES
        )
        context = SubmissionCompletenessContext()

        result = SubmissionCompletenessEvaluator.evaluate(
            uploaded_document_types=uploaded_documents,
            context=context,
        )

        self.assertTrue(result.is_complete)
        self.assertEqual(
            result.missing_document_types,
            frozenset(),
        )

    def test_missing_required_document_is_incomplete(self):
        uploaded_documents = (
            SubmissionCompletenessRules.REQUIRED_DOCUMENT_TYPES
            - {SubmissionDocumentType.PI_SIGNATURE}
        )
        context = SubmissionCompletenessContext()

        result = SubmissionCompletenessEvaluator.evaluate(
            uploaded_document_types=uploaded_documents,
            context=context,
        )

        self.assertFalse(result.is_complete)
        self.assertEqual(
            result.missing_document_types,
            frozenset({SubmissionDocumentType.PI_SIGNATURE}),
        )

    def test_questionnaire_becomes_required_when_context_requires_it(self):
        uploaded_documents = (
            SubmissionCompletenessRules.REQUIRED_DOCUMENT_TYPES
        )
        context = SubmissionCompletenessContext(
            uses_questionnaire_or_interview=True,
        )

        result = SubmissionCompletenessEvaluator.evaluate(
            uploaded_document_types=uploaded_documents,
            context=context,
        )

        self.assertFalse(result.is_complete)
        self.assertEqual(
            result.missing_document_types,
            frozenset({SubmissionDocumentType.QUESTIONNAIRE}),
        )

    def test_questionnaire_is_satisfied_when_uploaded(self):
        uploaded_documents = (
            SubmissionCompletenessRules.REQUIRED_DOCUMENT_TYPES
            | {SubmissionDocumentType.QUESTIONNAIRE}
        )
        context = SubmissionCompletenessContext(
            uses_questionnaire_or_interview=True,
        )

        result = SubmissionCompletenessEvaluator.evaluate(
            uploaded_document_types=uploaded_documents,
            context=context,
        )

        self.assertTrue(result.is_complete)
        self.assertEqual(
            result.missing_document_types,
            frozenset(),
        )

    def test_ai_cyber_assessment_becomes_required_for_ai_cyber_research(self):
        uploaded_documents = (
            SubmissionCompletenessRules.REQUIRED_DOCUMENT_TYPES
        )
        context = SubmissionCompletenessContext(
            is_ai_or_cyber_research=True,
        )

        result = SubmissionCompletenessEvaluator.evaluate(
            uploaded_document_types=uploaded_documents,
            context=context,
        )

        self.assertFalse(result.is_complete)
        self.assertEqual(
            result.missing_document_types,
            frozenset({SubmissionDocumentType.AI_CYBER_ASSESSMENT}),
        )

    def test_ai_cyber_assessment_is_satisfied_when_uploaded(self):
        uploaded_documents = (
            SubmissionCompletenessRules.REQUIRED_DOCUMENT_TYPES
            | {SubmissionDocumentType.AI_CYBER_ASSESSMENT}
        )
        context = SubmissionCompletenessContext(
            is_ai_or_cyber_research=True,
        )

        result = SubmissionCompletenessEvaluator.evaluate(
            uploaded_document_types=uploaded_documents,
            context=context,
        )

        self.assertTrue(result.is_complete)
        self.assertEqual(
            result.missing_document_types,
            frozenset(),
        )

    def test_both_conditional_documents_can_be_required(self):
        uploaded_documents = (
            SubmissionCompletenessRules.REQUIRED_DOCUMENT_TYPES
        )
        context = SubmissionCompletenessContext(
            uses_questionnaire_or_interview=True,
            is_ai_or_cyber_research=True,
        )

        result = SubmissionCompletenessEvaluator.evaluate(
            uploaded_document_types=uploaded_documents,
            context=context,
        )

        self.assertFalse(result.is_complete)
        self.assertEqual(
            result.missing_document_types,
            frozenset(
                {
                    SubmissionDocumentType.QUESTIONNAIRE,
                    SubmissionDocumentType.AI_CYBER_ASSESSMENT,
                }
            ),
        )

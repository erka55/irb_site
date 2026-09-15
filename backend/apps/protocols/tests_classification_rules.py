from django.test import SimpleTestCase

from apps.protocols.enums import ReviewClassification, RiskLevel
from apps.protocols.rules.classification import (
    ClassificationContext,
    ClassificationEvaluator,
)


class ClassificationContextTests(SimpleTestCase):

    def test_context_accepts_all_classification_inputs(self):
        context = ClassificationContext(
            risk_level=RiskLevel.MEDIUM,
            uses_personal_data=True,
            data_is_anonymized=True,
            involves_vulnerable_group=False,
            is_ai_research=False,
            is_cyber_research=False,
        )

        self.assertEqual(
            context.risk_level,
            RiskLevel.MEDIUM,
        )
        self.assertTrue(context.uses_personal_data)
        self.assertTrue(context.data_is_anonymized)
        self.assertFalse(context.involves_vulnerable_group)
        self.assertFalse(context.is_ai_research)
        self.assertFalse(context.is_cyber_research)


class ClassificationEvaluatorTests(SimpleTestCase):

    def test_ai_research_requires_full_review(self):
        context = ClassificationContext(
            risk_level=RiskLevel.LOW,
            uses_personal_data=False,
            data_is_anonymized=False,
            involves_vulnerable_group=False,
            is_ai_research=True,
            is_cyber_research=False,
        )

        result = ClassificationEvaluator.evaluate(context)

        self.assertEqual(
            result,
            ReviewClassification.FULL,
        )

    def test_cyber_research_requires_full_review(self):
        context = ClassificationContext(
            risk_level=RiskLevel.LOW,
            uses_personal_data=False,
            data_is_anonymized=False,
            involves_vulnerable_group=False,
            is_ai_research=False,
            is_cyber_research=True,
        )

        result = ClassificationEvaluator.evaluate(context)

        self.assertEqual(
            result,
            ReviewClassification.FULL,
        )

    def test_vulnerable_group_requires_full_review(self):
        context = ClassificationContext(
            risk_level=RiskLevel.MEDIUM,
            uses_personal_data=True,
            data_is_anonymized=True,
            involves_vulnerable_group=True,
            is_ai_research=False,
            is_cyber_research=False,
        )

        result = ClassificationEvaluator.evaluate(context)

        self.assertEqual(
            result,
            ReviewClassification.FULL,
        )

    def test_high_risk_requires_full_review(self):
        context = ClassificationContext(
            risk_level=RiskLevel.HIGH,
            uses_personal_data=False,
            data_is_anonymized=False,
            involves_vulnerable_group=False,
            is_ai_research=False,
            is_cyber_research=False,
        )

        result = ClassificationEvaluator.evaluate(context)

        self.assertEqual(
            result,
            ReviewClassification.FULL,
        )

    def test_no_personal_data_is_exempt(self):
        context = ClassificationContext(
            risk_level=RiskLevel.LOW,
            uses_personal_data=False,
            data_is_anonymized=False,
            involves_vulnerable_group=False,
            is_ai_research=False,
            is_cyber_research=False,
        )

        result = ClassificationEvaluator.evaluate(context)

        self.assertEqual(
            result,
            ReviewClassification.EXEMPT,
        )

    def test_anonymized_personal_data_with_medium_risk_is_simplified(self):
        context = ClassificationContext(
            risk_level=RiskLevel.MEDIUM,
            uses_personal_data=True,
            data_is_anonymized=True,
            involves_vulnerable_group=False,
            is_ai_research=False,
            is_cyber_research=False,
        )

        result = ClassificationEvaluator.evaluate(context)

        self.assertEqual(
            result,
            ReviewClassification.SIMPLIFIED,
        )

    def test_non_anonymized_personal_data_cannot_be_automatically_classified(
        self,
    ):
        context = ClassificationContext(
            risk_level=RiskLevel.MEDIUM,
            uses_personal_data=True,
            data_is_anonymized=False,
            involves_vulnerable_group=False,
            is_ai_research=False,
            is_cyber_research=False,
        )

        result = ClassificationEvaluator.evaluate(context)

        self.assertIsNone(result)

    def test_low_risk_anonymized_personal_data_cannot_be_automatically_classified(
        self,
    ):
        context = ClassificationContext(
            risk_level=RiskLevel.LOW,
            uses_personal_data=True,
            data_is_anonymized=True,
            involves_vulnerable_group=False,
            is_ai_research=False,
            is_cyber_research=False,
        )

        result = ClassificationEvaluator.evaluate(context)

        self.assertIsNone(result)

    def test_high_risk_takes_precedence_over_exempt_condition(self):
        context = ClassificationContext(
            risk_level=RiskLevel.HIGH,
            uses_personal_data=False,
            data_is_anonymized=False,
            involves_vulnerable_group=False,
            is_ai_research=False,
            is_cyber_research=False,
        )

        result = ClassificationEvaluator.evaluate(context)

        self.assertEqual(
            result,
            ReviewClassification.FULL,
        )

    def test_ai_research_takes_precedence_over_exempt_condition(self):
        context = ClassificationContext(
            risk_level=RiskLevel.LOW,
            uses_personal_data=False,
            data_is_anonymized=False,
            involves_vulnerable_group=False,
            is_ai_research=True,
            is_cyber_research=False,
        )

        result = ClassificationEvaluator.evaluate(context)

        self.assertEqual(
            result,
            ReviewClassification.FULL,
        )

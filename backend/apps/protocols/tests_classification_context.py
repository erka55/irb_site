from django.test import SimpleTestCase

from apps.protocols.enums import RiskLevel
from apps.protocols.rules.classification import ClassificationContext
from apps.protocols.rules.classification_context import (
    ClassificationContextFactory,
)


class ClassificationContextFactoryTests(SimpleTestCase):

    def test_factory_builds_context_from_protocol_version_snapshot(self):
        snapshot = {
            "risk_level": RiskLevel.MEDIUM,
            "uses_personal_data": True,
            "data_is_anonymized": True,
            "involves_vulnerable_group": False,
            "is_ai_research": False,
            "is_cyber_research": False,
        }

        context = ClassificationContextFactory.from_snapshot(snapshot)

        self.assertIsInstance(context, ClassificationContext)
        self.assertEqual(context.risk_level, RiskLevel.MEDIUM)
        self.assertTrue(context.uses_personal_data)
        self.assertTrue(context.data_is_anonymized)
        self.assertFalse(context.involves_vulnerable_group)
        self.assertFalse(context.is_ai_research)
        self.assertFalse(context.is_cyber_research)

    def test_factory_preserves_false_boolean_values(self):
        snapshot = {
            "risk_level": RiskLevel.LOW,
            "uses_personal_data": False,
            "data_is_anonymized": False,
            "involves_vulnerable_group": False,
            "is_ai_research": False,
            "is_cyber_research": False,
        }

        context = ClassificationContextFactory.from_snapshot(snapshot)

        self.assertEqual(context.risk_level, RiskLevel.LOW)
        self.assertFalse(context.uses_personal_data)
        self.assertFalse(context.data_is_anonymized)
        self.assertFalse(context.involves_vulnerable_group)
        self.assertFalse(context.is_ai_research)
        self.assertFalse(context.is_cyber_research)

    def test_factory_reads_risk_level_as_risk_level_enum(self):
        snapshot = {
            "risk_level": "high",
            "uses_personal_data": False,
            "data_is_anonymized": False,
            "involves_vulnerable_group": False,
            "is_ai_research": False,
            "is_cyber_research": False,
        }

        context = ClassificationContextFactory.from_snapshot(snapshot)

        self.assertEqual(context.risk_level, RiskLevel.HIGH)

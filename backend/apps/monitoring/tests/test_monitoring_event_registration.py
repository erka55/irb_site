from django.test import TestCase

from apps.monitoring.handlers import MonitoringHandler
from common.events.bootstrap import register_event_handlers
from common.events.registry import registry
from common.events.types import EventTypes


class MonitoringEventRegistrationTests(TestCase):

    def test_decision_published_registers_monitoring_handler(self):
        register_event_handlers()

        handlers = registry.get_handlers(
            EventTypes.DECISION_PUBLISHED
        )

        self.assertIn(
            MonitoringHandler.handle_decision_published,
            handlers,
        )

    def test_register_event_handlers_does_not_duplicate_monitoring_handler(self):
        register_event_handlers()
        register_event_handlers()

        handlers = registry.get_handlers(
            EventTypes.DECISION_PUBLISHED
        )

        monitoring_handlers = [
            handler
            for handler in handlers
            if handler == MonitoringHandler.handle_decision_published
        ]

        self.assertEqual(
            len(monitoring_handlers),
            1,
        )

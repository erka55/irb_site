from datetime import date

from django.test import SimpleTestCase

from apps.protocols.rules.working_days import WorkingDayRules


class WorkingDayRulesTests(SimpleTestCase):

    def test_add_zero_working_days(self):
        result = WorkingDayRules.add_working_days(
            date(2026, 9, 7),
            0,
        )

        self.assertEqual(result, date(2026, 9, 7))

    def test_add_one_working_day(self):
        result = WorkingDayRules.add_working_days(
            date(2026, 9, 7),
            1,
        )

        self.assertEqual(result, date(2026, 9, 8))

    def test_skips_weekend(self):
        result = WorkingDayRules.add_working_days(
            date(2026, 9, 4),
            1,
        )

        self.assertEqual(result, date(2026, 9, 7))

    def test_three_working_days_from_friday(self):
        result = WorkingDayRules.add_working_days(
            date(2026, 9, 4),
            3,
        )

        self.assertEqual(result, date(2026, 9, 9))

    def test_ten_working_days_from_friday(self):
        result = WorkingDayRules.add_working_days(
            date(2026, 9, 4),
            10,
        )

        self.assertEqual(result, date(2026, 9, 18))

    def test_negative_days_are_rejected(self):
        with self.assertRaises(ValueError):
            WorkingDayRules.add_working_days(
                date(2026, 9, 7),
                -1,
            )

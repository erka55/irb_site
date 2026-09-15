from datetime import date, timedelta


class WorkingDayRules:
    PRELIMINARY_CHECK_DAYS = 3
    CORRECTION_PERIOD_DAYS = 10

    @staticmethod
    def add_working_days(start_date: date, days: int) -> date:
        if days < 0:
            raise ValueError("Working days cannot be negative.")

        current_date = start_date
        remaining_days = days

        while remaining_days:
            current_date += timedelta(days=1)

            if current_date.weekday() < 5:
                remaining_days -= 1

        return current_date

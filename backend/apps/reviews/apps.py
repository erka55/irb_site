from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.reviews"

    def ready(self):
        from common.events.bootstrap import (
            register_event_handlers,
        )

        register_event_handlers()

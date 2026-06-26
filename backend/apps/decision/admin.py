from django.contrib import admin

from apps.decision.models import (
    Decision,
    DecisionCondition,
    DecisionLetter,
)


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display = (
        "protocol",
        "decision_type",
        "decision_date",
        "created_by",
    )

    list_filter = (
        "decision_type",
        "decision_date",
    )

    search_fields = (
        "protocol__protocol_number",
        "protocol__title",
    )


@admin.register(DecisionCondition)
class DecisionConditionAdmin(admin.ModelAdmin):
    list_display = (
        "decision",
        "order",
    )


@admin.register(DecisionLetter)
class DecisionLetterAdmin(admin.ModelAdmin):
    list_display = (
        "decision",
        "version",
        "status",
        "generated_at",
    )

    list_filter = (
        "status",
    )

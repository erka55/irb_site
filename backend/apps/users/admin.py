from django.contrib import admin

from .models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "tenant",
        "role",
        "is_active",
        "created_at",
    )

    list_filter = (
        "role",
        "is_active",
    )

    search_fields = (
        "user__email",
        "tenant__name",
        "tenant__code",
    )

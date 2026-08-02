from django.contrib import admin

from .models import (
    Meeting,
    MeetingParticipant,
    MeetingAgenda,
    MeetingVote,
)

admin.site.register(Meeting)
admin.site.register(MeetingParticipant)
admin.site.register(MeetingAgenda)
admin.site.register(MeetingVote)
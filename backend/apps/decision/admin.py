from django.contrib import admin
from .models.decision import Decision
from .models.condition import Condition
from .models.letter import Letter


class ConditionInline(admin.TabularInline):
    model = Condition
    extra = 1
    fields = ['description', 'is_completed', 'created_at']
    readonly_fields = ['created_at']


class LetterInline(admin.TabularInline):
    model = Letter
    extra = 0
    fields = ['title', 'content', 'created_at']
    readonly_fields = ['created_at']
    show_change_link = True


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display  = ['short_id', 'protocol', 'tenant', 'decision_type',
                     'decided_by', 'quorum_met', 'is_published', 'created_at']
    list_filter   = ['decision_type', 'tenant', 'is_published', 'quorum_met']
    search_fields = ['protocol__title', 'protocol__protocol_number']
    autocomplete_fields = ['protocol', 'tenant', 'decided_by']
    readonly_fields = ['id', 'created_at', 'updated_at', 'is_published', 'published_at']
    inlines       = [ConditionInline, LetterInline]

    def short_id(self, obj):
        return str(obj.id)[:8] + '…'
    short_id.short_description = 'ID'


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ['short_id', 'decision', 'is_completed', 'created_at']
    list_filter  = ['is_completed']
    search_fields = ['description']

    def short_id(self, obj):
        return str(obj.id)[:8] + '…'
    short_id.short_description = 'ID'


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['title', 'decision', 'created_at']
    search_fields = ['title', 'content']

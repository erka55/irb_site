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
    list_display  = ['short_id', 'protocol', 'tenant', 'status', 'decided_by',
                     'created_at', 'condition_count', 'letter_count', 'is_deleted']
    list_filter   = ['status', 'tenant', 'is_deleted']
    search_fields = ['protocol__title', 'protocol__protocol_number']
    autocomplete_fields = ['protocol', 'tenant', 'decided_by']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines       = [ConditionInline, LetterInline]

    def short_id(self, obj):
        return str(obj.id)[:8] + '…'
    short_id.short_description = 'ID'

    def condition_count(self, obj):
        return obj.conditions.count()
    condition_count.short_description = 'Нөхцөл'

    def letter_count(self, obj):
        return obj.letters.count()
    letter_count.short_description = 'Захидал'


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ['short_id', 'decision', 'is_completed', 'created_at', 'is_deleted']
    list_filter  = ['is_completed', 'is_deleted']
    search_fields = ['description']

    def short_id(self, obj):
        return str(obj.id)[:8] + '…'
    short_id.short_description = 'ID'


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['title', 'decision', 'created_at', 'is_deleted']
    list_filter  = ['is_deleted']
    search_fields = ['title', 'content']

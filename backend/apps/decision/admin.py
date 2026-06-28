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
    list_display  = ['id', 'status', 'created_at', 'updated_at', 'condition_count', 'letter_count']
    list_filter   = ['status']
    readonly_fields = ['created_at', 'updated_at']
    inlines       = [ConditionInline, LetterInline]

    def condition_count(self, obj):
        return obj.conditions.count()
    condition_count.short_description = 'Нөхцөл'

    def letter_count(self, obj):
        return obj.letters.count()
    letter_count.short_description = 'Захидал'


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ['id', 'decision', 'is_completed', 'created_at']
    list_filter  = ['is_completed']
    search_fields = ['description']


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['title', 'decision', 'created_at']
    search_fields = ['title', 'content']

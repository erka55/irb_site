from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Membership


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display  = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering      = ['email']

    # AbstractUser-ийн стандарт fieldsets 'username'-г шаарддаг тул
    # email-based User-д тааруулж дахин тодорхойлно
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Хувийн мэдээлэл', {'fields': ('first_name', 'last_name')}),
        ('Эрх', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Огноо', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


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

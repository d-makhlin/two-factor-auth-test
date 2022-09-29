from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
    )
    ordering = ("username",)

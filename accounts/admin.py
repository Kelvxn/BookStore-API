from django.contrib import admin

from .models import MyUser as User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ["username", "first_name", "last_name", "email"]
    search_fields = ["first_name", "last_name"]
    list_per_page = 5
    prepopulated_fields = {"slug": ["first_name", "last_name"]}
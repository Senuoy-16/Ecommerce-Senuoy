from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Account

@admin.register(Account)
class AccountAdmin(ModelAdmin):
    list_display = ['first_name', 'email', 'username']
    search_fields = ['username']
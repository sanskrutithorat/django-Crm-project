from django.contrib import admin
from djangoSolutions.apps.account.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'internal_id')  
    search_fields = ('name',)
    readonly_fields = ('internal_id',)
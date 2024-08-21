from django.contrib import admin
from tgbot.models import User as TelegramUser, BotAdmin, Contract, Speciality
from django.utils.html import format_html


@admin.register(TelegramUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "username", "telegram_id", )
    fields = ("full_name", "username", "telegram_id", )
    search_fields = ("full_name", "username", "telegram_id", )
    list_per_page = 50


@admin.register(BotAdmin)
class BotAdminsAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'user', 'is_active', 'created_at', 'account')
    list_editable = ('is_active',)
    list_display_links = ('id', 'telegram_id')

    def telegram_id(self, obj):
        return str(obj.user.telegram_id)
    
    def account(self, obj):
        return format_html(f'<button><a class="button" href="https://t.me/{obj.user.username}">View Telegram</a></bitton>'  )
    account.short_description = 'Account'
    account.allow_tags = True
    

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'is_internal', 'is_external', 'period_internal', 'period_external')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'code')
    list_per_page = 50
    

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'middle_name', 'phone_number', 'speciality','edu_stage', 'edu_type', 'semester', 'created_at')
    list_display_links = ('id', 'first_name')
    search_fields = ('first_name', 'last_name', 'middle_name', 'phone_number', 'semester')
    list_per_page = 50

    # def speciality(self, obj):
    #     return obj.speciality.name

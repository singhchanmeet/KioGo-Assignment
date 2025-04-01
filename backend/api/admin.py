from django.contrib import admin
from .models import User, AllowedDomains
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'one_time_password', 'pasword_expiry_time', 'is_active')
    search_fields = ('email',)
    list_filter = ('is_active',)
    ordering = ('email',)
    
class AllowedDomainsAdmin(admin.ModelAdmin):
    list_display = ('domain',)
    search_fields = ('domain',)
    ordering = ('domain',)
    
admin.site.register(User, UserAdmin)
admin.site.register(AllowedDomains, AllowedDomainsAdmin)
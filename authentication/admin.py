from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, TokenBlacklist


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin configuration for CustomUser model
    """
    fieldsets = (
        ('Basic Information', {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Contact Information', {'fields': ('phone_number',)}),
        ('Role & Permissions', {'fields': ('role', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Vendor Information', {'fields': ('shop_name', 'shop_description', 'bank_account')}),
        ('Status', {'fields': ('is_verified', 'is_active')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        ('Basic Information', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
        ('Role Assignment', {
            'classes': ('wide',),
            'fields': ('role', 'is_staff'),
        }),
    )
    
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_verified', 'is_active', 'created_at')
    list_filter = ('role', 'is_verified', 'is_active', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        """Override save to ensure admin role is only for superusers"""
        if obj.role == 'admin' and not obj.is_superuser:
            obj.is_superuser = True
            obj.is_staff = True
        super().save_model(request, obj, form, change)


@admin.register(TokenBlacklist)
class TokenBlacklistAdmin(admin.ModelAdmin):
    """
    Admin configuration for TokenBlacklist model
    """
    list_display = ('user', 'blacklisted_at', 'expires_at')
    list_filter = ('blacklisted_at', 'expires_at')
    search_fields = ('user__email',)
    readonly_fields = ('token', 'blacklisted_at')
    ordering = ('-blacklisted_at',)

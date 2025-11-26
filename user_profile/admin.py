from django.contrib import admin
from .models import UserProfile, PurchasedCourse

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('created_at', 'updated_at')

@admin.register(PurchasedCourse)
class PurchasedCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'amount_paid', 'payment_date', 'is_active')
    search_fields = ('user__username', 'user__email', 'course__title')
    list_filter = ('is_active', 'payment_date')

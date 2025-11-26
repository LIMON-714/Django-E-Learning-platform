from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'payment_method', 'course_name', 'amount', 'created_at')
    search_fields = ('name', 'email', 'phone', 'course_name')
    list_filter = ('payment_method', 'created_at')

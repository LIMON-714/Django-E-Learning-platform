from django.urls import path
from . import views

urlpatterns = [
    path('payment-process/', views.payment_process, name='payment-process-no-slug'),
    path('payment-process/<slug:course_slug>/', views.payment_process, name='payment-process'),
    path('payment/<int:payment_id>/', views.payment_page, name='payment'),
    path('payment-success/<int:payment_id>/', views.payment_success, name='payment_success'),
]


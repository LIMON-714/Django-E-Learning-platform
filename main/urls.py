from django.urls import path
from . import views

urlpatterns = [
    path ('',views.home, name='home'),
    path('about/', views.about_us, name='about'), 
    path('contact/', views.contact_us, name='contact'),
    path('service/', views.service, name='service'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
     path('search/', views.search, name='search'),
]

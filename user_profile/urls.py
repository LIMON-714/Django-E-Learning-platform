from django.urls import path
from . import views

app_name = 'user_profile'  # <-- ADD THIS

urlpatterns = [
    path('dashboard/', views.profile_dashboard, name='dashboard'),  
    path('edit/', views.edit_profile, name='edit_profile'), 
    path('courses/', views.user_courses, name='user_courses'),  
    path('courses/cancel/<int:payment_id>/', views.cancel_course, name='cancel_course'),  
    path("add-blog/", views.add_blog, name="add_blog"),
    path('Your_blogs/', views.user_blogs, name='user_blogs'), 
    path('Your_blogs/edit/<int:blog_id>/', views.edit_blog, name='edit_blog'), 
    path('Your_blogs/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),    
]

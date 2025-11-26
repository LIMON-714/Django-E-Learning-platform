from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blogs/<int:blog_id>/comment/', views.add_comment, name='add_comment'),
    path('blogs/<int:blog_id>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('blogs/<int:blog_id>/add-share/', views.add_share, name='add_share'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('course/', views.course_list,name='course'),
    path("category/<slug:slug>/", views.course_by_category, name="course_by_category"),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path("<slug:slug>/review/", views.submit_review, name="submit-review"),
]

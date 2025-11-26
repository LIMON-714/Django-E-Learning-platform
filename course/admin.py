from django.contrib import admin
from .models import Course, CourseCategory, CourseReview

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

class CourseReviewInline(admin.TabularInline):
    model = CourseReview
    extra = 1
    readonly_fields = ("created_at",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "discount_price", "level", "created_at")
    list_filter = ("category", "level")
    search_fields = ("title", "short_description", "features")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CourseReviewInline]

# ⭐ Register CourseReview so it appears in admin menu
@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ("course", "name", "rating", "created_at")
    list_filter = ("course", "rating")
    search_fields = ("name", "comment")

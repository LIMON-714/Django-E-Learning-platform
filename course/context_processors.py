from .models import CourseCategory

def course_categories(request):
    categories = CourseCategory.objects.prefetch_related('courses').all()
    return {
        'nav_categories': categories
    }

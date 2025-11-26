from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, CourseReview, CourseCategory
from django.contrib.auth.decorators import login_required


def course_list(request):
    courses = Course.objects.all()
    return render(request, "course/course.html", {"courses": courses})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    reviews = course.reviews.all()

    return render(request, "course/course_detail.html", {
        "course": course,
        "reviews": reviews,
    })


@login_required
def submit_review(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        name = request.user.get_full_name()  # Logged-in user's full name

        CourseReview.objects.create(
            course=course,
            name=name,
            rating=rating,
            comment=comment
        )
        return redirect("course_detail", slug=slug)

    return redirect("course_detail", slug=slug)


# -----------------------------
# Category-based course list
# -----------------------------
def course_by_category(request, slug):
    category = get_object_or_404(CourseCategory, slug=slug)
    courses = Course.objects.filter(category=category)

    return render(request, "course/category_courses.html", {
        "category": category,
        "courses": courses
    })

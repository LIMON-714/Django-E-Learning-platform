from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, PurchasedCourse
from course.models import Course
from Blogs.models import Blog, Category
from .forms import UserProfileForm, BlogEditForm


# ---------------------- Dashboard ----------------------
@login_required
def profile_dashboard(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    context = {
        "user_profile": user_profile,
        "purchased_courses": PurchasedCourse.objects.filter(user=request.user, is_active=True),
        "user_blogs": Blog.objects.filter(author=request.user),
    }
    return render(request, "user_profile/dashboard.html", context)


# ---------------------- Edit Profile ----------------------
@login_required
def edit_profile(request):
    # Get or create user profile
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile:dashboard')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        "form": form,
        "user_profile": user_profile,
    }
    return render(request, "user_profile/edit_profile.html", context)


# ---------------------- User Courses ----------------------
@login_required
def user_courses(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    courses = PurchasedCourse.objects.filter(user=request.user)

    context = {
        "courses": courses,
        "user_profile": user_profile,
    }
    return render(request, "user_profile/user_courses.html", context)


# ---------------------- Cancel Purchased Course ----------------------
@login_required
def cancel_course(request, payment_id):
    # Get the purchased course record for the logged-in user
    purchased_course = get_object_or_404(
        PurchasedCourse,
        id=payment_id,
        user=request.user
    )

    # Delete the record from the database
    purchased_course.delete()
    return redirect("user_profile:user_courses")


#------------------------------add Blogs--------------------

@login_required
def add_blog(request):
    categories = Category.objects.all()  # Load categories for dropdown

    if request.method == "POST":
        title = request.POST.get("title")
        category_id = request.POST.get("category")
        content = request.POST.get("content")
        photo = request.FILES.get("photo")

        # Validate category
        category = None
        if category_id:
            category = get_object_or_404(Category, id=category_id)

        # Create blog
        Blog.objects.create(
            title=title,
            author=request.user,
            category=category,
            photo=photo,
            content=content
        )
        return redirect("user_profile:user_blogs")

    return render(request, "user_profile/add_blog.html", {"categories": categories})



# ---------------------- User Blogs ----------------------

@login_required
def user_blogs(request):
    blogs = Blog.objects.filter(author=request.user)
    return render(request, "user_profile/user_blogs.html", {"blogs": blogs})


# ---------------------- Edit Blog ----------------------
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    
    categories = Category.objects.all()

    if request.method == "POST":
        form = BlogEditForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("user_profile:user_blogs")
    else:
        form = BlogEditForm(instance=blog)

    context = {
        "form": form,
        "blog": blog,
        "categories": categories,  
    }
    
    return render(request, "user_profile/edit_blog.html", context)


# ---------------------- Delete Blog ----------------------
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    blog.delete()
    return redirect("user_profile:user_blogs")

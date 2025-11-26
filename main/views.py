from django.shortcuts import render,  redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from main.models import TeamMember , Service
from django.contrib import messages
from course.models import Course
from Blogs.models import Blog
from django.db.models import Q
# Create your views here.


def home(request):
    return render(request, 'main/home.html')

def about_us(request):
    members = TeamMember.objects.all()
    return render(request, 'about_us/about_us.html', {'members': members})

def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            subject="New Contact Form Message",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["Your_email"], #-- your email
            fail_silently=False,
        )

        # Add success message
        messages.success(request, f"Thank you {name}! Your message has been sent successfully.")

        # Redirect to the same page to prevent duplicate POST
        return redirect('contact')  # 'contact_us' হলো তোমার url name

    return render(request, 'contact_us/contact_us.html')

@login_required
def service(request):
    services = Service.objects.all()
    return render(request, 'service/service.html', {'services': services})

@login_required
def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)

    # Handle service request form submission
    if request.method == "POST" and request.POST.get("service_id") == str(service.id):
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        full_message = f"Service Requested: {service.name}\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:\n{message}"

        send_mail(
            subject=f"Service Request: {service.name}",
            message=full_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["Your_email"],  #--- your email
            fail_silently=False,
        )

        
        return redirect('service_detail', pk=service.id)

    # Fetch reviews and features for this service
    reviews = service.reviews.all()  # from Review model
    features = service.features.all()  # from ServiceFeature model

    context = {
        'service': service,
        'reviews': reviews,
        'features': features,
    }
    return render(request, 'service/service_detail.html', context)

def search(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        query_words = query.split()  # split query into words
        
        # Courses: all words must appear in title, short_description, or long_description
        course_query = Q()
        for i, word in enumerate(query_words):
            word_filter = Q(title__icontains=word) | Q(short_description__icontains=word) | Q(long_description__icontains=word)
            if i == 0:
                course_query = word_filter
            else:
                course_query &= word_filter
        courses = Course.objects.filter(course_query).distinct()
        
        # Blogs: all words must appear in title, content, or author name
        blog_query = Q()
        for i, word in enumerate(query_words):
            word_filter = Q(title__icontains=word) | Q(content__icontains=word) | Q(author__first_name__icontains=word) | Q(author__last_name__icontains=word)
            if i == 0:
                blog_query = word_filter
            else:
                blog_query &= word_filter
        blogs = Blog.objects.filter(blog_query).distinct()
    
    else:
        courses = Course.objects.none()
        blogs = Blog.objects.none()

    # Ensure the template knows if nothing found
    if not courses.exists() and not blogs.exists():
        courses = None
        blogs = None

    context = {
        'query': query,
        'courses': courses,
        'blogs': blogs,
    }
    return render(request, 'main/search_results.html', context)
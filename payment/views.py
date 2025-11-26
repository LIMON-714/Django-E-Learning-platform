from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from payment.models import Payment
from course.models import Course
from user_profile.models import PurchasedCourse
from django.contrib.auth.decorators import login_required
# ---------------- Payment Process ----------------
@login_required
def payment_process(request, course_slug=None):
    course = None
    final_price = 0
    if course_slug:
        course = get_object_or_404(Course, slug=course_slug)
        final_price = course.price - (course.discount_price or 0)

    payment_methods = ["Card", "Bkash", "Nagad", "Rocket", "Paypal"]

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        payment_method = request.POST.get("payment_method")
        card_number = request.POST.get("card_number")
        mobile_number = request.POST.get("mobile_number")
        paypal_email = request.POST.get("paypal_email")
        course_name = request.POST.get("course_name")

        # --- Save Payment ---
        payment = Payment.objects.create(
            name=name,
            email=email,
            phone=phone,
            payment_method=payment_method,
            card_number=card_number,
            mobile_number=mobile_number,
            paypal_email=paypal_email,
            course_name=course_name,
            amount=final_price,
        )

        # --- Save PurchasedCourse ---
        user = request.user  # logged-in user
        course_obj = Course.objects.filter(title=course_name).first()
        if user and course_obj:
            PurchasedCourse.objects.get_or_create(
                user=user,
                course=course_obj,
                defaults={'amount_paid': final_price, 'is_active': True}
            )

        return redirect("payment_success", payment_id=payment.id)

    return render(request, "payment/payment.html", {
        "course": course,
        "payment_methods": payment_methods,
        "final_price": final_price,
    })


# ---------------- Payment Success ----------------
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    # Find user by email
    user = User.objects.filter(email=payment.email).first()

    # Find course by title
    course = Course.objects.filter(title=payment.course_name).first()

    if user and course:
        # Create PurchasedCourse if not exists
        purchased_course, created = PurchasedCourse.objects.get_or_create(
            user=user,
            course=course,
            defaults={'is_active': True}
        )
        if not created:
            purchased_course.is_active = True
            purchased_course.save()

    return render(request, "payment/payment_success.html", {"payment": payment})


# ---------------- Payment Page ----------------
def payment_page(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    course = None
    if payment.course_name:
        course = Course.objects.filter(title=payment.course_name).first()

    return render(request, "payment/payment_page.html", {
        "payment": payment,
        "course": course,
    })

from django.shortcuts import redirect, render
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator as token_generator

# ---------------- Login View ----------------
def login_view(request):
    # Auto logout user if already logged in
    if request.user.is_authenticated:
        logout(request)
    
    if request.method == 'POST':
        username = request.POST.get('u_name')
        password = request.POST.get('passw')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active: 
                login(request, user)
                next_url = request.GET.get('next', 'home')  
                return redirect(next_url)
            else:
                messages.warning(request, 'Account is inactive! Please activate via email.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password. Please try again!')
            return redirect('login')

    return render(request, 'authentication/login.html')


# ---------------- Register View ----------------
def register(request):
    # Auto logout user if already logged in
    if request.user.is_authenticated:
        logout(request)
    
    if request.method == 'POST':
        username = request.POST.get('Username')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        email = request.POST.get('email')
        pas = request.POST.get('pas')
        con_pas = request.POST.get('con_pas')

        # Username check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken! Please choose another one.")
            return redirect('register')

        # Password match check
        if pas != con_pas:
            messages.error(request, "Password and Confirm Password do not match!")
            return redirect('register')

        # Email check
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered!")
            return redirect('register')

        # Create user as inactive
        my_user = User.objects.create_user(username=username, email=email, password=pas,
                                           first_name=f_name, last_name=l_name, is_active=False)
        my_user.save()

        # ---- Send Email Verification ----
        current_site = get_current_site(request)
        mail_subject = 'Activate your InnoCLave account'
        uid = urlsafe_base64_encode(force_bytes(my_user.pk))
        token = token_generator.make_token(my_user)
        verification_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

        html_message = f"""
        <p>Hi {f_name},</p>
        <p>Thank you for registering at <strong>InnoCLave IT Solution</strong>.</p>
        <p>Please click the link below to activate your account:</p>
        <p><a href="{verification_link}" style="padding:10px 20px;background:#007bff;color:#fff;text-decoration:none;border-radius:5px;">Activate Account</a></p>
        <p>If you did not register, please ignore this email.</p>
        """

        try:
            send_mail(
                subject=mail_subject,
                message='',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False
            )
            
            return render(request, 'authentication/success.html', {
                'message': "Account created! Please check your email to activate your account."
            })
        except Exception as e:
            messages.warning(request, f"Account created but email could not be sent: {e}")
            return render(request, 'authentication/success.html', {
                'message': f"Account created but email could not be sent: {e}"
            })

    return render(request, 'authentication/register.html')




# ---------------- Activate Account ----------------
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated! You can now login.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('register')


# ---------------- Logout ----------------
def singout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

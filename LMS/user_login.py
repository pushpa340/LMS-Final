from django.shortcuts import render

# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from seekho_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings

def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')

        # Validations
        if not username or not email or not password:
            messages.warning(request, "All fields are required.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists.")
            return redirect('register')

        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        # ✅ Send Confirmation Email
        try:
            send_mail(
                subject="Welcome to SeekhoCoding!",
                message=(
                    f"Hi {username},\n\n"
                    f"Your account has been successfully created.\n"
                    f"You can now log in using your email: {email}\n\n"
                    f"Login here: https://yourdomain.com/login\n\n"
                    f"Thank you for joining us!\n\n"
                    f"— SeekhoCoding Team"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print("❌ Email failed:", e)

        messages.success(request, "Registration successful! A confirmation email has been sent.")
        return redirect('login')

    return render(request, 'registration/register.html')


def DO_LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email').strip()
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Both email and password are required.')
            return redirect('login')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('home')  # or 'dashboard'
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

    return render(request, 'registration/login.html')

def PROFILE(request ):
    return render(request,'registration/profile.html')

def PROFILE_UPDATE(request ):
   if request.method == "POST":
      username = request.POST.get('username')
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      email = request.POST.get('email')
      password = request.POST.get('password')
      user_id = request.user.id

      user = User.objects.get(id=user_id)
      user.first_name = first_name
      user.last_name = last_name
      user.username = username
      user.email = email

      if password != None and password != "":
         user.set_password(password)
      user.save()
      messages.success(request,'Profile Are Successfully Updated. ')
      return redirect('profile')
        
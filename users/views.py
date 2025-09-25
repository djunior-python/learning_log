from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string

from .models import CustomUser
from .forms import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # користувач не активний до підтвердження
            user.save()

            # Генеруємо посилання
            activation_link = f"{request.scheme}://{request.get_host()}/users/activate/{user.email_confirmation_token}/"

            # Підтягуємо текст з шаблону
            message = render_to_string("users/email_confirmation_message.txt", {
                "user": user,
                "activation_link": activation_link,
            })

            send_mail(
                subject="Activate your account",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            messages.success(request, "Please check your email to confirm your account.")
            return redirect("users:login")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


def activate_account(request, token):
    user = get_object_or_404(CustomUser, email_confirmation_token=token)

    if user.is_active:
        return render(request, "users/activation_invalid.html")  # вже активований

    user.is_active = True
    user.save()

    login(request, user)
    return render(request, "users/activation_success.html")
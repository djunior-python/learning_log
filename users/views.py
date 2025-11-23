from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CustomUser
from .forms import CustomUserCreationForm, ProfileForm
from .utils import send_activation_email


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Виклик софтової функції для відправки листа з підтвердженням
            send_activation_email(user, request)

            messages.success(request, "Please check your email to confirm your account. The message will most likely end up in your <<Spam>> folder.")
            return redirect("learning_logs:index")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


def activate_account(request, token):
    user = get_object_or_404(CustomUser, email_confirmation_token=token)

    if user.is_active:
        return render(request, "users/activation_invalid.html")

    user.is_active = True
    user.save()
    login(request, user)
    return render(request, "users/activation_success.html")

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=user)

    context = {
        'user_data': user,
        'form': form,
    }
    return render(request, 'users/profile.html', context)
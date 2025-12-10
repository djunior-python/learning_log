from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CustomUser, UserFollow
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

@login_required
def user_profile(request, user_id):
    user_data = get_object_or_404(CustomUser, id=user_id)

    is_following = UserFollow.objects.filter(
        follower=request.user, 
        following=user_data
    ).exists()
    
    topics = user_data.topic_set.filter(is_public=True).order_by('-date_added')

    context = {
        "user_data": user_data,
        "request_user": request.user,
        "is_following": is_following,
        "followers_count": user_data.followers.count(),
        "following_count": user_data.following.count(),
        "topics": topics,
    }

    return render(request, "users/user_profile.html", context)


@login_required
def toggle_follow(request, user_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=400)

    user_to_follow = get_object_or_404(CustomUser, id=user_id)

    # Не даємо підписуватися на себе
    if user_to_follow == request.user:
        return JsonResponse({"error": "You cannot follow yourself"}, status=400)

    follow_obj = UserFollow.objects.filter(
        follower=request.user, 
        following=user_to_follow
    )

    if follow_obj.exists():
        # Якщо запис існує → відписуємося
        follow_obj.delete()
        is_following = False
    else:
        # Якщо нема → створюємо підписку
        UserFollow.objects.create(
            follower=request.user,
            following=user_to_follow
        )
        is_following = True

    return JsonResponse({
        "is_following": is_following,
        "followers_count": user_to_follow.followers.count(),
        "following_count": request.user.following.count(),
    })
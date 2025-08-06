from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """Зареєструвати нових користувачів."""
    if request.method != 'POST':
        # Показати порожню форму реєстрації.
        form = UserCreationForm()
    else:
        # Опрацювати заповнену форму.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Авторизувати користувача та скерувати його на головну сторінку.
            login(request, new_user)
            return redirect('learning_logs:index')

    # Показати порожню або недійсну форму.
    context = {'form': form}
    return render(request, 'registration/register.html', context)

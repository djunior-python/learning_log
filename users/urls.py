"""Визначити регулярні вирази URL"""

from django.urls import path, include
from django.contrib.auth import views

from . import views

app_name = 'users'

urlpatterns = [
    # Додати уставні URL auth(автентифікації).
    path('', include('django.contrib.auth.urls')),
    # Сторінка реєстрації.
    path('register/', views.register, name='register'),
    path("activate/<str:token>/", views.activate_account, name="activate"),
    path('profile/', views.profile_view, name='profile'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path("follow/<int:user_id>/", views.toggle_follow, name="toggle_follow"),
]
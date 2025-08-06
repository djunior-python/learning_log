"""Defines URL patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Головна сторінка
    path('', views.index, name='index'),
    # Сторінка, що відображає всі теми.
    path('topics/', views.topics, name='topics'),
    # Сторінка, присвячена окремій темі.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Сторінка додавання нової теми
    path('new_topic/', views.new_topic, name='new_topic'),
    # Сторінка для додавання нового допису
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Сторінка для редагування допису.
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
    # Сторінка в разі видалення теми.
    path('delete_topic/<int:topic_id>', views.delete_topic, name='delete_topic'),
    # Сторінка в разі видалення допису.
    path('delete_entry/<int:entry_id>', views.delete_entry, name='delete_entry'),
]
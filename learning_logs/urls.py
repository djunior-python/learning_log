"""Defines URL patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Головна сторінка
    path('', views.index, name='index'),
    # Сторінка, що відображає всі теми.
    path('my_topics/', views.my_topics, name='my_topics'),
    # Сторінка, що відображає всі публічні теми.
    path('other_topics/', views.other_topics, name='other_topics'),
    # Сторінка, присвячена окремій темі.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Сторінка для публікації теми
    path('publish_topic/<int:topic_id>/', views.publish_topic, name='publish_topic'),
    # Сторінка присвячена окремому допису.
    path('entry/<int:entry_id>/', views.entry_detail, name='entry_detail'),
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
    # Сторінка для подачі скарги.
    path('complain/<int:topic_id>/', views.create_complaint, name='create_complaint')
]
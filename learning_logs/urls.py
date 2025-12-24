"""Defines URL patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Головна сторінка
    path('', views.index, name='index'),
    # Сторінка, що відображає всі теми.
    path('topics/', views.my_topics, name='topics'),
    # Сторінка, присвячена окремій темі.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Сторінка для публікації теми
    path('publish_topic/<int:topic_id>/', views.publish_topic, name='publish_topic'),
    # Сторінка для сортування тем
    path('filter_topics/', views.filter_topics, name='filter_topics'),
    # Сторінка для лайку теми
    path('like_topic/<int:topic_id>/', views.like_topic, name='like_topic'),
    # Сторінка присвячена окремому допису.
    path('entry/<int:entry_id>/', views.entry_detail, name='entry_detail'),
    # Сторінка додавання нової теми
    path('new_topic/', views.new_topic, name='new_topic'),
    # Сторінка для додавання нового допису
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Сторінка для редагування допису.
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
    # Видалення файлу.
    path('delete_file/<int:file_id>', views.delete_file, name='delete_file'),
    # Видалення зображення.
    path('delete_image/<int:image_id>', views.delete_image, name='delete_image'),
    # Сторінка в разі видалення теми.
    path('delete_topic/<int:topic_id>', views.delete_topic, name='delete_topic'),
    # Сторінка в разі видалення допису.
    path('delete_entry/<int:entry_id>', views.delete_entry, name='delete_entry'),
    # Сторінка для подачі скарги на тему.
    path('complain_topic/<int:topic_id>/', views.create_complaint_topic, name='create_complaint_topic'),
    # Сторінка для подачі скарги на коментар.
    path('complain_comment/<int:comment_id>/', views.create_complaint_comment, name='create_complaint_comment'),
    # Сторінка зі списком силок на профілі користувачів, на яких підписаний поточний користувач.
    path('following/', views.following, name='following'),
    # Сторінка для додавання коментаря до допису.
    path('add_comment/<int:entry_id>/', views.add_comment, name='add_comment'),
    # Сторінка для редагування коментаря.
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    # Сторінка для видалення коментаря.
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    # Сторінка правил спільноти.
    path('community/', views.community, name='community'),
    # Сторінка "Про сайт".
    path('about/', views.about, name='about'),
]
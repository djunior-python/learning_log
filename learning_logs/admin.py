from django.contrib import admin
from .models import Topic, Entry, Comment, ComplaintTopic, ComplaintComment
from django.urls import reverse
from django.utils.html import format_html


class EntryInline(admin.TabularInline):
    model = Entry
    extra = 0


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner', 'is_public', 'date_added')
    list_filter = ('is_public', 'date_added')
    search_fields = ('text', 'owner__user_name') # пошук за назвою теми та за ім'ям власника
    inlines = [EntryInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_public=True).prefetch_related('owner')
    
    def entry_count(self, obj):
        return obj.entry_set.count()
    entry_count.short_description = 'Number of Entries'
    
    
@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'topic', 'topic__owner', 'date_added')
    list_filter = ('topic__is_public', 'date_added')
    search_fields = ('text', 'topic__text', 'topic__owner__user_name') # пошук за назвою теми та за ім'ям власника
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(topic__is_public=True).select_related('topic__owner')
    
    def short_text(self, obj):
        return (obj.text[:50] + '...') if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Зміст'
    
    def topic_owner(self, obj):
        return obj.topic.owner.username
    topic_owner.short_description = 'Topic Owner'
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'entry', 'owner', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('text', 'owner__user_name', 'entry__text') # пошук за текстом коментаря, ім'ям власника та текстом запису
    
    def short_text(self, obj):
        return (obj.text[:30] + '...') if len(obj.text) > 30 else obj.text
    short_text.short_description = 'Comment Text'


@admin.register(ComplaintTopic)
class ComplaintTopicAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "offender", "topic", "status", "created_at")
    list_filter = ("status", "created_at", "offender")
    search_fields = ("text", "owner__user_name", "offender__user_name", "topic__title")
    ordering = ("-created_at",)
    list_editable = ("status",)  
    date_hierarchy = "created_at"
    
    # Поля, які відображаються при відкритті скарги
    readonly_fields = ("owner", "offender", "topic", "text", "created_at")
    fields = ("owner", "offender", "topic", "text", "status", "created_at")
    
    def topic_link(self, obj):
        url = reverse("learning_logs:topic", args=[obj.topic.id])
        return format_html('<a href="{}">{}</a>', url, obj.topic.text)
    topic_link.short_description = "Topic"
    

@admin.register(ComplaintComment)
class ComplaintCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "offender", "comment", "status", "created_at")
    list_filter = ("status", "created_at", "offender")
    search_fields = ("text", "owner__user_name", "offender__user_name", "comment__text")
    ordering = ("-created_at",)
    list_editable = ("status",)  
    date_hierarchy = "created_at"
    
    # Поля, які відображаються при відкритті скарги
    readonly_fields = ("owner", "offender", "comment", "text", "created_at")
    fields = ("owner", "offender", "comment", "text", "status", "created_at")
    
    def comment_link(self, obj):
        url = reverse("learning_logs:entry_detail", args=[obj.comment.entry.id])
        return format_html('<a href="{}">Comment ID {}</a>', url, obj.comment.id)
    comment_link.short_description = "Comment"
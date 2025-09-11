from django.contrib import admin
from .models import Topic, Entry


class EntryInline(admin.TabularInline):
    model = Entry
    extra = 0


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner', 'is_public', 'date_added')
    list_filter = ('is_public', 'date_added')
    search_fields = ('text', 'owner__username') # пошук за назвою теми та за ім'ям власника
    inlines = [EntryInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_public=True).prefetch_related('entrey_set', 'owner')
    
    def entry_count(self, obj):
        return obj.entry_set.count()
    entry_count.short_description = 'Кількість дописів'
    
    
@admin.register(Entry)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'topic', 'topic_owner', 'date_added')
    list_filter = ('topic__is_public', 'date_added')
    search_fields = ('text', 'topic__text', 'topic__owner__username') # пошук за назвою теми та за ім'ям власника
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(topic__is_public=True).select_related('topic__owner')
    
    def short_text(self, obj):
        return (obj.text[:50] + '...') if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Зміст'
    
    def topic_owner(self, obj):
        return obj.topic.owner.username
    topic_owner.short_description = 'Власник теми'
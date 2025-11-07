from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Count
from django.contrib import messages

from .models import Topic, Entry
from .forms import TopicForm, EntryForm, ComplaintForm

# Create your views here.
def check_owner(request, topic):
    """Доступ тільки власнику (для редагування, видалення, додавання записів)."""
    if topic.owner != request.user:
        raise Http404


def check_blocked(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.blocked:
            messages.error(request, "Your account is blocked. Action impossible.")
            return redirect("learning_logs:index")
        return view_func(request, *args, **kwargs)
    return wrapper


def check_owner_or_public(request, topic):
    """Доступ власнику завжди, іншим лише якщо тема публічна (для перегляду)."""
    if topic.owner != request.user and not topic.is_public:
        raise Http404
    

def index(request):
    """Головна сторінка <<Журналу спостережень>>."""
    return render(request, 'learning_logs/index.html')


@login_required
def my_topics(request):
    """Відображає всі мої теми."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topics(request):
    """Відображає всі опублікованні теми."""
    topics = Topic.objects.filter(is_public=True).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Відобразити тему та прив'язані до неї дописи."""
    topic = Topic.objects.get(id=topic_id)
    # Пересвідчитись, що тема належить поточному користувачеві.
    check_owner_or_public(request, topic)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
@check_blocked
def publish_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    check_owner(request, topic)  # функція перевірки власника
    
    if topic.is_public:
        topic.is_public = False
    else:
        topic.is_public = True
    topic.save()
    return redirect('learning_logs:topic', topic_id=topic.id)


@login_required
def filter_topics(request):
    sort = request.GET.get('sort', '-date_added')
    filter_type = request.GET.get('type', 'mine')

    topics = Topic.objects.annotate(likes_count=Count('likes'))

    if filter_type == 'mine':
        topics = topics.filter(owner=request.user)
    elif filter_type == 'public':
        topics = topics.filter(is_public=True)

    topics = topics.order_by(sort)

    html = render_to_string('learning_logs/topics_list.html', {'topics': topics}, request=request)
    return HttpResponse(html)


@login_required
def like_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if not topic.is_public:
        return JsonResponse({'error': 'Not public'}, status=403)

    if topic.owner == request.user:
        return JsonResponse({'error': 'Cannot like your own topic'}, status=400)

    liked = False
    if request.user in topic.likes.all():
        topic.likes.remove(request.user)
    else:
        topic.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': topic.likes.count()
    })


@login_required
def new_topic(request):
    """Додати нову тему."""
    if request.method != 'POST':
        # Жодних даних не відправлено; створити порожню форму.
        form = TopicForm()
    else:
        # відправити POST; обробити дані.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Показати порожню або недійсну форму.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def entry_detail(request, entry_id):
    """Відображає повний допис з прикріпленими файлами."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    check_owner_or_public(request, topic)

    context = {
        'entry': entry,
        'topic': topic,
    }
    return render(request, 'learning_logs/entry_detail.html', context)


@login_required
def new_entry(request, topic_id):
    """Додати нову тему, яка прив'язана до обраної теми."""
    topic = Topic.objects.get(id=topic_id)
    check_owner(request, topic)

    if request.method != 'POST':
        # Жодних даних не надіслано; створити порожню форму.
        form = EntryForm()
    else:
        # Отримати дані у POST-запиті; обробити дані.
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Показати порожню або недійсну форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Редагувати існуючий допис."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_owner(request, topic)

    if request.method != 'POST':
        # Початковий запит; попередньо заповніть форму поточними даними.
        form = EntryForm(instance=entry)
    else:
        # Дані POST надіслано; обробити дані.
        form = EntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    check_owner(request, topic)

    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:index')

    context = {'topic': topic}

    return render(request, 'learning_logs/confirm_delete_topic.html', context)


@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    check_owner(request, topic)

    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry}

    return render(request, 'learning_logs/confirm_delete_entry.html', context)


@login_required
@check_blocked
def create_complaint(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    offender = topic.owner  # вважаємо, що власник теми = порушник

    if request.method == "POST":
        form = ComplaintForm(request.POST, owner=request.user, topic=topic, offender=offender)
        if form.is_valid():
            form.save()
            messages.success(request, "Скаргу надіслано модераторам.")
            return redirect("learning_logs:topic", topic_id=topic.id)
    else:
        form = ComplaintForm(owner=request.user, topic=topic, offender=offender)

    return render(request, "learning_logs/create_complaint.html", {"form": form, "topic": topic})


def community(request):
    return render(request, "learning_logs/community.html")


def about(request):
    return render(request, "learning_logs/about.html")
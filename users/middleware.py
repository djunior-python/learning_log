from django.utils import timezone
from datetime import timedelta
from .models import CustomUser

class DeleteInactiveUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # видаляємо користувачів, які не активні більше 24 годин
        cutoff = timezone.now() - timedelta(hours=24)
        CustomUser.objects.filter(is_active=False, date_joined__lt=cutoff).delete()
        
        response = self.get_response(request)
        return response
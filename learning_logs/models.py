from django.db import models
from django.conf import settings

# Create your models here.
class Topic(models.Model):
    """Тема, яку вивчає користувач."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_topics', blank=True)

    def __str__(self):
        """Повернути рядкове представлення моделі."""
        return self.text

class Entry(models.Model):
    """Якась конкретна інформація до цієї теми."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='entry_images/', blank=True, null=True)
    file = models.FileField(upload_to='entry_files/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Повертає представлення моделі у string."""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text}"
        
class Complaint(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="complaints_made",
        verbose_name="Автор скарги"
    )
    offender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="complaints_received",
        verbose_name="Порушник"
    )
    topic = models.ForeignKey(
        "learning_logs.Topic", 
        on_delete=models.CASCADE, 
        related_name="complaints",
        verbose_name="Тема"
    )
    text = models.TextField("Текст скарги")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Очікує розгляду"),
            ("reviewed", "Розглянута"),
            ("rejected", "Відхилена"),
        ],
        default="pending"
    )
    
    class Meta:
        unique_together = ("owner", "topic")

    def __str__(self):
        return f"Скарга від {self.owner} на {self.offender} ({self.topic})"
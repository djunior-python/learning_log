from django.db import models
from django.conf import settings
from cloudinary_storage.storage import RawMediaCloudinaryStorage, MediaCloudinaryStorage
from .utils.validators import validate_file_size, validate_image_size

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

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Повертає представлення моделі у string."""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text}"
        
class Comment(models.Model):
    """Коментарі до запису."""
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'comments'
        
    def __str__(self):
        return f"Comment by {self.owner} on Entry ID {self.entry.id}, owner: {self.owner}" + ", " + (f"text: {self.text[:30]}..." if len(self.text) > 30 else f"text: {self.text}")
        
class Files(models.Model):
    """Файли, прикріплені до запису."""
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(storage=RawMediaCloudinaryStorage(), upload_to='entry_files/', validators=[validate_file_size], blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """Повертає представлення моделі у string."""
        return f"File for Entry ID {self.entry.id} uploaded at {self.uploaded_at}"
    
class Images(models.Model):
    """Зображення, прикріпленні до запису."""
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='entry_images/', validators=[validate_image_size], blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for Entry ID {self.entry.id} uploaded at {self.uploaded_at}"
        
class ComplaintTopic(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="topic_complaints_made",
        verbose_name="The author of the complaint topic"
    )
    offender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="topic_complaints_received",
        verbose_name="Offender"
    )
    topic = models.ForeignKey(
        "learning_logs.Topic", 
        on_delete=models.CASCADE, 
        related_name="complaints_topics",
        verbose_name="Topic"
    )
    text = models.TextField("Complaint text")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("reviewed", "Reviewed"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )
    
    class Meta:
        unique_together = ("owner", "topic")

    def __str__(self):
        return f"Complaint by {self.owner} against {self.offender} ({self.topic})"
    

class ComplaintComment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="comment_complaints_made",
        verbose_name="The author of the complaint comment"
    )
    offender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="comment_complaints_received",
        verbose_name="Offender"
    )
    comment = models.ForeignKey(
        "learning_logs.Comment", 
        on_delete=models.CASCADE, 
        related_name="complaints_comments",
        verbose_name="Comment"
    )
    text = models.TextField("Complaint text")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("reviewed", "Reviewed"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )
    
    class Meta:
        unique_together = ("owner", "comment")

    def __str__(self):
        return f"Complaint by {self.owner} against {self.offender} ({self.comment})"
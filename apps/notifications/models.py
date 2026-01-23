from django.db import models
from django.contrib.auth.models import User
from apps.posts.models import Post

class Notification(models.Model):
    TYPE_CHOICES = (
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('comment', 'Comment'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} {self.notification_type} {self.recipient}"

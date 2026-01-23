from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.posts.models import Post, Comment
from apps.accounts.models import UserProfile
from .models import Notification

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.user,
            post=instance.post,
            notification_type='comment'
        )

@receiver(m2m_changed, sender=Post.likes.through)
def create_like_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            user = User.objects.get(pk=pk)
            if user != instance.author:
                Notification.objects.create(
                    recipient=instance.author,
                    sender=user,
                    post=instance,
                    notification_type='like'
                )

@receiver(m2m_changed, sender=UserProfile.followers.through)
def create_follow_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            follower = User.objects.get(pk=pk)
            # instance is UserProfile
            # recipient is instance.user
            # sender is follower
            Notification.objects.create(
                recipient=instance.user,
                sender=follower,
                notification_type='follow'
            )

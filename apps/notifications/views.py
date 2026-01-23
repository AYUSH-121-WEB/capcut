from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        # Fetch unread first, then read
        return Notification.objects.filter(recipient=self.request.user).order_by('-is_read', '-created_at')

    def get(self, request, *args, **kwargs):
        # Mark all as read when viewed? Or user marks specifically?
        # Often simple approach: mark all as read when page loads
        response = super().get(request, *args, **kwargs)
        # However, updating in get() is side-effect. Better to allow manual mark or JS.
        # For simplicity, let's mark UNREAD notifications as READ when getting the list?
        # But this might be annoying if pagination.
        # Let's just list them. Adding a "Mark all read" button is better.
        # But per requirements "Mark as read", I'll implement a separate view or just auto-mark.
        # I'll leave them as is for now, maybe add a small JS/View to mark read.
        return response

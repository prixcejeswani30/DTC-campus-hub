from .models import Notification

def site_context(request):
    notifications = []
    if request.user.is_authenticated:
        notifications = list(Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5])
    return {'unread_notifications': notifications}

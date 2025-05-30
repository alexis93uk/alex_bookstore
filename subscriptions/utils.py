from django.utils import timezone

def has_active_subscription(user):
    if not user.is_authenticated:
        return False
    active_subscriptions = user.subscription_set.filter(end_date__gte=timezone.now())
    return active_subscriptions.exists()
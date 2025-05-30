from subscriptions.utils import has_active_subscription

def get_subscribed_user_books(user, book_queryset):
    if has_active_subscription(user):
        return book_queryset
    return book_queryset.filter(is_premium=False)

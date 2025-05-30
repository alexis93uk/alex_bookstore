from datetime import date

def has_active_subscription(user):
    if hasattr(user, 'subscription'):
        if user.subscription.end_date >= date.today():
            return True
    return False

def get_subscribed_user_books(user, book_queryset):
    if has_active_subscription(user):
        return book_queryset
    return book_queryset.filter(is_premium=False)

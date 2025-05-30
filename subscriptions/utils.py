from datetime import date

def has_active_subscription(user):
    """
    Returns True if the user has an active subscription, False otherwise.
    """
    if hasattr(user, 'subscription'):
        if user.subscription.end_date >= date.today():
            return True
    return False
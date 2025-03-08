import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .forms import CancelSubscriptionForm
from .models import Subscription
from django.contrib import messages


@login_required
def subscribe(request):
    try:
        # Get the user's subscription if it exists
        subscription = Subscription.objects.get(user=request.user)
    except Subscription.DoesNotExist:
        subscription = None

    now = timezone.now()

    # Check if subscription exists and is active
    if subscription and subscription.is_active():
        messages.info(request, "You are already subscribed. Please check your profile for details.")
        return redirect('profile')

    # At this point, either no subscription exists, or it is expired/canceled.
    # You can then create a new checkout session to resume or start a subscription.
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 999,  # $9.99 in cents
                    'product_data': {
                        'name': 'Monthly Subscription',
                    },
                },
                'quantity': 1,
            }],
            success_url=request.build_absolute_uri(reverse('payment_success')),
            cancel_url=request.build_absolute_uri(reverse('payment_failed')),
        )
        return redirect(session.url, code=303)

    return render(request, 'subscriptions/subscribe.html', {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})


@login_required
def payment_success(request):
    now = timezone.now()
    sub, created = Subscription.objects.get_or_create(
        user=request.user,
        defaults={'start_date': now, 'end_date': now + timedelta(days=30)}
    )
    
    if not created:
        # If subscription exists but is expired or canceled, resume it
        if sub.end_date <= now:
            sub.start_date = now
            sub.end_date = now + timedelta(days=30)
        else:
            # Subscription is active, so extend it
            sub.end_date += timedelta(days=30)
        sub.save()

    messages.success(request, "Your subscription has been successfully processed.")
    return render(request, 'subscriptions/payment_success.html')


@login_required
def payment_failed(request):
    return render(request, 'subscriptions/payment_failed_page.html')


@login_required
def cancel_subscription(request):
    try:
        subscription = Subscription.objects.get(user=request.user)
    except Subscription.DoesNotExist:
        # If the user doesn't have a subscription, redirect to profile
        return redirect('profile')
        
    if request.method == 'POST':
        form = CancelSubscriptionForm(request.POST)
        if form.is_valid():
            # Cancel the subscription by setting the end_date to now
            subscription.end_date = timezone.now()
            subscription.save()
            return redirect('profile')
    else:
        form = CancelSubscriptionForm()
        
    return render(request, 'subscriptions/cancel_subscription.html', {'form': form})
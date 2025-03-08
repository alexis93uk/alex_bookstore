import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Subscription

@login_required
def subscribe(request):
    if request.method == 'POST':
        # Set Stripe secret key
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Create the checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 999,  # e.g., $9.99 in cents
                    'product_data': {
                        'name': 'Monthly Subscription',
                    },
                },
                'quantity': 1,
            }],
            success_url=request.build_absolute_uri(reverse('payment_success')),
            cancel_url=request.build_absolute_uri(reverse('payment_failed')),
        )
        # Redirect the user to Stripe's checkout page
        return redirect(session.url, code=303)

    # If GET request, just render a page with a "Subscribe" button
    return render(request, 'subscriptions/subscribe.html')


@login_required
def payment_success(request):
    """
    A naive 'success' view — in production, you would verify with Stripe via webhooks,
    but here we'll just create the Subscription immediately.
    """
    # Create or update subscription for the user
    Subscription.objects.create(
        user=request.user,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=30),
    )
    return render(request, 'subscriptions/payment_success.html')


@login_required
def payment_failed(request):
    return render(request, 'subscriptions/payment_failed_page.html')

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Subscription
from django.contrib.auth.decorators import login_required
# Stripe or other payment logic

@login_required
def subscribe(request):
    if request.method == 'POST':
        Subscription.objects.create(
            user=request.user,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )
        return redirect('payment_success')
    return render(request, 'subscriptions/subscribe.html')

def payment_success(request):
    return render(request, 'subscriptions/payment_success.html')

def payment_failed(request):
    return render(request, 'subscriptions/payment_failed.html')

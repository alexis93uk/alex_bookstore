from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    # This can store whether it's an active subscription or not.

    def is_active(self):
        return self.end_date > timezone.now()

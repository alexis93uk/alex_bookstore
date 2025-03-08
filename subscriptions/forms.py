from django import forms

class CancelSubscriptionForm(forms.Form):
    confirm_cancel = forms.BooleanField(
        required=True,
        label="I confirm that I want to cancel my subscription."
    )

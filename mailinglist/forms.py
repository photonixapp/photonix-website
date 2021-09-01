from django import forms
from django.core.exceptions import ValidationError

from .models import List, Subscription, ListUnsubscribes


class UnsubscribeForm(forms.Form):
    email = forms.CharField(widget=forms.HiddenInput())
    token = forms.CharField(widget=forms.HiddenInput())
    unsubscribes = forms.MultipleChoiceField(
        label='Which lists do you want to unsubscribe from?',
        choices=[(l.name, l.name) for l in List.objects.all()], 
        widget=forms.widgets.CheckboxSelectMultiple(),
        required=False
    )
    unsubscribe_all = forms.BooleanField(
        label='Unsubscribe from all communication',
        required=False
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email or '@' not in email:
            raise ValidationError('No email address suppied')
        return email

    def clean_token(self):
        email = self.cleaned_data['email']
        token = self.cleaned_data['token']
        if not token:
            raise ValidationError('No token supplied')
        try:
            Subscription.objects.get(email=email, token=token)
        except Subscription.DoesNotExist:
            raise ValidationError('Invalid token')
        return token

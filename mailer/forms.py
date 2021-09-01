from django import forms

from .models import Template


class MassSendForm(forms.Form):
    template = forms.CharField(widget=forms.widgets.Select)
    recipients = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(MassSendForm, self).__init__(*args, **kwargs)
        choices = [(t.id, t.subject) for t in Template.objects.order_by('-updated_at')]
        self.fields['template'].widget.choices = choices

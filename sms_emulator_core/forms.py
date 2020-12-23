from django import forms

from sms_emulator_core.models import Enterprise


def enterprise_exists(enterprise):
    try:
        Enterprise.objects.get(name=enterprise)
    except Enterprise.DoesNotExist:
        raise forms.ValidationError(
            f"Enterprise with name '{enterprise}' doesn't exist"
        )


class SMSSendForm(forms.Form):
    enterprise = forms.CharField(validators=[enterprise_exists])
    phone_number = forms.CharField()
    sms_message = forms.CharField(required=False)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number'].replace(' ', '')
        return phone_number


class SMSReceiveForm(forms.Form):
    enterprise = forms.CharField(validators=[enterprise_exists])
    from_sender = forms.CharField()
    to = forms.CharField()
    text = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data['from_sender'] = self.data['from']

    def clean(self):
        self.cleaned_data['from'] = self.cleaned_data['from_sender']
        del self.cleaned_data['from_sender']

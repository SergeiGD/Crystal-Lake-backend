from django import forms

from .models import Client

from phonenumber_field.formfields import PhoneNumberField


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone', 'gender']

    phone = PhoneNumberField(region='RU')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        # self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        # self.fields['email'].widget.attrs.update({'class': 'form-control'})
        #self.fields['phone'].widget.attrs.update({'class': 'form-control'})

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class': 'form-control'})

        self.fields['gender'].widget.attrs.update({'class': 'form-select'})
        self.fields['email'].label = 'Электронная почта'

        self.fields['phone'].widget.attrs.update({'type': 'tel'})
        self.fields['phone'].label = 'Телефон'
        self.fields['phone'].widget.attrs.update({'placeholder': '+79999999999'})

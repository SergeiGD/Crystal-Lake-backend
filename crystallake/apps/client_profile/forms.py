from django import forms
from phonenumber_field.formfields import PhoneNumberField

from ..client.models import Client


class ClientLoginForm(forms.Form):
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'Номер телефона'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'Пароль'
    }))


class SendCodeForm(forms.Form):
    code = forms.CharField(required=True, label='СМС код', widget=forms.TextInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'СМС код'
    }))


class ClientPhoneForm(forms.Form):
    phone = PhoneNumberField(region='RU', required=True, widget=forms.TextInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'Номер телефона'
    }))


class ClientPasswordsForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['password1']

    password1 = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(required=True, label='Подтвердите пароль', widget=forms.PasswordInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'Подтвердите пароль'
    }))

    def clean(self):
        form_data = self.cleaned_data

        if form_data['password1'] != form_data['password2']:
            self._errors["password1"] = ["Пароли не совпадают"]

        return form_data


class ClientInfoForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'gender', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'input_field input_field__name', 'placeholder': 'Имя'})
        self.fields['first_name'].label = 'Имя:'

        self.fields['last_name'].widget.attrs.update({'class': 'input_field input_field__name', 'placeholder': 'Фамилия'})
        self.fields['last_name'].label = 'Фамилия:'

        self.fields['email'].widget.attrs.update({'class': 'input_field input_field__email', 'placeholder': 'Эл. почта'})
        self.fields['email'].label = 'Эл. почта:'

        self.fields['gender'].widget.attrs.update({'class': 'select_field input_field'})
        self.fields['gender'].label = 'Пол:'



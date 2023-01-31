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
    code = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'СМС код'
    }))


class ClientPhoneForm(forms.Form):
    phone = PhoneNumberField(region='RU', required=True, widget=forms.TextInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'Номер телефона'
    }))


class ClientPasswordsForm(forms.Form):
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'Подтвердите пароль'
    }))



# class ClientRegisterForm(ClientPasswordsForm):
#     phone = PhoneNumberField(region='RU', required=True, widget=forms.TextInput(attrs={
#         'class': 'login_field input_field',
#         'placeholder': 'Номер телефона'
#     }))




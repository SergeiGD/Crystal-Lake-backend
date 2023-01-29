from django import forms


class ClientLoginForm(forms.Form):

    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'Номер телефона'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login_field input_field',
        'placeholder': 'Пароль'
    }))

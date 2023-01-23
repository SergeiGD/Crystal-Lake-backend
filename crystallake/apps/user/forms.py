from django import forms

from .models import CustomUser

from phonenumber_field.formfields import PhoneNumberField


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'gender']

    phone = PhoneNumberField(region='RU')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control'})

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class': 'form-control'})

        self.fields['gender'].widget.attrs.update({'class': 'form-select'})
        self.fields['email'].label = 'Электронная почта'

        self.fields['phone'].widget.attrs.update({'type': 'tel'})
        self.fields['phone'].label = 'Телефон'
        self.fields['phone'].widget.attrs.update({'placeholder': '+79999999999'})


class SearchUserForm(forms.Form):
    # SORT_CHOICES = (
    #     ('id', ''),
    #     ('-id', ''),
    #     ('first_name', ''),
    #     ('-first_name', ''),
    #     ('phone', ''),
    #     ('-phone', ''),
    #     ('email', ''),
    #     ('-email', ''),
    # )

    id = forms.IntegerField(label='id', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    phone = forms.CharField(label='Номер телефона', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.CharField(label='Электронная почта', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    sort_by = forms.CharField(required=False, initial='id', widget=forms.TextInput(attrs={
        'class': 'd-none sorting_input',
        'value': 'id'
    }))
    page = forms.IntegerField(required=False, initial=1, widget=forms.NumberInput(attrs={
        'class': 'd-none page_input',
    }))


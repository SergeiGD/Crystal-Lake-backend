from django import forms

from .models import Worker


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['salary', 'additional_info', 'first_name', 'last_name', 'email', 'phone', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({'class': 'form-control'})

        self.fields['phone'].widget.attrs.update({'type': 'tel'})
        self.fields['phone'].label = 'Телефон'
        self.fields['phone'].widget.attrs.update({'placeholder': '+79999999999'})

        self.fields['additional_info'].widget.attrs.update({'class': 'form-control rounded-bottom rounded-0 h-10r'})
        self.fields['gender'].widget.attrs.update({'class': 'form-select'})
        self.fields['email'].label = 'Электронная почта'

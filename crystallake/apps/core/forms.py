from django import forms


class ShortSearchForm(forms.Form):
    name = forms.CharField(max_length=255, label='Наименование', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    id = forms.CharField(max_length=255, label='id', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

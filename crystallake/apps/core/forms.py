from django import forms


class ShortSearchForm(forms.Form):
    name = forms.CharField(max_length=255, label='Наименование', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    id = forms.CharField(max_length=255, label='id', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    sort_by = forms.CharField(required=False, initial='id', widget=forms.TextInput(attrs={
        'class': 'd-none sorting_input',
        'value': 'id'
    }))
    page = forms.IntegerField(required=False, initial=1, widget=forms.NumberInput(attrs={
        'class': 'd-none page_input',
    }))

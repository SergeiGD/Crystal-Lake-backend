from django import forms

from .models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].label = 'Наименование'


class SearchTagForm(forms.Form):
    name = forms.CharField(max_length=255, label='Наименование', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    id = forms.CharField(max_length=255, label='id', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

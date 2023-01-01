from django import forms

from .models import GroupProxy


class GroupForm(forms.ModelForm):
    class Meta:
        model = GroupProxy
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].label = 'Наименование'

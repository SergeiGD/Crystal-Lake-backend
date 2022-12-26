from django import forms

from ..offer.forms import SearchOffersForm, OfferForm
from .models import Service


class ServiceForm(OfferForm):
    class Meta(OfferForm.Meta):
        model = Service
        fields = [*OfferForm.Meta.fields, 'max_for_moment', 'dynamic_timetable']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.short_fields.extend(['max_for_moment'])
        self.number_fields.extend(['max_for_moment'])

        self.fields['dynamic_timetable'].widget.attrs.update({'class': 'form-check-input'})

        for field in self.fields:
            if str(field) in self.short_fields:
                self.fields[str(field)].widget.attrs.update({'class': 'form-control'})

            if str(field) in self.number_fields:
                self.fields[str(field)].widget.attrs.update({'min': 1})


class SearchServicesForm(SearchOffersForm):

    PERSONS_CHOICES = (
        ('', 'не важно'),
        ('1', '1 человек'),
        ('2', '2 человек'),
        ('3', '3 человек'),
        ('4', '4 человек'),
        ('5', '5 человек'),
    )

    persons = forms.ChoiceField(choices=PERSONS_CHOICES, label='Человек с вами', required=False, widget=forms.Select(attrs={
        'class': 'input_field select_field'
    }))

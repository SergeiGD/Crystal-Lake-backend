from django import forms

from ..offer.forms import SearchOffersForm, OfferForm, SearchOffersAdmin
from .models import Service, ServiceTimetable


class ServiceForm(OfferForm):
    class Meta(OfferForm.Meta):
        model = Service
        fields = [*OfferForm.Meta.fields, 'max_in_group', 'dynamic_timetable']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.short_fields.extend(['max_in_group'])
        self.number_fields.extend(['max_in_group'])

        self.fields['dynamic_timetable'].widget.attrs.update({'class': 'form-check-input'})

        for field in self.fields:
            if str(field) in self.short_fields:
                self.fields[str(field)].widget.attrs.update({'class': 'form-control'})

            if str(field) in self.number_fields:
                self.fields[str(field)].widget.attrs.update({'min': 1})

    def clean_name(self):
        name = self.cleaned_data.get("name")
        pk = self.instance.pk
        if Service.objects.filter(date_deleted=None, name=name).exclude(pk=pk):
            raise forms.ValidationError('Услуга с таким наименованием уже существует', code='unique')

        return name


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


class SearchServicesAdmin(SearchOffersAdmin):
    time_from = forms.DateField(label='с', required=False, widget=forms.TimeInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1'
    }))
    time_until = forms.DateField(label='до', required=False, widget=forms.TimeInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1'
    }))


class TimetableForm(forms.Form):
    # TODO: СДЕЛАТЬ МОДЕЛАКОЙ ДЛЯ CLEAR модели

    timetable_id = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={
        'class': 'd-none'
    }))
    date = forms.DateField(label='Дата', widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))
    start = forms.TimeField(label='Начало', widget=forms.TimeInput(attrs={
        'class': 'form-control',
        'type': 'time'
    }))
    end = forms.TimeField(label='Конец', widget=forms.TimeInput(attrs={
        'class': 'form-control',
        'type': 'time'
    }))


class SearchTimetablesAdmin(forms.Form):
    start = forms.DateField(label='с', required=False, widget=forms.DateInput(attrs={
        'class': 'form-control w-100  rounded-end flex-grow-0 flex-shrink-1',
        'type': 'date'
    }))
    end = forms.DateField(label='до', required=False, widget=forms.DateInput(attrs={
        'class': 'form-control w-100  rounded-end flex-grow-0 flex-shrink-1',
        'type': 'date'
    }))

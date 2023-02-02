from datetime import datetime
from django.utils import timezone

from django import forms

from ..offer.forms import SearchOffersForm, OfferForm, SearchOffersAdmin, BookOfferForm
from .models import Service, ServiceTimetable


class ServiceForm(OfferForm):
    class Meta(OfferForm.Meta):
        model = Service
        fields = [*OfferForm.Meta.fields, 'max_in_group', 'max_intersections']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.short_fields.extend(['max_in_group', 'max_intersections'])
        self.number_fields.extend(['max_in_group', 'max_intersections'])

        for field in self.fields:
            if str(field) in self.short_fields:
                self.fields[str(field)].widget.attrs.update({'class': 'form-control'})

            if str(field) in self.number_fields:
                self.fields[str(field)].widget.attrs.update({'min': 1})

    # def clean_name(self):
    #     name = self.cleaned_data.get("name")
    #     pk = self.instance.pk
    #     if Service.objects.filter(date_deleted=None, name=name).exclude(pk=pk):
    #         raise forms.ValidationError('Услуга с таким наименованием уже существует', code='unique')
    #
    #     return name


class SearchServicesForm(SearchOffersForm):

    PERSONS_CHOICES = (
        ('', 'не важно'),
        ('1', '1 человек'),
        ('2', '2 человек'),
        ('3', '3 человек'),
        ('4', '4 человек'),
        ('5', '5 человек'),
    )

    persons = forms.ChoiceField(choices=PERSONS_CHOICES, label='Человек:', required=False, widget=forms.Select(attrs={
        'class': 'input_field select_field'
    }))


class SearchServicesAdmin(SearchOffersAdmin):
    time_from = forms.DateField(label='с', required=False, widget=forms.TimeInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1'
    }))
    time_until = forms.DateField(label='до', required=False, widget=forms.TimeInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1'
    }))


class TimetableForm(forms.ModelForm):
    class Meta:
        model = ServiceTimetable
        fields = []

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

    def clean(self):
        cd = self.cleaned_data

        start = datetime.combine(cd['date'], cd['start'])
        end = datetime.combine(cd['date'], cd['end'])
        start, end = timezone.make_aware(start), timezone.make_aware(end)

        self.instance.start = start
        self.instance.end = end
        return cd


class SearchTimetablesAdmin(forms.Form):
    start = forms.DateField(label='с', required=False, widget=forms.DateInput(attrs={
        'class': 'form-control w-100  rounded-end flex-grow-0 flex-shrink-1',
        'type': 'date'
    }))
    end = forms.DateField(label='до', required=False, widget=forms.DateInput(attrs={
        'class': 'form-control w-100  rounded-end flex-grow-0 flex-shrink-1',
        'type': 'date'
    }))


class BookServiceForm(BookOfferForm):
    date = forms.DateField(label='Дата*:', widget=forms.DateInput(attrs={
        'class': 'input_field',
        'type': 'date'
    }))
    time_start = forms.TimeField(label='с', widget=forms.TimeInput(attrs={
        'class': 'input_field',
        'type': 'time'
    }))
    time_end = forms.TimeField(label='до', widget=forms.TimeInput(attrs={
        'class': 'input_field',
        'type': 'time'
    }))
    quantity = forms.IntegerField(label='Человек*:', initial=1,  widget=forms.NumberInput(attrs={
        'class': 'input_field input_field__people'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['value'] = 1

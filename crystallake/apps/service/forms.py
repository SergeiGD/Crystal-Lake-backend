from datetime import datetime, timedelta, time
from django.utils import timezone

from django import forms

from ..offer.forms import SearchOffersForm, OfferForm, SearchOffersAdmin, BookOfferForm
from .models import Service, ServiceTimetable
from ..order.models import PurchaseCountable


class ServiceForm(OfferForm):
    class Meta(OfferForm.Meta):
        model = Service
        fields = [*OfferForm.Meta.fields, 'max_in_group', 'max_intersections', 'min_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.short_fields.extend(['max_in_group', 'max_intersections', 'min_time'])
        self.number_fields.extend(['max_in_group', 'max_intersections', 'min_time'])

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
    time_from = forms.TimeField(label='с', required=False, widget=forms.TimeInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1',
        'type': 'time'
    }))
    time_until = forms.TimeField(label='до', required=False, widget=forms.TimeInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 rounded-end flex-grow-0 flex-shrink-1',
        'type': 'time'
    }))
    max_in_group = forms.IntegerField(label='Человек в группе', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control w-auto mw-100',
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
    start = forms.TimeField(label='Начало', initial=datetime.now(), widget=forms.TimeInput(attrs={
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
        'type': 'date',
    }))
    end = forms.DateField(label='до', required=False, widget=forms.DateInput(attrs={
        'class': 'form-control w-100  rounded-end flex-grow-0 flex-shrink-1',
        'type': 'date'
    }))

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['start'].widget.attrs.update({'value': datetime.today()})


class ServicePurchaseForm(forms.Form):
    # TODO: сделать модальной и вынести валидацию в модель

    date = forms.DateField(label='Дата*:', widget=forms.DateInput(attrs={
        'class': 'input_field',
        'type': 'date'
    }))
    time_start = forms.TimeField(label='Время с*', widget=forms.TimeInput(attrs={
        'class': 'input_field',
        'type': 'time'
    }))
    time_end = forms.TimeField(label='Время до*', widget=forms.TimeInput(attrs={
        'class': 'input_field',
        'type': 'time'
    }))
    quantity = forms.IntegerField(label='Человек*:', widget=forms.NumberInput(attrs={
        'class': 'input_field input_field__people'
    }))

    def clean(self):
        form_data = self.cleaned_data

        if form_data['date'] < datetime.now().date():
            self._errors["date"] = ["Нельзя сделать бронь на уже прошедшую дату"]

        return form_data


class ManageServicePurchaseForm(ServicePurchaseForm):
    def __init__(self, *args, **kwargs):
        self.purchase = kwargs.pop('purchase', None)
        super().__init__(*args, **kwargs)

        self.fields['date'].widget.attrs['value'] = timezone.localtime(self.purchase.end).date()
        self.fields['quantity'].widget.attrs['value'] = self.purchase.quantity
        self.fields['time_start'].widget.attrs['value'] = timezone.localtime(self.purchase.start).time()
        self.fields['time_end'].widget.attrs['value'] = timezone.localtime(self.purchase.end).time()


class BookServiceForm(BookOfferForm, ServicePurchaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['value'] = 1
        self.fields['date'].widget.attrs['value'] = datetime.now().date()


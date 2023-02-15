import datetime

from django import forms
from django.db.models import Q
from django.utils import timezone


from .models import Room
from ..offer.forms import SearchOffersForm, OfferForm, SearchOffersAdmin, BookOfferForm


class RoomForm(OfferForm):
    class Meta(OfferForm.Meta):
        model = Room
        fields = [*OfferForm.Meta.fields, 'rooms', 'floors', 'beds', 'square']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.short_fields.extend(['rooms', 'floors', 'beds', 'square'])
        self.number_fields.extend(['rooms', 'floors', 'beds', 'square'])

        for field in self.fields:
            if str(field) in self.short_fields:
                self.fields[str(field)].widget.attrs.update({'class': 'form-control'})

            if str(field) in self.number_fields:
                self.fields[str(field)].widget.attrs.update({'min': 1})


class SearchRoomsForm(SearchOffersForm):
    ROOMS_CHOICES = (
        ('', 'неважно'),
        ('1', '1 комната'),
        ('2', '2 комната'),
        ('3', '3 комната'),
        ('4', '4 комната'),
        ('5', '5 комнат'),
    )

    BEDS_CHOICES = (
        ('', 'неважно'),
        ('1', '1 человек'),
        ('2', '2 человека'),
        ('3', '3 человека'),
        ('4', '4 человека'),
        ('5', '5 человек'),
    )

    FLOORS_CHOICES = (
        ('', 'неважно'),
        ('1', '1 этаж'),
        ('2', '2 этажа'),
        ('3', '3 этажа'),
        ('4', '4 этажа'),
        ('5', '5 этажей'),
    )
    SORT_CHOICES = (
        *SearchOffersForm.SORT_CHOICES,
        ('beds', 'возрастанию спальных мест'),
        ('-beds', 'убыванию спальных мест'),
        ('rooms', 'возрастанию кол-ва комнат'),
        ('-rooms', 'убыванию кол-ва комнат'),
    )

    rooms = forms.ChoiceField(choices=ROOMS_CHOICES, label='Количество комнат', required=False, widget=forms.Select(attrs={
        'class': 'input_field select_field',
    }))
    floors = forms.ChoiceField(choices=FLOORS_CHOICES, label='Количество этажей', required=False, widget=forms.Select(attrs={
        'class': 'input_field select_field',
    }))
    beds = forms.ChoiceField(choices=BEDS_CHOICES, label='Количество спальных мест', required=False, widget=forms.Select(attrs={
        'class': 'input_field select_field',
    }))


class SearchRoomsAdmin(SearchOffersAdmin):
    beds_from = forms.IntegerField(label='от', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1'
    }))
    beds_until = forms.IntegerField(label='до', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1 rounded-end'
    }))
    rooms_from = forms.IntegerField(label='от', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1'
    }))
    rooms_until = forms.IntegerField(label='до', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1 rounded-end'
    }))


class RoomPurchaseForm(forms.Form):
    date_start = forms.DateField(label='Дата с*', widget=forms.DateInput(attrs={
        'class': 'input_field',
        'type': 'date'
    }))
    date_end = forms.DateField(label='Дата до*', widget=forms.DateInput(attrs={
        'class': 'input_field',
        'type': 'date'
    }))
    multiple_rooms_acceptable = forms.BooleanField(label='Разрешить переезд:', required=False)


class ManageRoomPurchaseForm(RoomPurchaseForm):
    def __init__(self, *args, **kwargs):
        self.purchase = kwargs.pop('purchase', None)
        super().__init__(*args, **kwargs)

        self.fields['date_start'].widget.attrs['value'] = timezone.localtime(self.purchase.start).date()
        self.fields['date_end'].widget.attrs['value'] = timezone.localtime(self.purchase.end).date()


class BookRoomForm(BookOfferForm, RoomPurchaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date_start'].widget.attrs['value'] = timezone.now().date()
        self.fields['date_end'].widget.attrs['value'] = (timezone.now() + datetime.timedelta(days=7)).date()




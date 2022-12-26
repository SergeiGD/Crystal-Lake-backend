from django import forms


from .models import Room
from ..offer.forms import SearchOffersForm, OfferForm


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


# class RoomForm(forms.ModelForm):
#     class Meta:
#         model = Room
#         fields = ['name', 'description', 'default_price', 'weekend_price', 'prepayment_percent',
#                   'refund_percent', 'main_photo', 'rooms', 'floors', 'beds', 'square', 'is_hidden']
#
#     main_photo = forms.ImageField(widget=forms.FileInput)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         self.short_fields = ['name', 'default_price', 'weekend_price', 'beds', 'rooms', 'floors',
#                              'square', 'prepayment_percent', 'refund_percent', 'slug']
#
#         self.number_fields = ['default_price', 'weekend_price', 'beds', 'rooms', 'floors', 'square']
#
#         self.fields['is_hidden'].widget.attrs.update({'class': 'form-check-input'})
#         self.fields['description'].widget.attrs.update({'class': 'form-control rounded-bottom rounded-0 h-15r flex-grow-1'})
#         self.fields['main_photo'].widget.attrs.update({'class': 'upload_img_input d-none', 'accept': 'image/png, image/jpeg, image/jpg'})
#         self.fields['main_photo'].required = False
#         self.fields['name'].error_messages = {'unique': 'номер с таким названием уже существует'}
#
#         for field in self.fields:
#             if str(field) in self.short_fields:
#                 self.fields[str(field)].widget.attrs.update({'class': 'form-control'})
#
#             if str(field) in self.number_fields:
#                 self.fields[str(field)].widget.attrs.update({'min': 1})
#
#     # def clean_name(self):
#     #     name = self.cleaned_data.get("name")
#     #
#     #     if Offer.objects.filter(name=name).exists():
#     #         raise forms.ValidationError('Номер с таким названием уже существует', code='unique required')
#     #     return name
#
#     def clean_main_photo(self):
#         photo = self.cleaned_data.get("main_photo")
#
#         if not photo:
#             raise forms.ValidationError('Главное фото не было выбрано', code='required')
#
#         return photo


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


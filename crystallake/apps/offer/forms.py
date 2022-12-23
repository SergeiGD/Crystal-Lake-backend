from django import forms

from .models import *


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
#         self.short_fields_labels = ['input-group-text', 'w-10r']
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


# class PhotoForm(forms.ModelForm):
#     class Meta:
#         model = Photo
#         fields = ['order', 'path']
#
#     path = forms.ImageField(widget=forms.FileInput(attrs={'class': 'upload_img_input d-none', 'accept': 'image/png, image/jpeg, image/jpg'}))
#     order = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'd-none'}))
#     path.label = ''
#     order.label = ''


# class SearchRoomsForm(forms.Form):
#     ROOMS_CHOICES = (
#         ('', 'неважно'),
#         ('1', '1 комната'),
#         ('1', '2 комната'),
#         ('1', '3 комната'),
#         ('1', '4 комната'),
#         ('1', '5 комнат'),
#     )
#
#     BEDS_CHOICES = (
#         ('', 'неважно'),
#         ('1', '1 человек'),
#         ('1', '2 человека'),
#         ('1', '3 человека'),
#         ('1', '4 человека'),
#         ('1', '5 человек'),
#     )
#
#     FLOORS_CHOICES = (
#         ('', 'неважно'),
#         ('1', '1 этаж'),
#         ('1', '2 этажа'),
#         ('1', '3 этажа'),
#         ('1', '4 этажа'),
#         ('1', '5 этажей'),
#     )
#
#     SORT_CHOICES = (
#         ('default_price', 'возрастанию цен'),
#         ('-default_price', 'убыванию цен'),
#         ('beds', 'возрастанию спальных мест'),
#         ('-beds', 'убыванию спальных мест'),
#         ('rooms', 'возрастанию кол-ва комнат'),
#         ('-rooms', 'убыванию кол-ва комнат'),
#     )
#
#     name = forms.CharField(max_length=255, label='Наименование', required=False, widget=forms.TextInput(attrs={
#         'class': 'input_field input_field__name'
#     }))
#     price_from = forms.DecimalField(label='от', required=False, widget=forms.NumberInput(attrs={
#         'class': 'input_field input_field__price'
#     }))
#     price_until = forms.DecimalField(label='до', required=False, widget=forms.NumberInput(attrs={
#         'class': 'input_field input_field__price'
#     }))
#     date_from = forms.DateField(label='с', required=False, widget=forms.DateInput(attrs={
#         'class': 'input_field input_field__date',
#         'type': 'date'
#     }))
#     date_until = forms.DateField(label='до', required=False, widget=forms.DateInput(attrs={
#         'class': 'input_field input_field__date',
#         'type': 'date'
#     }))
#     rooms = forms.ChoiceField(choices=ROOMS_CHOICES, label='Количество комнат', required=False, widget=forms.Select(attrs={
#         'class': 'input_field select_field',
#     }))
#     floors = forms.ChoiceField(choices=FLOORS_CHOICES, label='Количество этажей', required=False, widget=forms.Select(attrs={
#         'class': 'input_field select_field',
#     }))
#     beds = forms.ChoiceField(choices=BEDS_CHOICES, label='Количество спальных мест', required=False, widget=forms.Select(attrs={
#         'class': 'input_field select_field',
#     }))
#     sort_by = forms.ChoiceField(choices=SORT_CHOICES, label='Сортировать по', required=False, widget=forms.Select(attrs={
#         'class': 'select_sortby',
#     }))



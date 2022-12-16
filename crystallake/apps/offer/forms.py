from django import forms

from .models import *


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'default_price', 'weekend_price', 'prepayment_percent',
                  'refund_percent', 'main_photo', 'rooms', 'floors', 'beds', 'square', 'is_hidden']

    main_photo = forms.ImageField(widget=forms.FileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.short_fields = ['name', 'default_price', 'weekend_price', 'beds', 'rooms', 'floors',
                             'square', 'prepayment_percent', 'refund_percent', 'slug']

        self.short_fields_labels = ['input-group-text', 'w-10r']

        self.number_fields = ['default_price', 'weekend_price', 'beds', 'rooms', 'floors', 'square']

        self.fields['is_hidden'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['description'].widget.attrs.update({'class': 'form-control rounded-bottom rounded-0 h-15r'})
        self.fields['main_photo'].widget.attrs.update({'class': 'upload_img_input d-none', 'accept': 'image/png, image/jpeg'})
        self.fields['main_photo'].required = False
        self.fields['name'].error_messages = {'unique': 'номер с таким названием уже существует'}

        for field in self.fields:
            if str(field) in self.short_fields:
                self.fields[str(field)].widget.attrs.update({'class': 'form-control'})

            if str(field) in self.number_fields:
                self.fields[str(field)].widget.attrs.update({'min': 1})

    # def clean_name(self):
    #     name = self.cleaned_data.get("name")
    #
    #     if Offer.objects.filter(name=name).exists():
    #         raise forms.ValidationError('Номер с таким названием уже существует', code='unique required')
    #     return name

    def clean_main_photo(self):
        photo = self.cleaned_data.get("main_photo")

        if not photo:
            raise forms.ValidationError('Главное фото не было выбрано', code='required')

        return photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['order', 'path']

    path = forms.ImageField(widget=forms.FileInput(attrs={'class': 'upload_img_input d-none', 'accept': 'image/png, image/jpeg"'}))
    order = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'd-none'}))
    path.label = ''
    order.label = ''


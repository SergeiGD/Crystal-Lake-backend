from django import forms
from phonenumber_field.formfields import PhoneNumberField, RegionalPhoneNumberWidget

from .models import Offer


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'name',
            'description',
            'default_price',
            'weekend_price',
            'prepayment_percent',
            'refund_percent',
            'main_photo',
            'is_hidden'
        ]

    main_photo = forms.ImageField(widget=forms.FileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.short_fields = ['name', 'default_price', 'weekend_price', 'prepayment_percent', 'refund_percent', 'slug']

        self.number_fields = ['default_price', 'weekend_price']

        self.fields['is_hidden'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control rounded-bottom rounded-0 h-15r flex-grow-1'}
        )
        self.fields['main_photo'].widget.attrs.update(
            {'class': 'upload_img_input d-none', 'accept': 'image/png, image/jpeg, image/jpg'}
        )
        self.fields['main_photo'].required = False

        for field in self.fields:
            if str(field) in self.short_fields:
                self.fields[str(field)].widget.attrs.update({'class': 'form-control'})

            if str(field) in self.number_fields:
                self.fields[str(field)].widget.attrs.update({'min': 1})

    def clean_main_photo(self):
        photo = self.cleaned_data.get("main_photo")

        if not photo:
            raise forms.ValidationError('Главное фото не было выбрано', code='required')

        return photo


class SearchOffersForm(forms.Form):

    SORT_CHOICES = (
        ('default_price', 'возрастанию цен'),
        ('-default_price', 'убыванию цен'),
    )

    date_from = forms.DateField(label='с', required=False, widget=forms.DateInput(attrs={
        'class': 'input_field input_field__date',
        'type': 'date'
    }))
    date_until = forms.DateField(label='до', required=False, widget=forms.DateInput(attrs={
        'class': 'input_field input_field__date',
        'type': 'date'
    }))
    name = forms.CharField(max_length=255, label='Наименование', required=False, widget=forms.TextInput(attrs={
        'class': 'input_field input_field__name'
    }))
    price_from = forms.DecimalField(label='от', required=False, widget=forms.NumberInput(attrs={
        'class': 'input_field input_field__price'
    }))
    price_until = forms.DecimalField(label='до', required=False, widget=forms.NumberInput(attrs={
        'class': 'input_field input_field__price'
    }))
    sort_by = forms.ChoiceField(label='Сортировать по', required=False, widget=forms.Select(attrs={
        'class': 'select_sortby',
    }))

    @classmethod
    def get_sort_choices(cls):      # получаем через метод класса, чтоб брал значение текущего класса, а не
        return cls.SORT_CHOICES     # все время базового

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sort_by'].choices = self.get_sort_choices()


class SearchOffersAdmin(forms.Form):
    id = forms.IntegerField(label='id', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control w-auto mw-100'
    }))
    name = forms.CharField(label='Наименование', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    dates_from = forms.DateField(label='с', required=False, widget=forms.DateInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1',
        'type': 'date'
    }))
    dates_until = forms.DateField(label='до', required=False, widget=forms.DateInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1 rounded-end',
        'type': 'date'
    }))
    price_from = forms.IntegerField(label='от', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1'
    }))
    price_until = forms.IntegerField(label='до', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1 rounded-end'
    }))
    weekend_price_from = forms.IntegerField(label='от', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1'
    }))
    weekend_price_until = forms.IntegerField(label='до', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control w-100 mw-10r rounded-0 flex-grow-0 flex-shrink-1 rounded-end'
    }))
    sort_by = forms.CharField(required=False, initial='id', widget=forms.TextInput(attrs={
        'class': 'd-none sorting_input',
        'value': 'id'
    }))
    page = forms.IntegerField(required=False, initial=1, widget=forms.NumberInput(attrs={
        'class': 'd-none page_input',
    }))
        

class BookOfferForm(forms.Form):
    first_name = forms.CharField(label='Ваше имя:', required=False, widget=forms.TextInput(attrs={
        'class': 'input_field input_field__name',
    }))
    last_name = forms.CharField(label='Ваша фамилия:', required=False, widget=forms.TextInput(attrs={
        'class': 'input_field input_field__name',
    }))
    phone = PhoneNumberField(
        region='RU',
        label='Номер телефона*:',
        required=True,
        error_messages={
            'invalid': 'Неверный номер номера телефона. Пример: +79999999999 или 8(999)999-99-99'
        },
        widget=RegionalPhoneNumberWidget(attrs={
            'class': 'input_field input_field__phone',
            'placeholder': '+79999999999'
            }
        ))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user is not None and self.user.is_authenticated:
            # self.fields['phone'].disabled = True
            self.fields['phone'].widget.attrs['value'] = self.user.phone
            self.fields['phone'].widget.attrs['readonly'] = ''

            # self.fields['first_name'].disabled = True
            self.fields['first_name'].widget.attrs['value'] = self.user.first_name
            self.fields['first_name'].widget.attrs['readonly'] = ''

            # self.fields['last_name'].disabled = True
            self.fields['last_name'].widget.attrs['value'] = self.user.last_name
            self.fields['last_name'].widget.attrs['readonly'] = ''





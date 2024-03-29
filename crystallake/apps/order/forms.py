from django import forms

from .models import Order, Purchase, PurchaseCountable
from .status_choises import get_status_by_name, STATUS_CHOICES, STATUS_CHOICES_SEARCH


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['comment']

    client_name = forms.CharField(label='Клиент', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'readonly': ''
    }))
    client_id = forms.IntegerField(widget=forms.HiddenInput(attrs={
        'class': 'd-none'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['comment'].widget.attrs.update({'class': 'form-control rounded-bottom rounded-0 h-10r'})
        self.fields['comment'].label = 'Комментарий'


class EditOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['comment', 'paid']

    refund_made = forms.BooleanField(label='Средства возвращены', required=False, widget=forms.CheckboxInput(attrs={
        'class': 'btn-check'
    }))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'btn-check'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['status'].initial = get_status_by_name(self.instance.status)

        if not self.instance.is_editable():
            self.fields['comment'].disabled = True
            self.fields['paid'].disabled = True

        if self.instance.left_to_refund == 0:
            self.fields['refund_made'].disabled = True

        self.fields['comment'].widget.attrs.update({'class': 'form-control rounded-bottom rounded-0 h-10r'})
        self.fields['paid'].widget.attrs.update({'class': 'form-control rounded-bottom rounded-0'})


class SearchOrdersAdmin(forms.Form):
    id = forms.IntegerField(label='id', required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    status = forms.ChoiceField(label='Статус заказа', choices=STATUS_CHOICES_SEARCH, required=False, widget=forms.Select(attrs={
        'class': 'form-select w-100 mw-10r flex-grow-0 flex-shrink-1'
    }))
    client_id = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={
        'class': 'd-none'
    }))
    client_name = forms.CharField(label='Клиент', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-0 rounded-start',
        'readonly': ''
    }))
    sort_by = forms.CharField(required=False, initial='id', widget=forms.TextInput(attrs={
        'class': 'd-none sorting_input',
        'value': 'id'
    }))
    page = forms.IntegerField(required=False, initial=1, widget=forms.NumberInput(attrs={
        'class': 'd-none page_input',
    }))


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = []

    purchase_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)


class RoomPurchaseForm(PurchaseForm):
    class Meta(PurchaseForm.Meta):
        fields = [*PurchaseForm.Meta.fields, 'start', 'end']
        widgets = {
            'start': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    room_id = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={
        'class': 'd-none'
    }))

    multiple_rooms_acceptable = forms.BooleanField(
        label='Разрешить подбор нескольких комнат',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'btn-check',
            'type': 'checkbox',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start'].label = 'Заселение'
        self.fields['end'].label = 'Выселение'


class ServicePurchaseForm(PurchaseForm):
    class Meta(PurchaseForm.Meta):
        model = PurchaseCountable
        fields = [*PurchaseForm.Meta.fields, 'quantity']

    service_id = forms.IntegerField(required=False, widget=forms.HiddenInput(attrs={
        'class': 'd-none'
    }))
    day = forms.DateField(label='Дата', required=False, widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'date'
    }))
    time_start = forms.TimeField(label='Время начала', required=False, widget=forms.TimeInput(attrs={
        'class': 'form-control',
        'type': 'time'
    }))
    time_end = forms.TimeField(label='Время конца', required=False, widget=forms.TimeInput(attrs={
        'class': 'form-control',
        'type': 'time'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].initial = 1
        self.fields['quantity'].label = 'Количество'







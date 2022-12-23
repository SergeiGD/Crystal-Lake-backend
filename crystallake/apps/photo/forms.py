from django import forms

from .models import Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['order', 'path']

    path = forms.ImageField(widget=forms.FileInput(attrs={'class': 'upload_img_input d-none', 'accept': 'image/png, image/jpeg, image/jpg'}))
    order = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'd-none'}))
    path.label = ''
    order.label = ''

from django import forms
from .models import BMPImage


class BMPImageForm(forms.ModelForm):
    class Meta:
        model = BMPImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'accept': '.bmp'})
        }


class ExtendedBMPImageForm(BMPImageForm):
    class Meta(BMPImageForm.Meta):
        fields = BMPImageForm.Meta.fields + ['build_type', 'color_combination']
        widgets = BMPImageForm.Meta.widgets.copy()
        widgets.update({
            'build_type': forms.Select(),
            'color_combination': forms.Select()
        })

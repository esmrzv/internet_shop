from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    forbidden_words = ['казино',
                       'криптовалюта',
                       'крипта',
                       'биржа',
                       'дешево',
                       'бесплатно',
                       'обман',
                       'полиция',
                       'радар']

    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if name:
            for word in self.forbidden_words:
                if word in name.lower():
                    raise ValidationError(f'Название содержит запрещенное слово: {word}')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'


class ProductManageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'is_published', 'description',)


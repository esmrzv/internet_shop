from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product


class ProductForm(forms.ModelForm):
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

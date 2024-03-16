from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Version


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        name = self.cleaned_data['name'].lower()
        for word in forbidden_words:
            if word in name:
                raise ValidationError(f'Название не должно содержать запрещенное слово: {word}')
        return name

    def clean_description(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        description = self.cleaned_data['description'].lower()
        for word in forbidden_words:
            if word in description:
                raise ValidationError(f'Описание не должно содержать запрещенное слово: {word}')
        return description


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current_version']

    # Дополнительные настройки формы, если необходимо
    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        # Пример: добавление классов Bootstrap к полям формы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['is_current_version'].widget = forms.CheckboxInput()


class ProductDescriptionForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['description']

    def __init__(self, *args, **kwargs):
        super(ProductDescriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'description',
            Submit('submit', 'Сохранить')
        )


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category']
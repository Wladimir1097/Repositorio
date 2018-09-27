from django.forms import *
from .models import *


class ProviderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Provider
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'mobile': TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'address': TextInput(attrs={'placeholder': 'Ingrese un teléfono'}),
            'email': TextInput(attrs={'placeholder': 'Ingrese un correo'})
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'description': Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class BrandForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Brand
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class IngressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prov'].widget.attrs['autofocus'] = True

    class Meta:
        model = Ingress
        fields = '__all__'
        widgets = {
            'prov': Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}),
            'date_joined': DateInput(format='%Y-%m-%d',attrs={'value': datetime.now().strftime('%Y-%m-%d')}),
            'subtotal': TextInput(),
            'iva': TextInput(),
            'dscto': TextInput(),
            'total': TextInput()
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'cat': Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}),
            'brand': Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}),
            'cost': TextInput(),
            'price': TextInput()
        }
        exclude = ['stock']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

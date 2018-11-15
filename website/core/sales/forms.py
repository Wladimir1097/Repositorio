from django.forms import *
from .models import *


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'mobile': TextInput(attrs={'placeholder': 'Ingrese un teléfono'}),
            'address': TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'email': TextInput(attrs={'placeholder': 'Ingrese un email'}),
        }
        exclude = ['bodega']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class ServicesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Services
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'cost': TextInput(),
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class SalesForm(ModelForm):
    def __init__(self, bodega, *args, **kwargs):
        super(SalesForm, self).__init__(*args, **kwargs)
        self.fields['cli'].widget.attrs['autofocus'] = True
        self.fields['cli'].queryset = Client.objects.filter(bodega_id=bodega)

    class Meta:
        model = Sales
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}),
            'date_joined': DateInput(format='%Y-%m-%d', attrs={'value': datetime.now().strftime('%Y-%m-%d')}),
            'date_delivery': DateInput(format='%Y-%m-%d', attrs={'value': datetime.now().strftime('%Y-%m-%d')}),
            'subtotal': TextInput(),
            'iva': TextInput(),
            'dscto': TextInput(),
            'total': TextInput()
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class MedidorForm(ModelForm):
    def __init__(self, bodega, *args, **kwargs):
        super(MedidorForm, self).__init__(*args, **kwargs)
        #self.fields['cli'].queryset = Client.objects.filter(bodega_id=bodega)

    class Meta:
        model = InventoryMedidor
        fields = '__all__'
        widgets = {
            'medtype': Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}),
            'date_joined': DateInput(format='%Y-%m-%d', attrs={'value': datetime.now().strftime('%Y-%m-%d')})
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

from django.forms import *
from .models import *


class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'proprietor': TextInput(attrs={'placeholder': 'Ingrese el nombre del propietario'}),
            'ruc': TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'phone': TextInput(attrs={'placeholder': 'Ingrese un teléfono convencional'}),
            'mobile': TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'email': TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'schedule': TextInput(attrs={'placeholder': 'Ingrese un horario'}),
            'address': TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'mission': Textarea(attrs={'placeholder': 'Ingrese una misión', 'rows': 3, 'cols': 3}),
            'vision': Textarea(attrs={'placeholder': 'Ingrese una visión', 'rows': 3, 'cols': 3}),
            'about_us': Textarea(attrs={'placeholder': 'Ingrese una decripción de acerca de nosotros', 'rows': 3, 'cols': 3}),
        }
        exclude = []

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class ExpensesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs['autofocus'] = True

    class Meta:
        model = Expenses
        fields = '__all__'
        widgets = {
            'cost': TextInput(),
            'type': Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}),
            'date_joined': DateInput(format='%Y-%m-%d',attrs={'value': datetime.now().strftime('%Y-%m-%d'), 'readonly': True}),
            'details': Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        }
        exclude = ['comp']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class TypeExpenseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = TypeExpense
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese una descripción'})
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class ToolsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tools
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese una descripción'}),
            'code': TextInput(attrs={'placeholder': 'Ingrese un código de serie'}),
            'cost': TextInput(),
            'guarantee': TextInput(),
        }
        exclude = ['comp','dep','date_joined']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)
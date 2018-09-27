from django.forms import *
from .models import *


class ContractsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        action = kwargs.pop('action', None)
        super().__init__(*args, **kwargs)
        self.fields['pers'].widget.attrs['autofocus'] = True
        if action:
            super(ContractsForm, self).__init__(*args, **kwargs)
            del self.fields['pers']

    class Meta:
        model = Contracts
        widgets = {
            'pers': Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}),
            'start_date': DateInput(format='%Y-%m-%d',attrs={'value': datetime.now().strftime('%Y-%m-%d'), 'readonly': True}),
            'end_date': DateInput(format='%Y-%m-%d', attrs={'value': datetime.now().strftime('%Y-%m-%d'), 'readonly': True}),
            'rmu': TextInput()
        }
        exclude = ['comp', 'is_active']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class FaultsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        action = kwargs.pop('action', None)
        super().__init__(*args, **kwargs)
        self.fields['cont'].queryset = Contracts.objects.filter(is_active=True)
        self.fields['cont'].widget.attrs['autofocus'] = True
        if action:
            super(FaultsForm, self).__init__(*args, **kwargs)
            del self.fields['cont']

    class Meta:
        model = Faults
        fields = '__all__'
        widgets = {
            'cont': Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}),
            'details': Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'date_joined': DateInput(format='%Y-%m-%d', attrs={'value': datetime.now().strftime('%Y-%m-%d'), 'readonly': True}),
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class SalaryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].widget.attrs['autofocus'] = True

    class Meta:
        model = Salary
        fields = '__all__'
        widgets = {
            'month': Select(
                attrs={'class': 'form-control input-sm selectpicker', 'data-live-search': 'true', 'data-size': '10'}),
            'year': TextInput(attrs={'readonly': True, 'class': 'form-control input-sm', 'value': datetime.now().year})
        }
        exclude = ['cont', 'date_joined', 'total']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class PersonalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Personal
        fields = '__all__'
        widgets = {
            'names': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'dni': TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'mobile': TextInput(attrs={'placeholder': 'Ingrese un teléfono'}),
            'address': TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'email': TextInput(attrs={'placeholder': 'Ingrese un email'})
        }
        exclude = ['comp']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)
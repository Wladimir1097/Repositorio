from django.forms import *
from .models import User
from datetime import datetime


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        type = kwargs.pop('type', None)
        super().__init__(*args, **kwargs)
        self.fields['groups'].required = True
        self.fields['first_name'].widget.attrs['autofocus'] = True
        if type == 'profile':
            super(UserForm, self).__init__(*args, **kwargs)
            del self.fields['groups']

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Ingrese sus nombres'}),
            'username': TextInput(attrs={'placeholder': 'Ingrese un username'}),
            'last_name': TextInput(attrs={'placeholder': 'Ingrese sus apellidos'}),
            'dni': TextInput(attrs={'placeholder': 'Ingrese su número de cedula'}),
            'email': TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'}),
            'phone': TextInput(attrs={'placeholder': 'Ingrese su número de teléfono convencional'}),
            'mobile': TextInput(attrs={'placeholder': 'Ingrese su número de teléfono celular'}),
            'gender': Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
            'job': Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true'}),
            'address': TextInput(attrs={'placeholder': 'Ingrese el nombre de su dirección'}),
            'birthdate': DateInput(format='%Y-%m-%d',attrs={'value': datetime.now().strftime('%Y-%m-%d'), 'readonly': True}),
            'groups': SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple', 'style': 'width:100%'}),
        }
        exclude = ['is_change_password', 'is_active', 'is_staff', 'user_permissions', 'password',
                   'date_joined', 'last_login', 'is_superuser']

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    token = CharField(widget=HiddenInput(), required=False)

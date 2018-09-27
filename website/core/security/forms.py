from django.forms import *
from .models import *


class ModuleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].widget.attrs['autofocus'] = True

    class Meta:
        model = Module
        fields = '__all__'
        widgets = {
            'url': TextInput(attrs={'placeholder': 'Ingrese url'}),
            'type': Select(attrs={'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}),
            'name': TextInput(attrs={'placeholder': 'Ingrese nombre'}),
            'description': TextInput(attrs={'placeholder': 'Ingrese descripción'}),
            'icon': TextInput(attrs={'placeholder': 'ingrese icono de font awesone'}),
        }

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)


class GroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Group
        fields = 'name', 'modules'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese nombre'}),
        }
        exclude = []

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

    modules = ModelMultipleChoiceField(label='Módulos', queryset=Module.objects.all(), widget=SelectMultiple(
        attrs={'class': 'select2', 'multiple': 'multiple', 'style': 'width:100%'}))


class ModuleTypeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = ModuleType
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'icon': TextInput(attrs={'placeholder': 'ingrese un icono de font awesone'}),
        }
        exclude = []

    id = IntegerField(widget=HiddenInput(attrs={'id': 'id'}), initial=0)

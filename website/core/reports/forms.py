from django.forms import *

from core.dashboard.choices import *
from core.employees.models import *
from core.sales.models import *
from core.company.models import *


class ReportForm(forms.Form):

    def __init__(self, bodega, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['cli'].queryset = Client.objects.filter(bodega_id=bodega)
        self.fields['provs'].queryset = Provider.objects.filter(bodega_id=bodega)
        self.fields['products'].queryset = Product.objects.filter(bodega_id=bodega)
        self.fields['productsmult'].queryset = Product.objects.filter(bodega_id=bodega)

    year = CharField(widget=TextInput(attrs={'id': 'year', 'value': datetime.now().year, 'readonly': True}))
    month = ChoiceField(choices=months_choices, widget=Select(
        attrs={'id': 'month', 'class': 'form-control selectpicker', 'data-live-search': 'true'}))
    start_date = DateField(input_formats=['%Y-%m-%d'], widget=TextInput(
        attrs={'id': 'start_date', 'value': datetime.now().strftime('%Y-%m-%d'), 'readonly': True}))
    end_date = DateField(input_formats=['%Y-%m-%d'], widget=TextInput(
        attrs={'id': 'end_date', 'value': datetime.now().strftime('%Y-%m-%d'), 'readonly': True}))
    contracts = ModelChoiceField(queryset=Contracts.objects.filter(is_active=True).order_by('-id'), widget=Select(
        attrs={'id': 'contracts', 'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}))
    provs = ModelChoiceField(queryset=Provider.objects.order_by('-name'), widget=Select(
        attrs={'id': 'provs', 'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}))
    cli = ModelChoiceField(queryset=Client.objects.order_by('-name'), widget=Select(
        attrs={'id': 'cli', 'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}))
    productsmult = ModelMultipleChoiceField(queryset=Product.objects.filter().order_by('-name'), widget=SelectMultiple(
        attrs={'id': 'products', 'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}))
    products = ModelChoiceField(queryset=Product.objects.filter().order_by('-name'), widget=Select(
        attrs={'id': 'products', 'class': 'form-control selectpicker', 'data-live-search': 'true', 'data-size': '10'}))
    type_expenses = ModelChoiceField(queryset=TypeExpense.objects.order_by('-name'), widget=Select(
        attrs={'id': 'type_expenses', 'class': 'form-control selectpicker', 'data-live-search': 'true',
               'data-size': '10'}))
    type_sales = ChoiceField(choices=sales_choices, widget=Select(
        attrs={'id': 'type_sales', 'class': 'form-control selectpicker', 'data-live-search': 'true'}))

    type = ChoiceField(choices=type_choices, widget=Select(
        attrs={'id': 'type', 'class': 'form-control selectpicker', 'data-live-search': 'true'}))

    bod = ChoiceField(choices=bodega_choices, widget=Select(
        attrs={'id': 'bod', 'class': 'form-control selectpicker', 'data-live-search': 'true'}))

from django import forms
from .models import Balance,Investment, Expense

class InvestmentForm(forms.ModelForm):

    name=forms.CharField(
    widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"Transaction name"
    })
    )

    type=forms.ModelChoiceField(
    queryset=Balance.objects.only('name'),
    )


    amount=forms.FloatField(
    required=False,
    widget=forms.TextInput(attrs={
        'class':"form-control"
    })
    )

    rate=forms.IntegerField(
    required=False,
    widget=forms.TextInput(attrs={
        'class':"form-control"
    })
    )

    total=forms.FloatField(
    required=False,
    widget=forms.TextInput(attrs={
        'class':"form-control"
    })
    )

    class Meta:
        model=Investment
        fields=['name','amount','rate','total','type','type2']

    def __init__(self, *args, **kwargs):
        super(InvestmentForm, self).__init__(*args, **kwargs)
        self.fields['type2'].widget.attrs['class'] = 'form-control'


class ExpenseForm(forms.ModelForm):
    transaction_name=forms.CharField(
    widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"Transaction name"
    })
    )


    amount=forms.IntegerField(
    widget=forms.TextInput(attrs={
        'class':"form-control"
    })
    )


    class Meta:
        model=Expense
        fields=['transaction_name','type','amount']

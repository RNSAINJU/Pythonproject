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
    queryset=Balance.objects.only('name')
    )

    amount=forms.IntegerField(
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

    total=forms.IntegerField(
    required=False,
    widget=forms.TextInput(attrs={
        'class':"form-control"
    })
    )

    class Meta:
        model=Investment
        fields=['name','amount','rate','total','type']


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

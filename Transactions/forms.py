from django import forms
from .models import Investment, Expense

class InvestmentForm(forms.ModelForm):
    name=forms.CharField(
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

    total=forms.IntegerField(
    widget=forms.TextInput(attrs={
        'class':"form-control"
    })
    )

    class Meta:
        model=Investment
        fields=['name','type','amount','total']

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

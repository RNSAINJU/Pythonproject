from django import forms


PAYMENT_CHOICES =(
    ('E','Esewa'),
    ('I','Imepay'),
    ('K','Khalti')
)

class CheckoutForm(forms.Form):
    street_address=forms.CharField(
    widget=forms.TextInput(attrs={
        'class':"form-control",'placeholder':"baneshwor, kathmandu"
    })
    )

    secondary_address=forms.CharField(required=False,
    widget=forms.TextInput(attrs={
        'class':"form-control",'placeholder':"Apartment"
    })
    )

    # save_info=forms.BooleanField(required=False)
    payment_option=forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class PaymentForm(forms.Form):
    transaction_id=forms.CharField(
    widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"Your transaction code here"
    })
    )

class CouponForm(forms.Form):
    code=forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"Promo code",
        'aria-label':"Recipent's username",
        'aria_describedby':"basic-addon2"
    }))

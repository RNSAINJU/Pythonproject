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
        'placeholder':"Your Esewa transaction code here"
    })
    )

class CouponForm(forms.Form):
    code=forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"Promo code",
        'aria-label':"Recipent's username",
        'aria_describedby':"basic-addon2"
    }))

class TopupForm(forms.Form):
    game_id=forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"In game id ",
    }))
    game_name=forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"In game name ",
    }))

class TopupLoginForm(forms.Form):
    type=forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"Facebook, Google OR Epic games",
    }))

    email=forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
    }))
    password=forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
    }))
    character_name=forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"In game name |Epic id",
    }))
    remaining_vbucks=forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"Current remaining vbucks",
    }))

# class TopupLoginForm(forms.Form):
#     email=forms.CharField(widget=forms.TextInput(attrs={
#         'class':"form-control",
#         'placeholder':"Facebook, Google OR Epic games",
#     }))

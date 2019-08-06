from django import forms
from .models import Order

PAYMENT_CHOICES =(
    ('E','Esewa'),
)

class CheckoutForm(forms.Form):
    game_details = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Type all required details mentioned above here'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    transaction_image=forms.ImageField(required=False)
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

    transaction_image=forms.ImageField()
    type=forms.CharField(
    widget=forms.TextInput(attrs={
        'type':"hidden",
    })
    )

class CouponForm(forms.Form):
    code=forms.CharField(widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"Promo code",
        'aria-label':"Recipent's username",
        'aria_describedby':"basic-addon2"
    }))


# class TopupForm(forms.Form):
#     game_id=forms.CharField(widget=forms.TextInput(attrs={
#         'class':"form-control",
#         'placeholder':"In game id ",
#     }))
#     game_name=forms.CharField(widget=forms.TextInput(attrs={
#         'class':"form-control",
#         'placeholder':"In game name ",
#     }))
#
# class TopupLoginForm(forms.Form):
#     type=forms.CharField(widget=forms.TextInput(attrs={
#         'class':"form-control",
#         'placeholder':"Facebook, Google OR Epic games",
#     }))
#
#     email=forms.CharField(widget=forms.TextInput(attrs={
#         'class':"form-control",
#     }))
#     password=forms.CharField(widget=forms.TextInput(attrs={
#         'class':"form-control",
#     }))
#     character_name=forms.CharField(widget=forms.TextInput(attrs={
#         'class':"form-control",
#         'placeholder':"In game name |Epic id",
#     }))
#     remaining_vbucks=forms.CharField(widget=forms.TextInput(attrs={
#         'class':"form-control",
#         'placeholder':"Current remaining vbucks",
#     }))

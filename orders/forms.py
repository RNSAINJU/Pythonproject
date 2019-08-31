from django import forms
from .models import Order, OrderProduct, Payment
from products.models import Product,ChildProduct

PAYMENT_CHOICES =(
    ('E','Esewa'),
)

STATUS_CHOICES=(
    ('Pending','pending'),
    ('Processing','processing'),
    ('Completed','completed'),
    )


class Orderdetailform(forms.ModelForm):
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Type all required details mentioned above here'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    status=forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect, choices=STATUS_CHOICES)

    class Meta:
        model=Order
        fields=['message','status']


class OrderForm(forms.ModelForm):
    product=forms.ModelChoiceField(
    queryset=ChildProduct.objects.only('type')
    )

    class Meta:
        model=OrderProduct
        fields=['product',]



    # game_details = forms.CharField(
    #     required=False,
    #     widget=forms.Textarea(
    #         attrs={'rows': 5, 'placeholder': 'Type all required details mentioned above here'}
    #     ),
    #     max_length=4000,
    #     help_text='The max length of the text is 4000.'
    # )
    #
    # game_image=forms.ImageField(required=False)
    # # save_info=forms.BooleanField(required=False)
    # payment_option=forms.ChoiceField(
    #     widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    #
    # transaction_id=forms.CharField(
    # widget=forms.TextInput(attrs={
    #     'class':"form-control",
    #     'placeholder':"Your Esewa transaction code here"
    # })
    # )
    #
    # transaction_image=forms.ImageField()
    # type=forms.CharField(
    # widget=forms.TextInput(attrs={
    #     'type':"hidden",
    # })
    # )
    #


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

class Payment2Form(forms.ModelForm):
    transaction_id=forms.CharField(
    widget=forms.TextInput(attrs={
        'class':"form-control",
        'placeholder':"Your Esewa transaction code here"
    })
    )

    transaction_image=forms.ImageField()
    # type=forms.CharField(
    # widget=forms.TextInput(attrs={
    #     'type':"hidden",
    # })
    # )

    class Meta:
        model=Payment
        fields=['transaction_id','transaction_image']


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

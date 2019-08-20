from django import forms
from home.models import Enquiries,News, Partner

class NewsForm(forms.ModelForm):
    title=forms.CharField(
    max_length=50,
    widget=forms.TextInput(
    attrs={'class':"form-control"}
    )
    )

    description=forms.CharField(
    max_length=2000,
    widget=forms.Textarea(
    attrs={'rows':2,'cols':30,'class':"form-control"}
    )
    )

    image=forms.ImageField()

    class Meta:
        model=News
        fields=['title','description','image']

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'form-control'

class PartnersForm(forms.ModelForm):
    profession=forms.CharField(
    max_length=50,
    widget=forms.TextInput(
    attrs={'class':"form-control"}
    )
    )

    title=forms.CharField(
    max_length=50,
    widget=forms.TextInput(
    attrs={'class':"form-control"}
    )
    )

    description=forms.CharField(
    max_length=2000,
    widget=forms.Textarea(
    attrs={'rows':2,'cols':30,'class':"form-control"}
    )
    )

    image=forms.ImageField()

    ytlink=forms.CharField(
    max_length=100,
    widget=forms.TextInput(
    attrs={'class':"form-control"}
    )
    )

    fblink=forms.CharField(
    max_length=100,
    widget=forms.TextInput(
    attrs={'class':"form-control"}
    )
    )

    instalink=forms.CharField(
    max_length=100,
    widget=forms.TextInput(
    attrs={'class':"form-control"}
    )
    )


    class Meta:
        model=Partner
        fields=['profession','title','description','image','ytlink','fblink','instalink']

    def __init__(self, *args, **kwargs):
        super(PartnersForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'form-control'

class ContactForm(forms.ModelForm):
    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
        attrs={'class':"form-control",'placeholder': 'First Name'}
        )
    )

    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
        attrs={'class':"form-control",'placeholder': 'Last Name'}
        )
    )

    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
        attrs={'class':"form-control",'placeholder': 'Email'}
        )
    )

    phoneno = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
        attrs={'class':"form-control",'placeholder': 'Phone'}
        )
    )

    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(
        attrs={'rows':2, 'cols':30,'class':"form-control",'placeholder': 'Message'}
        ),
        help_text='Write here your message!'
    )


    class Meta:
        model=Enquiries
        fields=['firstname','lastname','email','phoneno','message',]

    # def clean(self):
    #     cleaned_data = super(ContactForm, self).clean()
    #     firstname = cleaned_data.get('firstname')
    #     lastname = cleaned_data.get('lastname')
    #     email = cleaned_data.get('email')
    #     phoneno = cleaned_data.get('phoneno')
    #     message = cleaned_data.get('message')
    #     if not firstname and not email and not message:
    #         raise forms.ValidationError('You have to write something!')

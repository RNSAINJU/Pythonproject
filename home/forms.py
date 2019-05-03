from django import forms

class ContactForm(forms.Form):
    firstname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
        )
    )

    lastname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
        )
    )

    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
        )
    )

    phoneno = forms.CharField(
        max_length=10,
        widget=forms.Textarea(
        )
    )

    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(
        ),
        help_text='Write here your message!'
    )

    source = forms.CharField(       # A hidden input for internal use
        max_length=50,              # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        firstname = cleaned_data.get('firstname')
        lastname = cleaned_data.get('lastname')
        email = cleaned_data.get('email')
        phoneno = cleaned_data.get('phoneno')
        message = cleaned_data.get('message')
        if not firstname and not email and not message:
            raise forms.ValidationError('You have to write something!')

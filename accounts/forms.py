from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    username=forms.CharField(max_length=10,required=True)
    password1=forms.CharField()
    password2=forms.CharField()
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput())
    # birth_date=forms.CharField(max_length=12,required=True)

    def clean_username(self):
        username=self.cleaned_data.get('username')
        qs=User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if not "gmail.com" in email:
            raise forms.ValidationError("Your email is not gmail")
        else:
            qs=User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("Email is taken")
        return email

    def check_if_valid(self):
        email=self.cleaned_data.get('email')

        return email

    def clean(self):
        data=self.cleaned_data
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password2 !=password1:
            raise forms.ValidationError("Password must match")
        return data

    # class Meta:
    #     model=User
    #     fields=('username','email','password1','password2',)


class UserInformationUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model= User
        fields=('first_name','last_name','email',)

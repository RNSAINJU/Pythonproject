from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from .forms import SignUpForm, UserInformationUpdateForm
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
import json
from django.shortcuts import render, redirect, get_object_or_404


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # user = form.save(commit=False)
            # user.is_active = True
            # user.save()
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password1")
            email=form.cleaned_data.get("email")
            user=User.objects.create_user(username,email,password)
            user.save()

            # current_site = get_current_site(request)
            # subject = 'Activate Your Khwoppa Gift Card Account'
            # message = render_to_string('account_activation_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            #     'token': account_activation_token.make_token(user),
            # })
            # send_mail(subject, message,'help.khwoppagiftcard.store',[user.email])
            login(request, user)
            return redirect('home:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

#fix after adding mail server account_activation_sent.html

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home:home')
    else:
        return render(request, 'registration/invalid.html')

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'my_account.html'
    success_url = reverse_lazy('accounts:my_account')

    def get_object(self):
        return self.request.user

@method_decorator(login_required, name='dispatch')
class UserAdminUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'kgc/user-profile-lite.html'
    success_url = reverse_lazy('accounts:admin_account')

    def get_object(self):
        return self.request.user

class UsersView(PermissionRequiredMixin,TemplateView):
    permission_required = 'superuserstatus'
    # paginate_by = 1
    template_name="kgc/users.html"


    def get(self,request):
        user= User.objects.all()
        model_name,view=self.__class__.__name__.split('V')
        queryset={'user':user,'model_name':model_name}
        return render(request,self.template_name,queryset)


    def delete(self,request):
        id=json.loads(request.body)['id']
        expense=get_object_or_404(User, id=id)
        expense.delete()
        return redirect('accounts:kgc_users')

    # username = form.cleaned_data.get('username')
    # raw_password = form.cleaned_data.get('password1')
    # confirm_password = form.cleaned_data.get('password2')
    # user = authenticate(username=username, password=raw_password, raw_password=confirm_password)
    # login(request, user)
    # return redirect('home')

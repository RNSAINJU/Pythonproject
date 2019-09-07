from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin

''' importing views module from accounts '''
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static
from home import views as views
# from rest_framework.urlpatterns import format_suffix_patterns
# from sales import views


urlpatterns = [
    # url(r'^employees/',views.employeeList.as_view()),

    path('',include('accounts.urls',namespace='accounts')),
    path('',include('boards.urls',namespace='boards')),
    path('',include('home.urls',namespace='home')),
    path('',include('orders.urls',namespace='orders')),
    path('',include('products.urls',namespace='core')),
    path('',include('Transactions.urls',namespace='transactions')),
    # path('api/',include('sales.urls')),

    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),

    #admin site url
    url(r'^admin/', admin.site.urls),



]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

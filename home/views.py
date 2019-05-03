from django.shortcuts import get_object_or_404, redirect, render
from .models import Partner, Reviews, News, Enquiries
from products.models import Product
import datetime
from .forms import ContactForm

def home_list_view(request):
    queryset=Product.objects.filter(featured=True)
    queryset2=Partner.objects.all()
    queryset3=Reviews.objects.all()
    queryset4=News.objects.all()
    context={
            'featured_list':queryset,
            'partners_list':queryset2,
            'reviewers_list':queryset3,
            'news_list':queryset4
    }
    return render(request,"index.html",context)

def partner_list_view(request):
    queryset=Partner.objects.all()
    context={
        'partners_list':queryset
    }
    return render(request,"partners.html",context)

def about_list_view(request):
    # queryset=Reviews.objects.all()
    # context={
    #         'reviewers_list':queryset
    # }
    # return render(request,"about.html",context)
    contact = get_object_or_404(Enquiries)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # contact = form.save(commit=False)
            contact.firstname=form.cleaned_data.get('firstname'),
            contact.lastname=form.cleaned_data.get('lastname'),
            contact.email=form.cleaned_data.get('email'),
            contact.phoneno=form.cleaned_data.get('phoneno'),
            contact.message=form.cleaned_data.get('message'),
            contact.save()

        return HttpResponseRedirect(reverse('about') )
    else:
        form = ContactForm()
    context = {
        'form': form,
        'contact': contact,
    }
    return render(request, "about.html", context)

def news_list_view(request):
    queryset=News.objects.all()
    context={
            'news_list':queryset
    }
    return render(request,"news.html",context)

def contact_page(request):
    if request.method == "POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            pass
        else:
            form=ContactForm()
        return render(request, 'about.html',{'form':form})

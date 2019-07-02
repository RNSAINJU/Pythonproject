from django.shortcuts import get_object_or_404, redirect, render
from home.models import Partner, Reviews, News, Enquiries
from products.models import Product, ChildProduct
from django.views.generic import ListView, DetailView, TemplateView
import datetime
from home.forms import ContactForm
from django.utils import timezone

class HomeView(TemplateView):
    template_name='index.html'

    def get(self, request):
        form=ContactForm()
        featuredproducts=ChildProduct.objects.filter(featured=True)
        partners=Partner.objects.all()
        reviews=Reviews.objects.all()
        news=News.objects.order_by('date')

        args={
        'form':form,'featured_list':featuredproducts,
        'partners_list':partners,
        'reviewers_list':reviews,
        'news_list':news
        }
        return render(request,self.template_name,args)

    def post(self,request):
        form=ContactForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.date=timezone.now()
            post.save()
            return redirect('home')
        else:
            form=ContactForm()
        return render(request, self.template_name, {'form':form})


class PartnerView(ListView):
    model=Partner
    context_object_name = 'partners_list'
    template_name="partners.html"
    # paginate_by = 10

class AboutView(TemplateView):
    template_name='about.html'

    def get(self,request):
        form=ContactForm()
        reviews=Reviews.objects.all()

        args={
        'form':form,'reviewers_list':reviews
        }
        return render(request, self.template_name,args)

    def post(self, request):
        form= ContactForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.date=timezone.now()
            post.save()
            return redirect('about')
        else:
            form = ContactForm()
        return render(request, self.template_name, {'form': form})



def news_list_view(request):
    queryset=News.objects.all()
    context={
            'news_list':queryset
    }
    return render(request,"news.html",context)

from django.shortcuts import get_object_or_404, redirect, render
from home.models import Partner, Reviews, News, Enquiries
from products.models import Product, ChildProduct
from django.views.generic import ListView, DetailView, TemplateView
import datetime
from home.forms import NewsForm, PartnersForm,ContactForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
import json

class HomeView(TemplateView):
    template_name='index.html'
    # paginate_by=2

    def get(self, request):
        form=ContactForm()
        featuredproducts=ChildProduct.objects.filter(homefeatured=True).order_by('id')
        partners=Partner.objects.all()
        reviews=Reviews.objects.all()
        news=News.objects.order_by('date').reverse()

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
            return redirect('home:home')
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
    queryset=News.objects.order_by('date').reverse()
    context={
            'news_list':queryset
    }
    return render(request,"news.html",context)



class EnquiryView(PermissionRequiredMixin, TemplateView):
    permission_required='superuserstatus'
    template_name='kgc/enquiries.html'

    def get(self,request):
        model_name,view=self.__class__.__name__.split('V')
        enquiry=Enquiries.objects.all()
        queryset={'enquiry':enquiry,'model_name':model_name}
        return render(request,self.template_name,queryset)


    def delete(self,request):
        id=json.loads(request.body)['id']
        enquiry=get_object_or_404(Enquiries, id=id)
        enquiry.delete()
        return redirect('home:enquiries')

class NewsView(PermissionRequiredMixin, TemplateView):
    permission_required='superuserstatus'
    template_name='kgc/news.html'

    def get(self,request):
        news=News.objects.all().order_by('id')
        model_name,view=self.__class__.__name__.split('V')
        form=NewsForm()
        queryset={'form':form,'news':news,'model_name':model_name}
        return render(request,self.template_name,queryset)

    def post(self,request):
        form=NewsForm(self.request.POST, self.request.FILES or None)
        if form.is_valid():
            post=form.save(commit=False)
            post.date=timezone.now()
            post.save()
            return redirect('home:admin-news')

    def delete(self,request):
        id=json.loads(request.body)['id']
        news=get_object_or_404(News, id=id)
        news.image.delete(save=True)
        news.delete()
        return redirect('home:admin-news')

class PartnersView(PermissionRequiredMixin, TemplateView):
    permission_required='superuserstatus'
    template_name='kgc/partners.html'

    def get(self,request):
        form=PartnersForm()
        partners=Partner.objects.all().order_by('id')
        model_name,view=self.__class__.__name__.split('V')
        queryset={'form':form,'partners':partners,'model_name':model_name}
        return render(request,self.template_name,queryset)

    def post(self,request):
        form=PartnersForm(self.request.POST,self.request.FILES or None)
        if form.is_valid():
            post=form.save(commit=False)
            post.save()
            return redirect('home:admin-partners')


    def delete(self,request):
        id=json.loads(request.body)['id']
        partner=get_object_or_404(Partner, id=id)
        partner.image.delete(save=True)
        partner.delete()
        return redirect('home:admin-partners')

class ReviewsView(PermissionRequiredMixin, TemplateView):
    permission_required='superuserstatus'
    template_name='kgc/reviews.html'

    def get(self,request):
        reviews=Reviews.objects.all().order_by('id')
        model_name,view=self.__class__.__name__.split('V')
        queryset={'reviews':reviews,'model_name':model_name}
        return render(request,self.template_name,queryset)

    # def post(self,request):
    #     form=InvestmentForm(request.POST)
    #     if form.is_valid():
    #         post=form.save(commit=False)
    #         post.save()
    #         return redirect('boards:boards')

    def delete(self,request):
        id=json.loads(request.body)['id']
        review=get_object_or_404(Reviews, id=id)
        review.delete()
        return redirect('home:admin-reviews')

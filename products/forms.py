from django import forms
from products.models import Product, ChildProduct

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['title', 'short_description','description','category','image','status','purchase_method']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['short_description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['purchase_method'].widget.attrs['class'] = 'form-control'

class ChildProductForm(forms.ModelForm):
    class Meta:
        model=ChildProduct
        fields=['parent_product','type', 'cost_price','price','discount_price','status','homefeatured','productsfeatured','enabledetail']

    def __init__(self, *args, **kwargs):
        super(ChildProductForm, self).__init__(*args, **kwargs)
        self.fields['parent_product'].widget.attrs['class'] = 'form-control'
        self.fields['type'].widget.attrs['class'] = 'form-control'
        self.fields['cost_price'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['discount_price'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'

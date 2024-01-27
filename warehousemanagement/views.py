from django.shortcuts import render, redirect
from .models import Product, Category, Supplier
from django.views import View
from django import forms
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all())
    class Meta:
        model = Product
        fields = ['sku', 'name', 'location', 'quantity', 'category', 'supplier']

class AddProductView(View):
    def get(self, request):
        product_form = ProductForm()
        return render(request, 'add_product.html', {
            'product_form': product_form
        })

    def post(self, request):
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            return redirect('home')
        return render(request, 'add_product.html', {
            'product_form': product_form
        })
        
class UpdateProductView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product_form = ProductForm(instance=product)
        return render(request, 'update_product.html', {
            'product_form': product_form
        })

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('home')
        return render(request, 'update_product.html', {
            'product_form': product_form
        })

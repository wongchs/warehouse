from django.shortcuts import render, redirect
from .models import Product, Category, Supplier, Inbound, Outbound
from django.views import View
from django import forms
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.
def home(request):
    query = request.GET.get('search')
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(sku__icontains=query) |
            Q(location__icontains=query) |
            Q(category__name__icontains=query) |
            Q(supplier__name__icontains=query)
        )
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
        
class InboundForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all())
    class Meta:
        model = Inbound
        fields = ['reference', 'product', 'quantity', 'supplier', 'location', 'remarks']

class InboundView(View):
    def get(self, request):
        inbound_form = InboundForm()
        return render(request, 'inbound.html', {
            'inbound_form': inbound_form
        })

    def post(self, request):
        inbound_form = InboundForm(request.POST)
        if inbound_form.is_valid():
            inbound = inbound_form.save()
            inbound.product.quantity += inbound.quantity
            inbound.product.save()
            return redirect('home')
        return render(request, 'inbound.html', {
            'inbound_form': inbound_form
        })

class OutboundForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    class Meta:
        model = Outbound
        fields = ['reference', 'product', 'quantity', 'destination', 'remarks']

class OutboundView(View):
    def get(self, request):
        outbound_form = OutboundForm()
        return render(request, 'outbound.html', {
            'outbound_form': outbound_form
        })

    def post(self, request):
        outbound_form = OutboundForm(request.POST)
        if outbound_form.is_valid():
            outbound = outbound_form.save()
            outbound.product.quantity -= outbound.quantity
            outbound.product.save()
            return redirect('home')
        return render(request, 'outbound.html', {
            'outbound_form': outbound_form
        })

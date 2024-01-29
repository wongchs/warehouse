from django.shortcuts import render, redirect
from .models import Product, Inbound, Outbound, UserProfile
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, InboundForm, OutboundForm, UserForm, UserProfileForm, SupplierForm, CategoryForm

# Create your views here.
@login_required
def home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    outbounds = Outbound.objects.all()
    inbounds = Inbound.objects.all()
    if user_profile.user_permissions():
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
        return render(request, 'home.html', {'products': products, 'outbounds': outbounds, 'inbounds': inbounds})
    else:
        return render(request, 'operator_home.html', {'outbounds': outbounds, 'inbounds': inbounds})

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

class OutboundView(View):
    def get(self, request):
        outbound_form = OutboundForm()
        return render(request, 'outbound.html', {
            'outbound_form': outbound_form
        })

    def post(self, request):
        outbound_form = OutboundForm(request.POST)
        if outbound_form.is_valid():
            outbound = outbound_form.save(commit=False)
            if outbound.quantity > outbound.product.quantity:
                outbound_form.add_error('quantity', 'Quantity cannot exceed inventory')
                return render(request, 'outbound.html', {
                    'outbound_form': outbound_form
                })
            outbound.product.quantity -= outbound.quantity
            outbound.product.save()
            outbound.save()
            return redirect('home')
        return render(request, 'outbound.html', {
            'outbound_form': outbound_form
        })
        
@login_required
def register(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.user_permissions():
        return redirect('home')
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            UserProfile.objects.create(user=user, role=profile_form.cleaned_data['role'])
            return redirect('home')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

class AddSupplierView(View):
    def get(self, request):
        supplier_form = SupplierForm()
        return render(request, 'add_supplier.html', {
            'supplier_form': supplier_form
        })

    def post(self, request):
        supplier_form = SupplierForm(request.POST)
        if supplier_form.is_valid():
            supplier_form.save()
            return redirect('home')
        return render(request, 'add_supplier.html', {
            'supplier_form': supplier_form
        })

class AddCategoryView(View):
    def get(self, request):
        category_form = CategoryForm()
        return render(request, 'add_category.html', {
            'category_form': category_form
        })

    def post(self, request):
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('home')
        return render(request, 'add_category.html', {
            'category_form': category_form
        })

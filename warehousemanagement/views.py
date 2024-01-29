from django.shortcuts import render, redirect
from .models import Product, Category, Supplier, Inbound, Outbound, UserProfile
from django.views import View
from django import forms
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

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


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Product
        fields = ['sku', 'name', 'location', 'quantity', 'category', 'supplier']
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter SKU'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
        }

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
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Inbound
        fields = ['reference', 'product', 'quantity', 'supplier', 'location', 'remarks']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reference'}),
            'product': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter supplier'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter remarks'}),
        }

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
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Outbound
        fields = ['reference', 'product', 'quantity', 'destination', 'remarks']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reference'}),
            'product': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter destination'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter remarks'}),
        }

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
        
class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('role',)
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        
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

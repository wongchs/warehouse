from django import forms
from .models import Product, Category, Supplier, Inbound, Outbound, UserProfile
from django.contrib.auth.forms import UserCreationForm

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
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter supplier name'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
        }
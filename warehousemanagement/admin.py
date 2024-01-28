from django.contrib import admin
from .models import Category, Supplier, Product, Inbound, Outbound, UserProfile

# Register your models here.
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Inbound)
admin.site.register(Outbound)
admin.site.register(UserProfile)
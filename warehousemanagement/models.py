from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    sku = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Inbound(models.Model):
    reference = models.CharField(max_length=255, default="INBOUND")
    date_received = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, default="Storage S")
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.reference

class Outbound(models.Model):
    reference = models.CharField(max_length=255, default="OUTBOUND")
    date_shipped = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    destination = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.reference
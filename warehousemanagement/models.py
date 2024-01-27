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
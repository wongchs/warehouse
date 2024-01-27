import csv
from django.core.management.base import BaseCommand
from warehousemanagement.models import Category, Supplier, Product

class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        with open(options['csv_file'], newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                category, _ = Category.objects.get_or_create(name=row[1])
                supplier, _ = Supplier.objects.get_or_create(name=row[6])
                Product.objects.create(
                    id=row[0],
                    category=category,
                    sku=row[2],
                    name=row[3],
                    location=row[4],
                    quantity=row[5],
                    supplier=supplier,
                )

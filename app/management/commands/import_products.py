import csv
import pandas as pd
from django.core.management.base import BaseCommand
from app.models import Product  # 🔁 Make sure 'app' matches your actual app name

def parse_price(value):
    if not value or pd.isna(value):
        return 0.0
    cleaned = str(value).replace('₹', '').replace(',', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0  # fallback for unexpected format

class Command(BaseCommand):
    help = 'Import products from cleaned CSV into database'

    def handle(self, *args, **kwargs):
        with open('clean_amazon_products.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product, created = Product.objects.update_or_create(
                    title=row['title'],
                    defaults={
                        'selling_price': parse_price(row['selling_price']),
                        'discounted_price': parse_price(row['discounted_price']),
                        'description': row['description'],
                        'brand': row['brand'],
                        'category': row['category'],
                        'img_link': row['img_link'],
                        'location': row['location'],
                    }
                )
                action = "Created" if created else "Updated"
                print(f"{action}: {product.title}")

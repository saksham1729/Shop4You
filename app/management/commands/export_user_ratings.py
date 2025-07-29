from django.core.management.base import BaseCommand
from app.models import ProductRating
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = []
        ratings = ProductRating.objects.select_related('product', 'user')

        for r in ratings:
            data.append({
                'user_id': r.user_id,
                'category': r.product.category,
                'brand': r.product.brand,
                'price': r.product.discounted_price,
                'rating': r.rating
            })

        df = pd.DataFrame(data)
        df.to_csv('training_data.csv', index=False)
        self.stdout.write(self.style.SUCCESS('✅ Rating data exported.'))

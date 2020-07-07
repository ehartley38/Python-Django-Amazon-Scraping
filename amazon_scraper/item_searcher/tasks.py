'''General tasks'''

from .models import Item, Price
from .site_scraper import get_price
from datetime import datetime

'''Updates all items in database with current Amazon price'''

def update_pricing_info():
    for item in Item.objects.all():
        updated_price = get_price(item.url)
        price_to_add = Price.objects.create(item=item, price=updated_price, date=datetime.now())
        price_to_add.save()
        if item.current_price != updated_price:
            item.current_price = updated_price
    print('Database updated')

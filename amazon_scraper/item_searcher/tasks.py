'''General tasks'''

from .models import Item
from .site_scraper import get_price

'''Updates all items in database with current Amazon price'''

def update_pricing_info():
    for item in Item.objects.all():
        updated_price = get_price(item.url)
        if item.price != updated_price:
            item.price = updated_price

update_pricing_info()
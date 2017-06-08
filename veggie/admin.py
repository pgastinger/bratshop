from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Offer, Item, Order, OrderDate, OrderItem

admin.site.register(Offer)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderDate)
admin.site.register(OrderItem)

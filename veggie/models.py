from django.db import models


# Create your models here.
class Offer(models.Model):
    offer_text = models.CharField(max_length=200)
    offer_description = models.TextField()
    change_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.offer_text


class Item(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    item_description = models.CharField(max_length=200)
    item_price = models.FloatField()
    item_unitsize = models.CharField(max_length=15, default="EUR/kg")
    item_status = models.BooleanField(default=True)
    item_image = models.ImageField(blank=True)
    change_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "item: %s | offer: %s | price: %s %s" % (
        self.item_description, self.offer, self.item_price, self.item_unitsize)


class OrderDate(models.Model):
    offer_id = models.ForeignKey(Offer)
    order_date = models.DateField()
    status = models.BooleanField(default=True)
    change_date = models.DateTimeField(auto_now=True)
    available_until = models.DateTimeField()

    def __str__(self):
        return "order_date: %s | offer: %s" % (str(self.order_date), self.offer_id)


class Order(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    order_date = models.ForeignKey(OrderDate)
    order_name = models.CharField(max_length=20)
    order_surname = models.CharField(max_length=20)
    order_phone = models.CharField(max_length=20)
    order_email = models.EmailField()
    order_confirmed = models.BooleanField(default=False)
    order_confirm_hash = models.CharField(max_length=64)
    add_date = models.DateTimeField()
    confirm_date = models.DateTimeField(null=True)
    cancel_date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.order_date)


class OrderItem(models.Model):
    oi = models.ForeignKey(Order)
    item = models.ForeignKey(Item)
    amount = models.IntegerField()

    def __str__(self):
        return "item: %s | amount: %s" % (self.item, self.amount)

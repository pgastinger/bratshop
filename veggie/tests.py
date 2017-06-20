import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Offer, OrderDate, Order, OrderItem, Item

class ModelTests(TestCase):

    def setUp(self):
        o1 = Offer.objects.create(offer_text="My Test Offer #1", offer_description="This is a test description for a Test Offer #1")
        Item.objects.create(offer=o1, item_description="item01#01", item_price=1.1, item_unitsize="Euro/kg")
        Item.objects.create(offer=o1, item_description="item01#02", item_price=2.2, item_unitsize="Euro/kg")
        o2 = Offer.objects.create(offer_text="My Test Offer #2", offer_description="This is a test description for a Test Offer #2", status=False)
        Item.objects.create(offer=o2, item_description="item02#01", item_price=3.3, item_unitsize="Euro/kg")
        Item.objects.create(offer=o2, item_description="item02#02", item_price=4.4, item_unitsize="Euro/kg")
        od1 = OrderDate.objects.create(offer_id=o1, order_date=datetime.date.today()+datetime.timedelta(days=1), available_until=timezone.now())
        od2 = OrderDate.objects.create(offer_id=o1, order_date=datetime.date.today()+datetime.timedelta(days=8), available_until=timezone.now()+timezone.timedelta(days=7))

    def test_01_Offer_objects(self):
        self.assertEqual(len(Offer.objects.all()), 2)

    def test_02_Offer_objects(self):
        self.assertEqual(len(Offer.objects.filter(status=True)), 1)

    def test_03_Offer_objects(self):
        self.assertEqual(Offer.objects.first().offer_text, "My Test Offer #1")

    def test_04_Item_objects(self):
        self.assertEqual(len(Item.objects.all()), 4)

    def test_05_Item_objects(self):
        self.assertEqual(Item.objects.first().item_description, "item01#01")

    def test_06_Item_objects(self):
        offer = Offer.objects.filter(status=True)[0]
        items = offer.item_set.all()
        self.assertEqual(len(items), 2)

    def test_07_OrderDate_objects(self):
        self.assertEqual(len(OrderDate.objects.all()), 2)
        
    def test_08_OrderDate_objects(self):
        offer = Offer.objects.filter(status=True)[0]
        order_dates = offer.orderdate_set.all()
        self.assertEqual(len(order_dates), 2)

    def test_09_OrderDate_objects(self):
        offer = Offer.objects.filter(status=True)[0]
        order_dates = offer.orderdate_set.filter(available_until__gte=timezone.now())
        self.assertEqual(len(order_dates), 1)


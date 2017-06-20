import datetime

from django.test import TestCase
from django.utils import timezone
from django.test import Client

from .models import Offer, OrderDate, Order, OrderItem, Item


def setUP():
    # available items and dates
    o1 = Offer.objects.create(offer_text="My Test Offer #1",
                              offer_description="This is a test description for a Test Offer #1")
    it1 = Item.objects.create(offer=o1, item_description="item01#01", item_price=1.1, item_unitsize="Euro/kg")
    it2 = Item.objects.create(offer=o1, item_description="item01#02", item_price=2.2, item_unitsize="Euro/kg")
    o2 = Offer.objects.create(offer_text="My Test Offer #2",
                              offer_description="This is a test description for a Test Offer #2", status=False)
    it3 = Item.objects.create(offer=o2, item_description="item02#01", item_price=3.3, item_unitsize="Euro/kg")
    it4 = Item.objects.create(offer=o2, item_description="item02#02", item_price=4.4, item_unitsize="Euro/kg")
    od1 = OrderDate.objects.create(offer_id=o1, order_date=datetime.date.today() + datetime.timedelta(days=1),
                                   available_until=timezone.now())
    od2 = OrderDate.objects.create(offer_id=o1, order_date=datetime.date.today() + datetime.timedelta(days=8),
                                   available_until=timezone.now() + timezone.timedelta(days=7))

    order1 = Order.objects.create(offer=o1, order_date=od2, order_name="Peter", order_surname="Gastinger",
                                  order_phone="0043500800", order_email="peter.gastinger@mailinator.com",
                                  add_date=timezone.now())
    OrderItem.objects.create(oi=order1, item=it1, amount=10)
    OrderItem.objects.create(oi=order1, item=it2, amount=20)


class ModelTests(TestCase):
    def setUp(self):
        setUP()

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

    def test_10_Order_objects(self):
        order = Order.objects.filter(order_confirmed=True).all()
        self.assertEqual(len(order), 0)

    def test_11_Order_objects(self):
        order = Order.objects.all()
        self.assertEqual(len(order), 1)

    def test_12_Order_objects(self):
        order = Order.objects.first()
        ois = order.orderitem_set.all()
        self.assertEqual(len(ois), 2)

    def test_13_Order_objects(self):
        order = Order.objects.first()
        ois = order.orderitem_set.all()
        total_amount = sum([x.amount * x.item.item_price for x in ois])
        self.assertEqual(total_amount, 55.0)


class ViewTests(TestCase):
    def setUp(self):
        setUP()
        self.client = Client()

    def test_01_Index_Single(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)

    def test_02_Index_Single(self):
        response = self.client.get('/veggie/1')
        self.assertEquals(response.status_code, 200)
        self.assertIn("My Test Offer #1", str(response.content))

    def test_03_Index_Multiple(self):
        o = Offer.objects.filter(status=False).first()
        o.status = True
        o.save()
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertIn("My Test Offer #1", str(response.content)) and self.assertIn("My Test Offer #2",
                                                                                   str(response.content))

    def test_04_OutOfSale(self):
        o = Offer.objects.filter(status=True).first()
        o.status = False
        o.save()
        response = self.client.get('/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIn("Out Of Sale", str(response.content))

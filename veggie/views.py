from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import ugettext as _
import mistune

from .models import Offer, Item, OrderDate, Order, OrderItem
from .forms import OrderForm

import logging

def index(request):
    available_offers = Offer.objects.filter(status=True)
    if len(available_offers) == 1:
        return redirect('offerDetail',available_offers[0].id)
    context = {'available_offers': available_offers}
    return render(request, 'veggie/index.html', context)


def offerDetail(request, id):
    queryset = Offer.objects.filter(status=True)
    offer = get_object_or_404(queryset, pk=id)
    items = offer.item_set.filter(item_status=True) 
    now = timezone.now()
    orderdates = offer.orderdate_set.filter(status=True).filter(available_until__gte=now)
    if request.method == 'POST':
        orderForm = OrderForm(orderdates, request.POST)
        if orderForm.is_valid():
            confirmhash = get_random_string(length=64)
            edithash = get_random_string(length=64)
            neworder = Order(order_name=orderForm.cleaned_data.get("data_firstname"),order_date_id=orderForm.cleaned_data.get("data_orderdate"),
                offer_id=id, order_surname=orderForm.cleaned_data.get("data_surname"), order_phone=orderForm.cleaned_data.get("data_phone"), order_email=orderForm.cleaned_data.get("data_email"), order_confirm_hash=confirmhash, order_edit_hash=edithash)
            neworder.save()
            for shopitem in orderForm.cleaned_data:
                if shopitem.startswith("shopitem_"):
                    if orderForm.cleaned_data[shopitem]:
                        itemid = shopitem.replace("shopitem_","")
                        item = offer.item_set.filter(item_status=True).filter(pk=itemid)[0]
                        oi = OrderItem(oi=neworder, item=item, amount=orderForm.cleaned_data[shopitem])
                        oi.save()
            messages.add_message(request, messages.INFO, _('Order added successfully, you have to confirm the order with the sent confirmation link via email'))
            return redirect('index')
    else:
        description = mistune.markdown(offer.offer_description)
        orderForm = OrderForm(orderdates)
        context = {'offerDetail': offer, 'offerItems': items, 'form': orderForm, 'description': description}
        return render(request, 'veggie/detail.html', context)


def order(request):
    orders = OrderDate.objects.filter(status=True)
    context = {'orders': orders}
    return render(request, 'veggie/order.html', context)


def orderDetails(request, orderdateid):
    queryset = OrderDate.objects.filter(status=True)
    orderdate = get_object_or_404(queryset, pk=orderdateid)
    orders = orderdate.order_set.filter(order_confirmed=True)
    if len(orders) > 0:
        orderitems = orders[0].orderitem_set.all()
#        logging.error(orders)
        context = {'orders': orders, 'orderitems': orderitems}
        return render(request, 'veggie/orderdetail.html', context)
    else:
        messages.add_message(request, messages.INFO, _('No orders found' ))
        return redirect('order')



def confirmOrder(request, confirmhash):
    offer = get_object_or_404(Order, order_confirm_hash=confirmhash)
    if offer.order_confirmed:
        messages.add_message(request, messages.INFO, _('Order already confirmed'))
    else:
        offer.order_confirmed = True
        offer.save()
        messages.add_message(request, messages.SUCCESS, _('Order successfully confirmed'))
    return render(request, 'veggie/confirm.html', {})

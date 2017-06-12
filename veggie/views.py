from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.http import JsonResponse,HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMessage
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
            body = '<html>\n<body>\n<a href="localhost:8000/veggie/confirm/%s">Confirm order</a>\n\n'%(confirmhash)
            body += "<table>\n<thead>\n"
            body += "<tr><th>Description</th><th>Amount</th><th>Price</th><th>Sum</th></tr>\n"
            body += "</thead>\n<tbody>\n"
            sum = 0
            for shopitem in orderForm.cleaned_data:
                if shopitem.startswith("shopitem_"):
                    if orderForm.cleaned_data[shopitem]:
                        itemid = shopitem.replace("shopitem_","")
                        item = offer.item_set.filter(item_status=True).filter(pk=itemid)[0]
                        if orderForm.cleaned_data[shopitem] > 0:
                            oi = OrderItem(oi=neworder, item=item, amount=orderForm.cleaned_data[shopitem])
                            oi.save()
                            sum += oi.item.item_price*oi.amount
                            body += "<tr><td>" + str(oi.item.item_description) +"</td><td>"+ str(oi.amount)+"</td><td>"+str(oi.item.item_price)+ " " + str(oi.item.item_unitsize)+"</td><td>"+str(oi.item.item_price*oi.amount)+"</td></tr>\n"
            
            body += '<tr><td colspan="3">Sum</td><td>'+str(sum)+' Euro</td></tr>\n'
            body += "</tbody>\n</table>\n\n"
            body += "<b>If this order was not submitted by you or you reconsidered, just ignore this mail</b>"
            body += "</body>\n</html>"
            messages.add_message(request, messages.INFO, _('Order added successfully, you have to confirm the order with the sent confirmation link via email'))

            email = EmailMessage(
                _("Order -%(description)s- for -%(date)s-, please confirm order")%{"date": neworder.order_date.order_date, 'description':neworder.offer.offer_text},
                str(body),
                'bratshop@do-not-reply.com',
                [orderForm.cleaned_data.get("data_email")],
                reply_to=['peter.gastinger@gmail.com'],
            )
            email.content_subtype = "html"
            email.send()
            return redirect('index')
        else:
            description = mistune.markdown(offer.offer_description)
            context = {'offerDetail': offer, 'offerItems': items, 'form': orderForm, 'description': description}
            return render(request, 'veggie/detail.html', context)
    else:
        description = mistune.markdown(offer.offer_description)
        orderForm = OrderForm(orderdates)
        context = {'offerDetail': offer, 'offerItems': items, 'form': orderForm, 'description': description}
        return render(request, 'veggie/detail.html', context)


def order(request):
    orders = OrderDate.objects.filter(status=True)
    context = {'orders': orders}
    return render(request, 'veggie/order.html', context)


def _get_order_for_orderdateid(orderdateid):
    queryset = OrderDate.objects.filter(status=True)
    orderdate = get_object_or_404(queryset, pk=orderdateid)
    orders = orderdate.order_set.all()
    orders_list = list()

    if len(orders) > 0:
        for item in orders:
            ordersum = 0
            ois = item.orderitem_set.all()
            orderitems = list()
            for oi in ois:
                ordersum += oi.amount*oi.item.item_price
                orderitems.append(dict(description=oi.item.item_description, amount=oi.amount, price=oi.item.item_price, unitsize=oi.item.item_unitsize, itemsum=oi.item.item_price*oi.amount))
            order_dict = dict(id=item.id, name=item.order_name, surname=item.order_surname, phone=item.order_phone, email=item.order_email, status=item.order_confirmed, confirmhash=item.order_confirm_hash, ordersum=ordersum, orderitems=orderitems, orderdate=orderdate.order_date)
            orders_list.append(order_dict)
    return orders_list


def orderDetails(request, orderdateid):
    orders_list = _get_order_for_orderdateid(orderdateid)
    if len(orders_list) > 0:
        context = {'orders': orders_list, 'orderdateid': orderdateid}
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
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('index')


def downloadxls(request, orderdateid):
    queryset = OrderDate.objects.filter(status=True)
    orderdate = get_object_or_404(queryset, pk=orderdateid)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bestellung_%s.xlsx"'%(orderdate.order_date)

    import xlsxwriter
    from io import BytesIO

    buffer = BytesIO()

    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    format_center_bold = workbook.add_format()
    format_center_bold.set_align('center')
    format_center_bold.set_bold()

    format_wrap = workbook.add_format()
    format_wrap.set_text_wrap()
    worksheet.write(0, 0, _("Name"), format_center_bold)
    worksheet.write(0, 1, _("Telephone"), format_center_bold)
    worksheet.write(0, 2, _("Email"), format_center_bold)
    worksheet.write(0, 3, _("Sum"), format_center_bold)
    worksheet.write(0, 4, _("Items"), format_center_bold)
    worksheet.write(0, 5, _("Done"), format_center_bold)
    row = 1
    col_length = dict(col0=10, col1=10, col2=20, col4=30)

    orders_list = _get_order_for_orderdateid(orderdateid)
    for item in orders_list:
        if not item["status"]:
            continue
        worksheet.write(row, 0, "%s, %s" % (item["surname"], item["name"]))
        if len("%s, %s" % (item["surname"], item["name"])) > col_length["col0"]:
            col_length["col0"] = len("%s, %s" % (item["surname"], item["name"]))
        worksheet.write(row, 1, item["phone"])
        if len(item["phone"]) > col_length["col1"]:
            col_length["col1"] = len(item["phone"])
        worksheet.write(row, 2, item["email"])
        if len(item["email"]) > col_length["col2"]:
            col_length["col2"] = len(item["email"])
        worksheet.write(row, 3, item["ordersum"])
        worksheet.write(row, 5, "")

        items = ""
        for oi in item["orderitems"]:
            line = "%s-%s%s-%s-%s EUR\n"%(oi["description"],oi["price"],oi["unitsize"],oi["amount"],oi["itemsum"])
            if len(line) > col_length["col4"]:
                col_length["col4"] = len(line)
            items+= line
        worksheet.write(row, 4, items.rstrip(), format_wrap)
        row += 1

    worksheet.set_column(0,0, col_length["col0"]+2)
    worksheet.set_column(1,1, col_length["col1"]+2)
    worksheet.set_column(2,2, col_length["col2"]+2)
    worksheet.set_column(4,4, col_length["col4"]+2)

    worksheet.autofilter(0,0,0,4)
    workbook.close()
    result = buffer.getvalue()
    buffer.close()
    response.write(result)
    return response 

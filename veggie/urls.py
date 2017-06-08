from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^([0-9]+)$', views.offerDetail, name='offerDetail'),
    url(r'^orders/$', views.order, name='order'),
    url(r'^orders/([0-9]+)$', views.orderDetails, name='orderDetails'),
    url(r'^confirm/$', views.index, name='index'),
    url(r'^confirm/([a-zA-Z0-9]+)$', views.confirmOrder, name='confirmOrder'),
    url(r'^downloadxls/$', views.order, name='order'),
    url(r'^downloadxls/([0-9]+)$', views.downloadxls, name='downloadxls'),
]

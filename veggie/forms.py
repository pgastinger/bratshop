from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator, RegexValidator
from captcha.fields import ReCaptchaField

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import logging

class OrderForm(forms.Form):
    data_firstname = forms.CharField(label=_('First Name'), max_length=20, validators=[RegexValidator(regex="^[a-zA-Z_-]+$")])
    data_surname = forms.CharField(label=_('Surname'), max_length=20, validators=[RegexValidator(regex="^[a-zA-Z_-]+$")])
    data_email = forms.EmailField(label=_('Email'), validators=[EmailValidator()])
    data_phone = forms.CharField(label=_('Phone'), max_length=20, validators=[RegexValidator(regex="^[0-9/ _-]+$")])
    if not settings.DEBUG:
        antispam = ReCaptchaField()

    def __init__(self, orderdates, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields["data_orderdate"] = forms.ChoiceField(label=_('Date'), choices = [(x.id,_("%(orderdate)s (available until %(availabledate)s)") % { 'orderdate': x.order_date, 'availabledate': x.available_until}) for x in orderdates])
        #self.fields["data_orderdate"] = forms.ChoiceField(label=_('Date'), choices = [(x.id,_("%(orderdate)s (available until %(availabledate)s)") % { 'orderdate': x.order_date, 'availabledate': x.available_until}) for x in orderdates], validators=[MinValueValidator(0)])
        shopitems = orderdates[0].offer_id.item_set.all()
        self.images = dict()
        for si in shopitems:
            key = "shopitem_%d"%(si.id)
            descr = '%s (%s %s)'%(si.item_description, si.item_price, si.item_unitsize)
            self.fields[key] = forms.IntegerField(label=descr, required=False, initial=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
            self.fields[key].url = si.item_image

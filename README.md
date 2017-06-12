# bratshop

> This code is not ready for a productive environment! This can be considered as a prototype/proof of concept.

Usually, during spring, we can order certain vegetables (e.g. asparagus) for specific dates through a word based order form, which we fill out and send to the organizer via email. This organizer extracts each order from each email, generates an Excel sheet and sends all the orders to the local farmer. This farmer will deliver all the ordered items to a central location, where everyone picks up their order and pays with cash. The organizational part is pretty cumbersome and there are probably dozens better ways to handle this. That's why this really simple/basic bratshop (BRAT actually means _Betriebsrat_, the german word for workers council) was originally built using Django. 

The link to a pretty basic order form will be distributed (e.g. Intranet article, Email) to multiple potential users. Interested users must provide their names, email-address and phone-number, as well as a specific order date. They can then choose an amount of different kind of items and send their order. After that, they will get a confirmation email, in which they will find a link to confirm their orders. 
The organizer can download all the confirmend orders as Excel file, send it to the local farmer and handle the pickup. That's it.

## order form

No registration necessary!

![order_form_01](https://user-images.githubusercontent.com/3997488/27031418-73a3bfee-4f70-11e7-8c8d-a57c8db28d41.png)

## Confirmation email

```
Content-Type: text/html; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit
Subject:
 =?utf-8?q?Bestellung_-Frischer_Spargel_aus_dem_Marchfeld-_f=C3=BCr_-2017-06-?=
  =?utf-8?q?14-=2C_bitte_Bestellung_best=C3=A4tigen?=
  From: bratshop@do-not-reply.com
  To: erika.musterfrau@doesnotexist.com
  Reply-To: peter.gastinger@gmail.com
  Date: Mon, 12 Jun 2017 11:50:50 -0000
  Message-ID: <20170612115050.32669.67041@wos34526.wien.rbgat.net>

  <html>
  <body>
  <a href="localhost:8000/veggie/confirm/duIjTRlCGQ8Pn130GOyR8TYYuMSGF299XINnDoMD5CD8mdyscOotbqvY6K8P0Rrl">Confirm order</a>

  <table>
  <thead>
  <tr><th>Description</th><th>Amount</th><th>Price</th><th>Sum</th></tr>
  </thead>
  <tbody>
  <tr><td>Spargel Klasse II</td><td>2</td><td>5.0 EUR/kg</td><td>10.0</td></tr>
  <tr><td>Grün Solo</td><td>1</td><td>10.0 EUR/kg</td><td>10.0</td></tr>
  <tr><td>Grün mittel</td><td>1</td><td>8.0 EUR/kg</td><td>8.0</td></tr>
  <tr><td colspan="3">Sum</td><td>28.0 Euro</td></tr>
  </tbody>
  </table>

  <b>If this order was not submitted by you or you reconsidered, just ignore this mail</b></body>
  </html>
  -------------------------------------------------------------------------------
```

## Download orders

* Order overview
![order_users_01](https://user-images.githubusercontent.com/3997488/27032704-873c660e-4f76-11e7-9323-b7c91de297a6.png)

* Excel order list
![order_users_02](https://user-images.githubusercontent.com/3997488/27032703-85ea6ea4-4f76-11e7-8b62-b88aa98b521d.png)

## management 

Order management (what is available, at which dates with which costs) is handled using the Django admin interface.


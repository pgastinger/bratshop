# Bratshop

> This code is not ready for a productive environment! This can be considered as a prototype/proof of concept.

Usually, during spring, we (employees) can order certain vegetables (e.g. asparagus)
for specific dates through a Word based order form, which we fill out and send to 
the organizer via email. The organizer extracts each order from each email, 
generates an Excel sheet and sends all the orders to the local farmer. This farmer 
will deliver all the ordered items to a central location, where everyone picks up 
their order and pays with cash. The organizational part is pretty cumbersome and 
there are probably dozens better ways to handle this. That's why this really 
simple/basic bratshop (BRAT actually means _Betriebsrat_, the german word for 
workers council) was originally built using Django. 

The link to a pretty basic order form will be distributed (e.g. Intranet article, 
Email) to multiple potential users. Interested users must provide their names, 
email-address and phone-number, as well as a specific order date. They can then 
choose an amount of different kind of items and send their order. After that, they 
will get a confirmation email, in which they will find a link to confirm their 
orders. 
The organizer can download all the confirmed orders as Excel file, send it to 
the local farmer and handle the pickup. That's it.

## Order form

No registration necessary!

![order_form_01](https://user-images.githubusercontent.com/3997488/27031418-73a3bfee-4f70-11e7-8c8d-a57c8db28d41.png)

## Confirmation email

```
Content-Type: text/html; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit
Subject: 
 =?utf-8?q?Bestellung_-Frischer_Spargel_aus_dem_Marchfeld-_f=C3=BCr_-2017-06-?=
 =?utf-8?q?28-=2C_bitte_Bestellung_best=C3=A4tigen?=
From: bratshop@do-not-reply.com
To: peter.gastinger@gmail.com
Reply-To: peter.gastinger@gmail.com
Date: Sat, 17 Jun 2017 14:18:44 -0000
Message-ID: <20170617141844.6064.29602@peda-desktop>


<html>
<head>
    <title>Bestellung bestätigen</title>
</head>
<body>

<b>Falls diese Bestellung nicht von Ihnen in Auftrag gegeben wurde, bitte diese E-Mail einfach ignorieren.</b>

<br/>
<br/>

<a href="http:localhost:8000/veggie/confirm/bIehUuq7pPS0S5wZ48quNsGK1wqNNboEghQKqRjA0o3d5SmFpnoPGmR2AzPgCia0">Bestellung bestätigen</a>

<br/>
<br/>

<table border="1">
    <thead>
        <tr>
            <th>Beschreibung</th>
            <th>Menge</th>
            <th>Preis</th>
            <th>Sum</th>
        </tr>
    </thead>
    <tbody>
    
        <tr>
            <td>Spargel Klasse II</td>
            <td>2</td>
            <td>5,0 EUR/kg</td>
            <td>10,0 Euro</td>
        </tr>
    
        <tr>
            <td colspan="3">Sum</td>
            <td>10,0 Euro</td>
        </tr>
    </tbody>
</table>

<br/>

<b>Falls diese Bestellung nicht von Ihnen in Auftrag gegeben wurde, bitte diese E-Mail einfach ignorieren.</b>

</body>
</html>

-------------------------------------------------------------------------------
```

## Download orders

* Order overview
![order_users_01](https://user-images.githubusercontent.com/3997488/27032704-873c660e-4f76-11e7-9323-b7c91de297a6.png)

* Excel order list
![order_users_02](https://user-images.githubusercontent.com/3997488/27032703-85ea6ea4-4f76-11e7-8b62-b88aa98b521d.png)

## Management 

Order management (what is available, at which dates with which costs) is handled using the Django admin interface.

## TODO
 
To make this interface more stable, a lot of things are still missing:

- Source Code Improvements
- Tests
- More features
- Deployment procedure

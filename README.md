# bratshop

> This code is not ready for a productive environment! This can be considered as a prototype/proof of concept.

Usually, during spring, we can order certain vegetables (e.g. asparagus) for specific dates through a word based order form, which we fill out and send to the organizer via email. This organizer extracts each order from each email, generates an Excel sheet and sends all the orders to the local farmer. This farmer will deliver all the ordered items to a central location, where everyone picks up their order and pays with cash. The organizational part is pretty cumbersome and there are probably dozens better ways to handle this. That's why this really simple/basic bratshop (BRAT actually means _Betriebsrat_, the german word for workers council) was originally built using Django. 

The link to a pretty basic order form will be distributed (e.g. Intranet article, Email) to multiple potential users. Interested users must provide their names, email-address and phone-number, as well as a specific order date. They can then choose an amount of different kind of items and send their order. After that, they will get a confirmation email, in which they will find a link to confirm their orders. 
The organizer can download all the confirmend orders as Excel file, send it to the local farmer and handle the pickup. That's it.

## order form

No registration necessary!

![order_form_01](https://user-images.githubusercontent.com/3997488/27031418-73a3bfee-4f70-11e7-8c8d-a57c8db28d41.png)


## management 

Order management (what is available, at which dates with which costs) is handled using the Django admin interface.


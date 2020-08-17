from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product, Product_Subscription

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

         # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                order_exists = True
                print('--ORDER EXISTS')
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                print('Order DOES NOT EXIST - creating...')
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                print('Order is created here, now for OrderLine Item...')
                for item_id, item_data in json.loads(basket).items():
                    product = Product.objects.get(id=item_id)
                    product_subscription = Product_Subscription.objects.filter(product=item_id)

                    print('-INSIDE the orderlineitemfor loop')
                    print('basket[item_id]', basket)
                    if 'item_subscription' in basket[item_id]:
                        print('We are at ITEM SUBSCRIPTION')
                        for subs_size, quantity in item_data['item_subscription'].items():
                            prod_sub = product_subscription.filter(subscription_type=subs_size)
                            selected_product_subs = get_object_or_404(Product_Subscription, pk=prod_sub[0].id)
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                #product_subscription=selected_product_subs,
                            )

                            print('order', order)
                            print('product', product)

                            order_line_item.save()
                    elif 'items_by_size' in basket[item_id]:
                        print('We are at ITEM SIZE')
                        for subs_size, quantity in item_data['items_by_size'].items():
                            prod_sub = product_subscription.filter(size=subs_size)
                            for p in prod_sub:
                                prod_size = p.size
                            sel_prod_size = get_object_or_404(Sizes, code=prod_size)
                            selected_product_subs = get_object_or_404(Product_Subscription, pk=prod_sub[0].id)
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                #product_subscription=selected_product_subs,
                                #product_size=sel_prod_size,
                            )
                            print('order', order)
                            print('product', product)
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                    print('--Failed creating order, error', e)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)                    
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
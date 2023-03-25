from django.shortcuts import render,redirect
import json
import stripe
from django.conf import settings
from .models import Product
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

stripe.api_key=settings.STRIPE_SECRET_KEY


def checkoutsessioncreate(request):
    product=Product.objects.first()
    # price = stripe.Price.create(
    # unit_amount=product.price * 100,  # Stripe prices are in cents
    # currency='usd',
    # product_data={
    #     'name': product.title,
    # },
    # )
	# stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':    
        checkout_session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = [
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': (product.price*100),
                        'product_data': {
                            'name': product.title,
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode = 'payment',
            # customer_creation = 'always',
            
            success_url = settings.REDIRECT_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = settings.REDIRECT_DOMAIN + '/cancel',
        )
        print(checkout_session.id)
        print(checkout_session.url)
        return redirect(checkout_session.url, code=303)
    return render(request, 'checkout/checkout.html',{'product':product})

def checkoutsessioncreateProduct(request,pk,quantity):
    product=Product.objects.get(id=pk)
    # price = stripe.Price.create(
    # unit_amount=product.price * 100,  # Stripe prices are in cents
    # currency='usd',
    # product_data={
    #     'name': product.title,
    # },
    # )
	# stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':    
        checkout_session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = [
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': (product.price*100),
                        'product_data': {
                            'name': product.title,
                        },
                    },
                    'quantity': quantity,
                },
            ],
            mode = 'payment',
            # customer_creation = 'always',
            
            success_url = settings.REDIRECT_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = settings.REDIRECT_DOMAIN + '/cancel',
        )
        print(checkout_session.id)
        print(checkout_session.url)
        return redirect(checkout_session.url, code=303)
    return render(request, 'checkout/checkout.html',{'product':product})

def success(request):
        stripe.api_key=settings.STRIPE_SECRET_KEY
        checkout_session_id = request.GET.get('session_id', None)
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer_id = session.customer
        if customer_id is not None:
            customer = stripe.Customer.retrieve(customer_id)
        else:
            customer = None
        return render(request,'checkout/success.html',{'checkout_session_id':checkout_session_id})

def cancel(request):
      return render(request,'checkout/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
    # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
        event['data']['object']['id'],
        expand=['line_items'],
        )
        print(session)
        # line_items = session.line_items
        # # Fulfill the purchase...
        # fulfill_order(line_items)

        # Passed signature verification
        return HttpResponse(status=200)

# def fulfill_order(line_items):
#   print("Fulfilling order")
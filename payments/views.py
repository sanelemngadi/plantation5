from django.shortcuts import render
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import uuid
# Create your views here.
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

def payment_view(request):
    host = request.get_host()

    http = "https://"

    if settings.DEBUG:
        http = "http://"
    
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "20.0",
        "invoice": str(uuid.uuid4()),
        "currency_code": "USD",
        "item_name": "book",
        "notify_url": f'https://{host}{reverse("paypal-ipn")}',
        "return_url": f'{http}{host}{reverse("successful")}',
        "cancel_return": f'{http}{host}{reverse("cancelled")}',
    }

    #request.build_absolute_uri(reverse("paypal-ipn"))
    #"return_url": request.build_absolute_uri(reverse("successful"))
    #request.build_absolute_uri(reverse("cancelled"))

    form = PayPalPaymentsForm(initial = paypal_dict)

    context = { "form": form, "value": request.GET }
    return render(request, "payment.html", context)


def payment_successful_view(request):
    return render(request, "success.html")

def payment_cancelled_view(request):
    return render(request, "cancelled.html")

def razorpay_view(request):
    return render()
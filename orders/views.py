from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.http import HttpResponse, Http404
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from xhtml2pdf import pisa
from django.template.loader import get_template

from orders.models import PlantationOrderModel
from orders.forms import PlantationOrderForm
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import uuid

from products.models import PlantationProduct

from delivery.forms import PlantationDeliveryForm
from delivery.models import PlantationDelivery

import random

def generate_otp(n: int):
    otp = ""
    for _ in range(5):
        otp += str(random.randint(0, 9))
    
    return otp

# import weasyprint

# from payfast.forms import PayFastForm

# Create your views here.
@login_required(login_url='/users/login/')
def order_list_view(request):
    orders = PlantationOrderModel.objects.all().order_by("-date")
    return render(request, "orders.html", { "orders": orders })

def page_invoice_view(request, pk):
    try:
        order = get_object_or_404(PlantationOrderModel, pk=pk)
    except Http404:
        return render(request, "problem.html")
    return render(request, "invoice-home.html", { "order": order })


def pay_for_order_view(request, order):
    try:
        order = get_object_or_404(PlantationOrderModel, pk = order)

        host = request.get_host()

        http = "https://"

        if settings.DEBUG:
            http = "http://"
        
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": order.total_grand_price,
            "invoice": str(uuid.uuid4()),
            "currency_code": "USD",
            "item_name": "Plantation cart",
            "notify_url": f'https://{host}{reverse("paypal-ipn")}',
            "return_url": f'{http}{host}{reverse("pay-order-success", kwargs={"order_id": order.pk})}',
            "cancel_return": f'{http}{host}{reverse("cancelled")}',
        }

        form = PayPalPaymentsForm(initial = paypal_dict)
        delivery_form = PlantationDeliveryForm()

        if request.method == "POST":
            delivery_form = PlantationDeliveryForm(request.POST)
            has_delivery = PlantationDelivery.objects.filter(order_number = order.order_number()).exists()

            if delivery_form.is_valid() and not has_delivery:
                delivery: PlantationDelivery = delivery_form.save(commit=False)
                order.has_driver = True
                order.save()

                delivery.address = order.address
                delivery.client = order.user
                delivery.order = order

                if order.payment_option == "C":
                    delivery.pay_with_cash = True
                delivery.otp = generate_otp(5)

                delivery.order_number = order.order_number()

                delivery.save()

                return redirect("orders")

    except Http404:
        return render(request, "problem.html")
     
    return render(request, "payment.html", { "order": order, "form": form, "delivery_form": delivery_form })



def order_paid_success_view(request, order_id):
    try:
        order = get_object_or_404(PlantationOrderModel, pk = order_id)
        order.paid = True

        for item in order.items.all():
            product = get_object_or_404(PlantationProduct, pk = item.product_id)
            if not product:
                continue

            product.buy(item.quantity)

        order.save()
    except Http404:
        return render(request, "problem.html")
    
    return redirect("pay-for-order", order.pk)
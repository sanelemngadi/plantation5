from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.conf import settings
from django.urls import reverse
import uuid

from cart.models import PlantationCartModel, PlantationProductDetails
from products.models import PlantationProduct
from orders.forms import PlantationAddressForm, PlantationOrderForm
from orders.models import PlantationOrderModel, PlantationOrderItemModel

from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
@login_required(login_url="/users/login/")
def cart_list_view(request):
    cart = PlantationCartModel.objects.filter(user = request.user).first()
    return render(request, "cart.html", { "cart": cart })


@login_required(login_url="/users/login/")
def add_to_cart_view(request, pk, path):
    product = get_object_or_404(PlantationProduct, pk = pk)

    cart = PlantationCartModel.objects.filter(user = request.user).first()

    if not cart:
        cart = PlantationCartModel.objects.create(user = request.user)
        cart.save()

    if not cart.items.filter(product = product).exists():
        print("product is availabel but: ", cart.items.all().first())
        cart_item, created = PlantationProductDetails.objects.get_or_create(product=product, defaults={'quantity': 1})
        cart.items.add(cart_item)
        cart.save()
    else:
        item = cart.items.filter(product = product).first()
        item.increment()
        cart.save()

    return redirect(path)


@login_required(login_url="/users/login/")
def update_cart_view(request, pk):
    if request.method == "POST":
        product = get_object_or_404(PlantationProduct, pk = pk)
        cart = PlantationCartModel.objects.filter(user = request.user).first()
        quantity = request.POST.get("quantity")

        if not cart:
            return redirect("main:main")
        
        item = cart.items.filter(product = product).first()
        if item and quantity:
            item.define(quantity)
            cart.save()      

    return redirect("cart")

def remove_from_cart_view(request, pk):
    product = get_object_or_404(PlantationProduct, pk = pk)
    cart = PlantationCartModel.objects.filter(user = request.user).first()

    if not cart:
        return redirect("main:main")

    item = cart.items.filter(product = product).delete()
    # cart.items = item
    cart.save()
    

    return redirect("cart")

@login_required(login_url="/users/login/")
def checkout_view(request):
    order_form = PlantationOrderForm()
    address_form = PlantationAddressForm()
    cart = PlantationCartModel.objects.filter(user = request.user).first()

    if not cart:
        return redirect("cart") # nothing in th cart so go back

    context = { 
        "order_form": order_form,
        "address_form": address_form,
        "cart": cart
        }
    
    if request.method == "POST":
        order_form = PlantationOrderForm(request.POST)
        address_form = PlantationAddressForm(request.POST)

        # print("here is data")
        if order_form.is_valid() and address_form.is_valid():
            # print("everything is valid")
            address = address_form.save()
            order = order_form.save(False)

            order_items = []
            for cart_item in cart.items.all():
                item = PlantationOrderItemModel.objects.create(name = cart_item.product.name, 
                                                               quantity = cart_item.quantity,
                                                               price = cart_item.product.price, product_id = cart_item.product.pk)
                order_items.append(item)


            order.user = request.user
            order.quantity = cart.get_total_items()
            order.total_grand_price = cart.get_grand_total()
            order.address = address
            order.paid = False
            order.save() # redirect to payment and create an order 
            order.items.set(order_items)
            order.save()

            cart.delete()
            return redirect("pay-for-order", order.pk)       

    return render(request, "checkout.html", context)


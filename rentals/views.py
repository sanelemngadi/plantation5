from django.shortcuts import render, redirect, get_object_or_404
from rentals.forms import PlantationRentalForm, PlantationRentalImageForm
from rentals.models import PlantationRentalModel
from django.contrib.auth.decorators import login_required, user_passes_test
from products.models import PlantationProduct
from datetime import date

from django.http import Http404
from django.urls import reverse
from django.conf import settings
import uuid, os

from user import queries

from paypal.standard.forms import PayPalPaymentsForm

# def is_admin(user):
#     return user.is_staff or user.is_superuser


# def is_user(user):
#     return not user.is_staff or not user.is_superuser


# Create your views here.
@login_required(login_url='/users/login/')
def rental_list_view(request):
    rentals = PlantationRentalModel.objects.filter(user = request.user)
    rentals = PlantationRentalModel.objects.all()

    if queries.is_admin(request.user):
        print("This admin")
        rentals = PlantationRentalModel.objects.filter(paid = True)

    count_unread = rentals.filter(viewed = False).count() 
    count_not_accepted = rentals.filter(verified = False).count() 
    total = rentals.count()

    # if total == count_not_accepted:
    #     count_not_accepted = "all"

    context = { 
        "rentals": rentals, 
        "count_unread": count_unread,
        "count_not_accepted": count_not_accepted,
        "total": total
        }
    return render(request, "rental-list.html", context)

@login_required(login_url='/users/login/')
def confirm_rental_view(request, pk):
    rental = get_object_or_404(PlantationRentalModel, pk = pk)

    return render(request, "rental-confirm.html", { "rental": rental })

@login_required(login_url='/users/login/')
def rental_create_view(request, pk):
    form = PlantationRentalForm()

    rented_product = get_object_or_404(PlantationProduct, pk = pk)

    if request.method == "POST":
        form = PlantationRentalForm(request.POST)

        print("hello world")

        if form.is_valid():
            instance = form.save(False)
            instance.product = rented_product
            instance.user = request.user

            if instance.date_from <= date.today():
                print("this have to be after today")
                # raise ValueError("invalid items")
                form.add_error("date_from","Date from must always bigger than today")
                return render(request, "create-rental.html", { "form": form, "product": rented_product })

            if instance.date_from > instance.date_to:
                form.add_error("date_from","Date to must always bigger than date from")
                return render(request, "create-rental.html", { "form": form, "product": rented_product })

            if instance.date_from == instance.date_to:
                form.add_error("date_from","The item cannot be borrowed and returned same day")
                return render(request, "create-rental.html", { "form": form, "product": rented_product })
            instance.save()

            return redirect("rental-detail", pk = instance.pk)

    return render(request, "rental-create.html", { "form": form, "product": rented_product })

@user_passes_test(queries.is_admin)
def admin_rentals_view(request):
    pass


user_passes_test(queries.is_general)
def user_rentals_view(request):
    pass

def rental_detail_view(request, pk):
    try:
        rental = get_object_or_404(PlantationRentalModel, pk = pk)

        host = request.get_host()

        http = "https://"

        if settings.DEBUG:
            http = "http://"
        
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": rental.product.rent_price,
            "invoice": str(uuid.uuid4()),
            "currency_code": "USD",
            "item_name": rental.product.name,
            "notify_url": f'https://{host}{reverse("paypal-ipn")}',
            "return_url": f'{http}{host}{reverse("rental-success", kwargs={"pk": rental.pk})}',
            "cancel_return": f'{http}{host}{reverse("cancelled")}',
        }

        form = PayPalPaymentsForm(initial = paypal_dict)

        rental_form = PlantationRentalImageForm(instance=rental)

        if rental:
            rental.viewed = True
            rental.save()

        if request.method == "POST":
            rental_form = PlantationRentalImageForm(request.POST, instance=rental, files=request.FILES)

            if rental_form.is_valid():
                item = rental_form.save(False)
                item.pending = True
                item.save()
                return redirect("rental-detail", rental.pk)
        
    except Http404:
        return render(request, "problem.html")

    return render(request, "rental-detail.html", { "rental": rental, "rental_form": rental_form, "form": form })


def accept_rental(request, pk, accept):
    rental = get_object_or_404(PlantationRentalModel, pk = pk)

    if rental:
        if accept == "yes":
            rental.accepted = True
            rental.status = "accepted"
            rental.save()

    return redirect("rental-detail", pk)

def verify_rental_identity_view(request, pk):
    try:
        rental = get_object_or_404(PlantationRentalModel, pk = pk)
        rental.verified = True
        rental.status = "pending"
        rental.save()

    except Http404:
        return render(request, "problem.html")
    return redirect("rental-detail", rental.pk)

def rental_collection_view(request, pk):
    try:
        rental = get_object_or_404(PlantationRentalModel, pk = pk)
        rental.collected = True
        rental.status = "collected"
        rental.save()

    except Http404:
        return render(request, "problem.html")
    return redirect("rental-detail", rental.pk)

def rental_returned_view(request, pk):
    try:
        rental = get_object_or_404(PlantationRentalModel, pk = pk)
        rental.returned = True
        rental.status = "returned"
        rental.save()

    except Http404:
        return render(request, "problem.html")
    return redirect("rental-detail", rental.pk)

def reject_rental_identity_files(request, pk):
    try:
        rental = get_object_or_404(PlantationRentalModel, pk = pk)
        rental.verified = False
        rental.pending = False
        rental.status = "rejected"
        # rental.save()

        id_image_path = rental.id_image.path
        pp_path = rental.proof_of_residence.path

        rental.id_image = None
        rental.proof_of_residence = None
        rental.save()

        if os.path.isfile(id_image_path):
            os.remove(id_image_path)
        
        if os.path.isfile(pp_path):
            os.remove(pp_path)

    except Http404:
        return render(request, "problem.html")
    return redirect("rental-detail", rental.pk)


def rental_success(request, pk):
    try:
        rental = get_object_or_404(PlantationRentalModel, pk = pk)
        rental.paid = True
        rental.status = "pending"
        rental.save()

    except Http404:
        return render(request, "problem.html")
    return redirect("rental-detail", rental.pk)
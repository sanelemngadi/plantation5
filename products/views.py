from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.http.request import HttpRequest

from products.models import PlantationProduct
from products.forms import PlantationProductForm, PlantationProductUpdateForm, PlantationSupplierProductForm

from suppliers.models import PlantationSupplier
# from services.models import PlantationService
# Create your views here.
from user import queries

def is_admin(user):
    return user.is_staff or user.is_superuser

def product_list_view(request):
    products = PlantationProduct.objects.all() # we need to keep track of who created the product
    supplier_products = PlantationProduct.objects.filter(supplier__admin = request.user) # we need to keep track of who created the product
    return render(request, "product-list.html", { "products": products, "supplier_products": supplier_products })

# @login_required(login_url='/users/login/')
def product_detail_view(request, pk):
    product = get_object_or_404(PlantationProduct, pk = pk)
    similar = PlantationProduct.objects.filter(supplier__pk = product.supplier.pk).exclude(pk = pk)[:3]
    return render(request, "product-detail.html", { "product": product, "similar": similar })

@login_required(login_url='/users/login/')
@user_passes_test(queries.is_management)
def product_create_view(request):
    form = PlantationProductForm()

    products = PlantationSupplier.objects.exists()

    # service = get_object_or_404(PlantationService, pk = pk)
    if request.method == "POST":
        form = PlantationProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(False)
            # product.service = service
            product.save()
            # print("item is saved")
            return redirect("product-list")
            # return redirect("service-detail", service.pk)
    return render(request, "product-create.html", { "form": form, "products": products })

@login_required(login_url='/users/login/')
@user_passes_test(queries.is_management)
def product_remove_view(request, pk):
    product = get_object_or_404(PlantationProduct, pk = pk)

    if request.method == "POST" and product:
        try:
            product.delete()
        except Http404:
            return render(request, "problem.html")
        return redirect("product-list")
    
    return render(request, "product-remove.html", { "product": product } )

def is_management_or_supplier(user):
    return queries.is_management or queries.is_supplier

@login_required(login_url='/users/login/')
@user_passes_test(is_management_or_supplier)
def product_update_view(request: HttpRequest, pk):
    try:
        product = get_object_or_404(PlantationProduct, pk = pk)
        form = PlantationProductUpdateForm(instance=product)

        supplier_form = PlantationSupplierProductForm(instance=product)

        if request.method == "POST":
            form = PlantationProductUpdateForm(request.POST, instance=product)
            supplier_form = PlantationSupplierProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return redirect("product-list")
            
            if supplier_form.is_valid():
                print("the form is actually valid")
                supplier_form.save()
                return redirect("product-list")

    except Http404:
        return render(request, "problem.html")
    
    return render(request, "product-update.html", { "product": product, "form": form, "supplier_form": supplier_form })
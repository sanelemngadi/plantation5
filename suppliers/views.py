from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from suppliers.models import PlantationSupplier, PlantationSupplierOrderModel, PlantationOrderItemModel
from suppliers.forms import PlantationSupplierCreateForm

from django.contrib.auth.decorators import user_passes_test, login_required
from user import queries
from inventory.forms import PlantationStockForm
from inventory.models import PlantationStock

from django.contrib import messages

# Create your views here.
def supplier_list_view(request):
    suppliers = PlantationSupplier.objects.all()
    return render(request, "suppliers.html", { "suppliers": suppliers } )

def supplier_remove_view(request, pk):
    supplier = get_object_or_404(PlantationSupplier, pk = pk)

    if request.method == "POST" and supplier:
        supplier.delete()
        return redirect("suppliers")
    
    return render(request, "supplier-remove.html", { "supplier": supplier } )

@user_passes_test(queries.is_supplier)
def supplier_update_view(request, pk):
    supplier = get_object_or_404(PlantationSupplier, pk = pk)
    form = PlantationSupplierCreateForm(instance=supplier)

    if request.method == "POST" and supplier:
        form = PlantationSupplierCreateForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect("suppliers")
        
        context = { "supplier": supplier , "form": form }
        
    return render(request, "supplier-update.html", context )

# def supplier_create_view(request):
#     form = PlantationSupplierCreateForm()

#     if request.method == "POST":
#         form = PlantationSupplierCreateForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("suppliers")
        
#     return render(request, "supplier-create.html", { "form": form })

def supplier_detail_view(request, pk):   
    try:
        supplier = get_object_or_404(PlantationSupplier, pk = pk)
        # items = PlantationStock.objects.all()
        # stocks = PlantationStock.objects.filter(product__supplier = supplier).filter(status = "P")

        order = PlantationSupplierOrderModel.objects.filter(supplier = supplier).filter(active = True).first()
        if not order:
            order = PlantationSupplierOrderModel.objects.create(user = request.user, supplier = supplier)
            order.active = True
            order.save()

        form = PlantationStockForm()
        if request.method == "POST":
            form = PlantationStockForm(request.POST)
            if form.is_valid():
                stock: PlantationStock = form.save(False)

                if stock.product.supplier != supplier:
                    return redirect("supplier-detail", supplier.pk) 
                
                order_item = PlantationOrderItemModel.objects.create(name = stock.product.name, 
                                                                     price = stock.product.supplier_price, 
                                                                     quantity = stock.quantity, 
                                                                     product_id = stock.product.pk)

                order.items.add(order_item)
                order.save()
                return redirect("supplier-detail", supplier.pk)  
               
    except Http404:
        return render(request, "problem.html")

    context = { 
        "supplier": supplier, 
        "form": form, 
        # "items": items, 
        # "stocks": stocks, 
        "order": order
    }

    return render(request, "supplier-detail.html", context )


def supplier_order_accept(request, pk):
    try:
        order = get_object_or_404(PlantationSupplierOrderModel, pk = pk)

        if request.method == "POST":
            order.accepted = True
            order.save()
            return redirect("supplier-orders")

    except Http404:
        return render(request, "problem.html")
    
    return render(request, "supplier-order-accept.html", { "order": order })


def delete_order_item(request, pk, sup):
    try:
        order_item = get_object_or_404(PlantationOrderItemModel, pk = pk)
        supplier = get_object_or_404(PlantationSupplier, pk = sup)
        order_item.delete()

    except Http404:
        return render(request, "problem.html")
    return redirect("supplier-detail", supplier.pk)

def send_order_to_supplier(request, pk):
    try:
        order = get_object_or_404(PlantationSupplierOrderModel, pk = pk)
        order.active = False
        order.save()

    except Http404:
        return render(request, "problem.html")
    
    return redirect("supplier-detail", order.supplier.pk)
    
def confirm_order_to_supplier(request, pk):
    try:
        supplier = get_object_or_404(PlantationSupplier, pk = pk)
        order = PlantationSupplierOrderModel.objects.filter(supplier = supplier).filter(active = True).first()

    except Http404:
        return render(request, "problem.html")
    return render(request, "confirm-supplier-order.html", { "order": order, "supplier": supplier, "num": 256 })
    

def supplier_order_invoice(request, pk):
    try:
        order = get_object_or_404(PlantationSupplierOrderModel, pk = pk)
    except Http404:
        return render(request, "problem.html")
    return render(request,  "supplier-invoice.html", {"order": order})
    

def supplier_order_list(request):
    orders = PlantationSupplierOrderModel.objects.filter(active = False)
    return render(request, "supplier-order-list.html", { "orders": orders })


@login_required(login_url='/users/login/')
def supplier_order_list_view(request):
    try:
        supplier = PlantationSupplier.objects.filter(admin = request.user).first()
        orders = PlantationSupplierOrderModel.objects.filter(supplier = supplier).order_by("-date")

        if request.method == "POST":
            stock_id = request.POST.get("stock_id", None)
            print("id is: ", stock_id)

            if stock_id:
                stock = get_object_or_404(PlantationSupplierOrderModel, pk = int(stock_id))

                if stock:
                    stock.delivered = True
                    stock.save()
                    return redirect("supplier-orders")

    except Http404:
        return render(request, "problem.html")
    
    return render(request, "supplier-order.html", { "orders": orders })
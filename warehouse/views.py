from django.shortcuts import render, redirect
from django.http.request import HttpRequest

from warehouse.forms import PlantationWarehouseForm
from warehouse.models import PlantationWarehouse

from products.models import PlantationProduct

# Create your views here.

def warehouse_view(request: HttpRequest):
    form = PlantationWarehouseForm()
    products = PlantationProduct.objects.all()
    items = PlantationWarehouse.objects.all()

    if request.method == "POST":
        form = PlantationWarehouseForm(request.POST)

        if form.is_valid():
            warehouse: PlantationWarehouse = form.save(False) # filter orders by products add add the product quantity

            has_row = False
            has_shelf = False
            for item in items:
                if item.row == warehouse.row:
                    has_row = True
                
                if item.shelf == warehouse.shelf:
                    has_shelf = True
            if has_shelf and has_row:
                form.add_error("product", f"The Row {warehouse.row} and shelf {warehouse.shelf} has already been used")

            is_valid_warehouse = items.filter(product = warehouse.product).exists()
            if is_valid_warehouse:
                form.add_error("product", f"The product named: {warehouse.product.name } has already added to the warehouse")

                
            else:
                warehouse.save()
                return redirect("warehouse")

            

    return render(request, "warehouse.html", { "form": form, "products": products, "items": items })

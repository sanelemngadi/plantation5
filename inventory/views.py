from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required

from inventory.forms import PlantationStockForm
from inventory.models import PlantationStock
from warehouse.models import PlantationWarehouse
from warehouse.forms import PlantationWarehouseForm
from products.models import PlantationProduct

from suppliers.models import PlantationSupplier
# Create your views here.
def inventory_view(request):
    items = PlantationWarehouse.objects.all()
    products = PlantationStock.objects.all()
    form = PlantationStockForm()
    if request.method == "POST":
        form = PlantationStockForm(request.POST or None)
        if form.is_valid():
            stock: PlantationStock = form.save(False)
            stock.save()
            return redirect("inventory")
            

    return render(request, "inventory.html", { "form": form, "items": items, "products": products })

def stock_update_view(request, pk):
    try:
        stock = get_object_or_404(PlantationWarehouse, pk = pk)

        form = PlantationWarehouseForm(instance=stock)
    except Http404:
        return render(request, "problem.html")
    
    return render(request, "stock-update.html", { "form": form })

def stock_remove_view(request, pk):
    try:
        stock = get_object_or_404(PlantationWarehouse, pk = pk)
    except Http404:
        return render(request, "problem.html")
    
    return render(request, "stock-remove.html", { "stock": stock })


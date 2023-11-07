from django.shortcuts import render, get_object_or_404, redirect
from delivery.models import PlantationDelivery
from django.http import Http404
from user import emails

# Create your views here.
def delivery_list_view(request):

    if request.method == "POST":
        delivery = request.POST.get("delivery", None)

        if delivery:
            try:
                item = get_object_or_404(PlantationDelivery, pk = int(delivery))
                item.settled = True
                item.save()
                name = item.client.get_name()
                message = f"Hi {name}\n\nThank you for ordering with us.\n\nRegards\nPlantation"
                emails.email_user(item.client, "Order pending for delivery".capitalize(), message)
                return redirect("delivery-list")
            except Http404:
                return render(request, "problem.html")
            
            # print("delivery pk is: ", delivery)
    return render(request, "delivery-list.html")
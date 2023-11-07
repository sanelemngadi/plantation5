from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import Http404

from events.models import PlantationEventModel
from notifications.models import PlantationNotification
# Create your views here.
def is_stuff(user):
    return user and (not user.is_superuser or not user.is_staff)

@login_required(login_url='/users/login/')
# @user_passes_test(is_stuff)
def notification_list_view(request):
    # notifications = PlantationNotificationsModel.objects.filter(user = request.user)
    # notifications = PlantationNotification.objects.filter(recipients__user = request.user)
    return render(request, "notifications.html")

@login_required(login_url='/users/login/')
def notification_detail_view(request, pk):
    try:
        notification = get_object_or_404(PlantationNotification, pk = pk)

        if not notification.read:
            notification.read = True
            notification.save()
    except Http404:
        return render(request, "problem.html")
    
    return render(request, "notification-detail.html", { "notification": notification})

@login_required(login_url='/users/login/')
def notification_order_view(request, pk):
    # notification = get_object_or_404(PlantationNotificationsModel, pk = pk)

    bought_vip = True
    if request.method == "POST":
        data = request.POST.get("ticket", None)

        if data and data == "general":
            # notification.bought_vip = False
            bought_vip = False
            # notification.save()
        

    return render(request, "confirm-notification-order.html", { "bought_vip": bought_vip })

@login_required(login_url='/users/login/')
def pay_order_view(request, pk):
    # notification = get_object_or_404(PlantationNotificationsModel, pk = pk)
    # if notification:
    #     notification.rsvped = True
    #     notification.save()
    # return redirect("notification", notification.pk)
    pass
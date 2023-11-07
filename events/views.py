from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse

from django.core.files import File
from django.core.files.base import ContentFile
from django.http import FileResponse


from events.forms import PlantationEventForm, PlantationRSVPEventForm
from events.models import PlantationEventModel
from user.models import PlantationUser
# from notifications.models import PlantationNotificationsModel

import qrcode, json, uuid, os
from user import queries

from django.http import Http404
from paypal.standard.forms import PayPalPaymentsForm

from user import emails

# Create your views here.
@login_required(login_url='/users/login/')
# @user_passes_test(queries.is_management)
def event_list_view(request):
    events = PlantationEventModel.objects.all()
    return render(request, "events.html", { "events": events })

@login_required(login_url='/users/login/')
@user_passes_test(queries.is_management)
def event_create_view(request):
    form = PlantationEventForm()
    if request.method == "POST":
        form = PlantationEventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            # form_sent = True
            event.host = request.user
            event.save()

            users = PlantationUser.objects.filter(is_staff=False).filter(is_superuser=False)
            for user in users:
                # notification = PlantationNotificationsModel.objects.create(user = user, event = event)
                # notification.save()
                pass

                # notification, created = PlantationNotificationsModel.objects.get_or_create(user=user, event=event)
                # if created:
                #     notification.viewed = False  # Set any other initial values as needed
                #     notification.rsvped = False
                #     notification.attended = False
                #     notification.save()
                


            return redirect("events")
    return render(request, "create-events.html", {"form": form})


@login_required(login_url='/users/login/')
def event_detail_view(request, pk):
    try:
        print("this is the event detail")
        event = get_object_or_404(PlantationEventModel, pk = pk)
        event_form = PlantationRSVPEventForm(instance=event)
        accepted = False
        general = True
        price = 0.0

        host = request.get_host()

        http = "https://"

        if settings.DEBUG:
            http = "http://"
        
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": 5,
            "invoice": str(uuid.uuid4()),
            "currency_code": "USD",
            "item_name": "Plantation cart",
            "notify_url": f'https://{host}{reverse("paypal-ipn")}',
            "return_url": f'{http}{host}{reverse("download", kwargs={"event_id": event.pk})}',
            "cancel_return": f'{http}{host}{reverse("cancelled")}',
        }

        paypal_form = PayPalPaymentsForm(initial = paypal_dict)

        if request.method == "POST":
            event_form = PlantationRSVPEventForm(request.POST, instance=event)
            if event_form.is_valid():
                accepted = True
                rsvp: PlantationEventModel = event_form.save(commit=False)
                price = rsvp.general_price

                if rsvp.ticket == "V":
                    general = False
                    price = rsvp.vip_price
            paypal_dict["amount"] = price
            
    except Http404:
        return render(request, "problem.html")

    context = { 
        "event": event, 
        "event_form": event_form, 
        "accepted": accepted ,
        "price": price ,
        "general": general ,
        "paypal_form": paypal_form ,
        }
    return render(request, "events-detail.html", context)


def download_event_qr_view(request, pk):
    try:
        event = get_object_or_404(PlantationEventModel, pk = pk)

        data = {
            "name": request.user.get_name(),
            "event": event.title,
            "ticket_id": "0000" + str(event.pk) + str(request.user.pk)
        }
    
         # Create a QR code instance
        data_as_json = json.dumps(data)
    
        # Create a QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_as_json)
        qr.make(fit=True)
    
        # Create an image object
        img = qr.make_image(fill_color="black", back_color="white")

        # Construct the image file path
        image_filename = f"qr_code_{data['ticket_id']}.png" 

        image_path = os.path.join(settings.MEDIA_ROOT, image_filename)


        # Save the image to the images folder
        img.save(image_path)
        # # Create a response with the image content type
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")

        name = request.user.get_name()
        message = f"Hi {name}\n\nThank you for reserving a seat for this event.\n\hPlease find attached qr code for you entrance.\n\nRegards\nPlantation"

        emails.attach_image_email(request.user, f"{request.user.get_name()} RSVP EVENT", message, image_path)


        
        
        
        return response
    except Exception as e:
        print(e)
        return redirect("main:main")
    

def event_payment_success(request, event_id):
    try:
        event = get_object_or_404(PlantationEventModel, pk = event_id)
        event.paid = True
        event.save()
        
        return download_event_qr_view(request, pk=event_id)

    except Http404:
        return render(request, "problem.html")
    return redirect("event", event_id)
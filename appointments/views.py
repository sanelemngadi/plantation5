from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.http.request import HttpRequest

from appointments.models import PlantationAppointmentsModel
from appointments.forms import PlantationAppointmentForm, PlantationAssignUserForm

from notifications import forms
from notifications.models import PlantationNotification, PlantationNotificationStatus

from user import queries, emails

# Create your views here.
@login_required(login_url='/users/login/')
# @user_passes_test(queries.is_management)
def appointment_list_view(request):
    appointments = PlantationAppointmentsModel.objects.all()

    if queries.is_general(request.user):
        appointments = PlantationAppointmentsModel.objects.all().filter(user = request.user)

    if queries.is_staff(request.user):
        appointments = PlantationAppointmentsModel.objects.filter(fumigator = request.user)
        
        
    return render(request, "appointments.html", { "appointments": appointments })

@login_required(login_url='/users/login/')
def appointment_confirm_view(request, pk):
    try:
        appointment = get_object_or_404(PlantationAppointmentsModel, pk=pk)

        if request.method == "POST":
            appointment.confirmed = True
            appointment.save()
            return redirect("detail-appointment", appointment.pk)
        
    except Http404:
        return render(request, "problem.html")

    return render(request, "confirm-appointment.html", { "appointment": appointment} )
    
@login_required(login_url='/users/login/')
def appointment_create_view(request):
    form = PlantationAppointmentForm()
    if request.method == "POST":
        form = PlantationAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(False)
            appointment.user = request.user
            appointment.fumigator = None
            appointment.price_per_sqm = 250
            appointment.save()

            return redirect("confirm-appointment", pk = appointment.pk)

    return render(request, "create-appointment.html", { "form": form })

@login_required(login_url='/users/login/')
def appointment_detail_view(request: HttpRequest, pk):
    try:
        appointment = get_object_or_404(PlantationAppointmentsModel, pk = pk)

        form = PlantationAssignUserForm(instance=appointment)

        if request.method == "POST":
            form = PlantationAssignUserForm(request.POST, instance=appointment)

            if form.is_valid():
                appointment: PlantationAppointmentsModel = form.save(False)

                # if not appointment.fumigator:
                #     form.add_error("fumigator", "Please assign this booking to a valid user")
                #     # print("this appointment is not valid")
                # else:
                message = f"Hi {appointment.fumigator.get_name()}\nYou have been appointment by the administor to make a follow up with our\nrecent booking that has been forwarded to you with the following details: \nAppointment type: {appointment.appointment_service_type}\nFumigation Area: {appointment.fumigation_area}\nClient: {appointment.user.get_name()}\nLocation: {appointment.location}\n\nMessage from: {request.user.get_name()}"
                status = PlantationNotificationStatus.objects.create(notification_from = request.user, message = message)
                notification = PlantationNotification.objects.create(user = appointment.fumigator, notification = status)
                # notification.recipients.add(status)
                appointment.assigned = True 
                # name = appointment.fumigator.get_name()
                emails.email_user(appointment.fumigator, "Fumigation Appointment".capitalize(), message)              
                
                appointment.save()
                # print("this is a valid appoint")
                return redirect("detail-appointment", appointment.pk )


    except Http404:
        return render(request, "problem.html")    
    return render(request, "detail-appointment.html", { "appointment": appointment, "form": form })
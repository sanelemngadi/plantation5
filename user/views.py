from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages
from django.http import Http404

from user.forms import RegistrationForm, PlantationUpdateUserForm

from user.models import PlantationUser
from user import queries

from suppliers.forms import PlantationSupplierCreateForm
from suppliers.models import PlantationSupplier

def is_staff(user):
    return not user.is_staff and not user.is_superuser

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Redirect to a success page
            return redirect("main:main")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})




def register_view(request):
    # as_admin = request.GET.get("as_admin")
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user: PlantationUser = form.save(commit=False)
            user.role = "G"
            user.is_general = True
            user.save()
            # Redirect to a success page or login the user
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form, "as_admin": "as_admin"})


def logout_view(request):
    logout(request)
    return redirect("login")

def settings_view(request):
    return render(request, "settings.html")


def manage_users_view(request):
    users = PlantationUser.objects.filter(role = "G").exclude(pk = request.user.pk)
    staff = PlantationUser.objects.filter(role = "S").exclude(pk = request.user.pk)
    delivery = PlantationUser.objects.filter(role = "D").exclude(pk = request.user.pk)
    admin = PlantationUser.objects.filter(role = "A").exclude(pk = request.user.pk)

    context = {
        "users": users, "staff": staff, "delivery": delivery, "admin": admin
    }
    return render(request, "manage-users.html", context)


def user_update_view(request, pk):
    try:
        user = get_object_or_404(PlantationUser, pk = pk)
        form = PlantationUpdateUserForm(instance = user)

        if request.method == "POST":
            form = PlantationUpdateUserForm(request.POST, instance=user)

            if form.is_valid():
                person:PlantationUser = form.save(commit=False)
                queries.switch_all(person, person.role)
                person.save()
                return redirect("manage-users")
    except Http404:
        render(request, "problem.html")

    return render(request, "user-update.html", { "form": form })


def user_remove_view(request, pk):
    try:
        user = get_object_or_404(PlantationUser, pk = pk)

        if request.method == "POST":
            # user.delete()
            queries.switch_all(user, "N")
            user.save()
            return redirect("manage-users")
    except Http404:
        render(request, "problem.html")

    return render(request, "user-remove.html")


def supplier_register_view(request):
    # as_admin = request.GET.get("as_admin")
    form  = RegistrationForm()
    supplier_form = PlantationSupplierCreateForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        supplier_form = PlantationSupplierCreateForm(request.POST)
        if form.is_valid() and supplier_form.is_valid():
            user: PlantationUser = form.save(commit=False)
            user.role = "P"
            user.is_general = False
            user.is_supplier = True
            user.save()

            supplier: PlantationSupplier = supplier_form.save(commit=False)
            supplier.admin = user
            supplier.save()
            # Redirect to a success page or login the user
            return redirect('login')

    return render(request, 'supplier-register.html', {'form': form, "supplier_form": supplier_form })
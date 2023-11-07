from django import forms 
from suppliers.models import PlantationSupplier, PlantationSupplierOrderModel

class PlantationSupplierCreateForm(forms.ModelForm):
    class Meta:
        model = PlantationSupplier
        fields = "__all__"

        exclude = ("admin",)

class PlantationSupplierOrdeCreaterForm(forms.ModelForm):
    class Meta:
        model = PlantationSupplier
        fields = "__all__"


class PlantationSupplierOrderConfirmForm(forms.ModelForm):
    class Meta:
        model = PlantationSupplier
        fields = "__all__"

        exclude = ("admin",)
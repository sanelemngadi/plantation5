from django import forms
from rentals.models import PlantationRentalModel

class PlantationRentalForm(forms.ModelForm):
    class Meta:
        model = PlantationRentalModel
        fields = "__all__"

        exclude = ("user", "product", "status", "returned", "collected", "paid", "id_image","proof_of_residence", "qr_tag")

        widgets = {
            "date_from": forms.DateInput(attrs={"type": "date"}),
            "date_to": forms.DateInput(attrs={"type": "date"}),
            "reason": forms.Textarea(attrs={"type": "textarea"}),
        }


class PlantationRentalImageForm(forms.ModelForm):
    class Meta:
        model = PlantationRentalModel
        fields = ("id_image","proof_of_residence")

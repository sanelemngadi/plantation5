from django import forms
from delivery.models import PlantationDelivery
from user.models import PlantationUser

class PlantationDeliveryForm(forms.ModelForm):
    class Meta:
        model = PlantationDelivery
        fields = ("driver",)

    def __init__(self, *args, **kwargs):
        super(PlantationDeliveryForm, self).__init__(*args, **kwargs)

        self.fields["driver"].queryset = PlantationUser.objects.filter(is_delivery_man = True)

class PlantationDeliveryCompleteForm(forms.ModelForm):
    class Meta:
        model = PlantationDelivery
        fields = ("settled",)
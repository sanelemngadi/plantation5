from django import forms
from warehouse.models import PlantationWarehouse

class PlantationWarehouseForm(forms.ModelForm):
    class Meta:
        model = PlantationWarehouse
        fields = "__all__"
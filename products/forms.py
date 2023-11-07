from django import forms
from products.models import PlantationProduct

class PlantationProductForm(forms.ModelForm):
    class Meta:
        model = PlantationProduct
        fields = "__all__"

        exclude = ("quantity", "supplier_price")

class PlantationProductUpdateForm(forms.ModelForm):
    class Meta:
        model = PlantationProduct
        fields = "__all__"

class PlantationSupplierProductForm(forms.ModelForm):
    class Meta:
        model = PlantationProduct
        fields = ("supplier_price",)
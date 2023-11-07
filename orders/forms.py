from django import forms
from orders.models import PlantationOrderModel, PlantationAddress

class PlantationOrderForm(forms.ModelForm):
    class Meta:
        model = PlantationOrderModel
        fields = "__all__"

        exclude = ("user", "paid", "items", "quantity", "address", "card_information", "order_number", "collected", "total_grand_price")


# class PlantationCardInformationForm(forms.ModelForm):
#     class Meta:
#         model = PlantationCardInformation
#         fields = "__all__"


class PlantationAddressForm(forms.ModelForm):
    class Meta:
        model = PlantationAddress
        fields = "__all__"
from django import forms
from inventory.models import PlantationStock
from products.models import PlantationProduct

class PlantationStockForm(forms.ModelForm):
    class Meta:
        model = PlantationStock
        fields = "__all__"

        exclude = ("status",)
    
    def __init__(self, *args, **kwargs):
        # Get the supplier from the instance (if it exists) or from the initial data
        instance = kwargs.get('instance')
        initial = kwargs.get('initial', {})
        supplier = None

        if instance:
            supplier = instance.product.supplier
        elif 'product' in initial:
            supplier = initial['product'].supplier

        super(PlantationStockForm, self).__init__(*args, **kwargs)

        # Filter the queryset for the 'product' field to only show products from the same supplier
        if supplier:
            self.fields['product'].queryset = PlantationProduct.objects.filter(supplier=supplier)

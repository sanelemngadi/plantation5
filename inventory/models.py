from django.db import models
from suppliers.models import PlantationSupplier
from products.models import PlantationProduct

class PlantationStock(models.Model):
    CHOICE = (("P", "Pending for delivery"), ("D", "Delivered"))
    product = models.ForeignKey(PlantationProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=CHOICE, default="P")
    

    def __str__(self):
        return f"{self.product.name}"
    
    def get_total_amount(self):
        return float(self.product.quantity) * self.product.price
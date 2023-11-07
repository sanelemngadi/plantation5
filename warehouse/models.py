from django.db import models
from products.models import PlantationProduct

# Create your models here.

class PlantationWarehouse(models.Model):
    row = models.CharField(max_length=50)
    shelf = models.CharField(max_length=50)
    product = models.ForeignKey(PlantationProduct, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} located at Row: {self.row} Shelf: {self.shelf}"
    
    def get_total_price(self):
        return self.product.price * self.product.quantity

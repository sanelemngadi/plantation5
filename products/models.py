from django.db import models
from suppliers.models import PlantationSupplier

# Create your models here.
class PlantationProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    rent_price = models.FloatField(default=0.0)
    supplier_price = models.FloatField(default=0.0)
    available = models.BooleanField(default=True)
    discount_percentage = models.IntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    supplier = models.ForeignKey(PlantationSupplier, on_delete=models.CASCADE, related_name="products")
    quantity = models.IntegerField(default=0)

    class Meta:
        ordering = ("-date",)

    def buy(self, quantity): # when we buy we subtract from stock and email the admin that we dont have no more stock
        self.quantity -= quantity
        self.save()
        
    def add_stock(self, quantity):
        self.quantity += quantity
        self.save()

    def __str__(self):
        return self.name
    
    def get_total_price(self):
        return self.quantity * self.price
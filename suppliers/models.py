from django.db import models
from user.models import PlantationUser 
from orders.models import PlantationAddress, PlantationOrderItemModel

class PlantationSupplier(models.Model):
    name = models.CharField(max_length=70)
    street_number = models.CharField(max_length=70)
    street_name = models.CharField(max_length=70)
    provice = models.CharField(max_length=70)
    telephone = models.CharField(max_length=12)
    admin = models.ForeignKey(PlantationUser, on_delete=models.CASCADE, related_name="suppliers")

    def __str__(self):
        return self.name

class PlantationSupplierOrderModel(models.Model):
    date = models.DateField(auto_now_add=True)
    items = models.ManyToManyField(PlantationOrderItemModel, blank=True)
    user = models.ForeignKey(PlantationUser, on_delete=models.CASCADE, related_name="supplier_orders")
    delivered = models.BooleanField(default=False) #if it is paid it becomes an order otherwise it stays in cart
    accepted = models.BooleanField(default=False) #if it is paid it becomes an order otherwise it stays in cart
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    supplier = models.ForeignKey(PlantationSupplier, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order: {self.order_number()}"
    
    def order_number(self):
        return f"0000{self.pk}"
    
    def get_total_tax(self):
        return (1 - 0.15) * self.get_total()
    
    def get_total(self):
        price = 0

        for item in self.items.all():
            price += item.price
        return price
    
    def get_gross_total(self):
        return self.get_total() + self.get_total_tax() + 250
    
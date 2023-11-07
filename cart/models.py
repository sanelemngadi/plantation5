from django.db import models
from user.models import PlantationUser
from products.models import PlantationProduct

# Create your models here.

class PlantationProductDetails(models.Model):
    product = models.ForeignKey(PlantationProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def increment(self):
        self.quantity += 1
        self.save()

    def define(self, number: int):
        self.quantity = number
        self.save()

    def get_total_price(self):
        return self.quantity * self.product.price


class PlantationCartModel(models.Model):
    user = models.ForeignKey(PlantationUser, on_delete=models.CASCADE, related_name="carts")
    items = models.ManyToManyField(PlantationProductDetails, blank=True)

    def __str__(self):
        return self.user.first_name + "' cart"
    
    def get_net_total(self):
        return self.get_total_price() - self.get_total_discount()
    
    def get_grand_total(self):
        return self.get_net_total() + self.get_total_tax() + self.get_delivery_price()
    
    def get_total_price(self):
        total_price = 0
        for item in self.items.all():
            price = item.product.price
            count = item.quantity
            total_price += (count * price)
        return total_price
    
    def get_total_items(self):
        total_items = 0
        for item in self.items.all():
            count = item.quantity
            total_items += count
        return total_items
    
    def get_total_tax(self):
        return self.get_total_price() * 15 / 100
    
    def get_total_discount(self):
        total_discount = 0
        for item in self.items.all():
            count = item.quantity
            price = item.product.price
            discount_perc = item.product.discount_percentage
            discount = (count * price) * (discount_perc / 100)
            total_discount += discount
        if total_discount < 0:
            return 0
        return total_discount
    
    def get_delivery_price(self):
        return 250

    
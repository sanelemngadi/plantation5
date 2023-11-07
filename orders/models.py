from django.db import models
from user.models import PlantationUser
# from cart.models import PlantationProductDetails

# Create your models here.
class PlantationAddress(models.Model):
    street_number = models.CharField(max_length=255)
    street_name = models.CharField(max_length=255)
    street_type = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    zip_code = models.IntegerField()

    def __str__(self):
        return f"{self.street_number} {self.street_name} {self.street_type} | {self.town} | {self.zip_code}"

    def get_street(self):
        return f"{self.street_number} {self.street_name} {self.street_type} | {self.town} | {self.zip_code}"
    
    def get_street_line(self):
        return f"{self.street_number} {self.street_name} {self.street_type}"
    

class PlantationOrderItemModel(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField()
    product_id = models.IntegerField()

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"order {self.name} for {self.price}"

class PlantationOrderModel(models.Model):
    DELIVERY_OPTIONS = (("D", "Delivery"), ("C", "Collect"))
    PAYMENT_OPTIONS = (("C", "Cash"), ("P", "Paypal"))

    date = models.DateField(auto_now_add=True)
    items = models.ManyToManyField(PlantationOrderItemModel, blank=True)
    user = models.ForeignKey(PlantationUser, on_delete=models.CASCADE, related_name="orders")
    paid = models.BooleanField(default=False) #if it is paid it becomes an order otherwise it stays in cart
    collected = models.BooleanField(default=False) #if it is paid it becomes an order otherwise it stays in cart
    quantity = models.IntegerField(default=1)
    cellphone = models.CharField(max_length=10)
    address = models.ForeignKey(PlantationAddress, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    # order_number = models.IntegerField(default=0000)

    delivery_option = models.CharField(max_length=2, choices=DELIVERY_OPTIONS)
    payment_option = models.CharField(max_length=2, choices=PAYMENT_OPTIONS)
    total_grand_price = models.FloatField(default=0)

    has_driver = models.BooleanField(default=False)

    def __str__(self):
        return f"Order: {self.order_number}"
    
    def order_number(self):
        return f"0000{self.pk}"
    
    def get_total(self):
        return (1 - 0.15) *self.total_grand_price
    
    def get_total_tax(self):
        return (0.15) *self.total_grand_price

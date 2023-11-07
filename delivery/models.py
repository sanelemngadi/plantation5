from django.db import models
from orders.models import PlantationAddress, PlantationOrderModel
from user.models import PlantationUser

# Create your models here.
class PlantationDelivery(models.Model):
    address = models.ForeignKey(PlantationAddress, on_delete=models.PROTECT)
    client = models.ForeignKey(PlantationUser, on_delete=models.CASCADE)
    driver = models.ForeignKey(PlantationUser, on_delete=models.CASCADE, related_name="deliveries")
    order = models.ForeignKey(PlantationOrderModel, on_delete=models.CASCADE)
    settled = models.BooleanField(default=False)
    pay_with_cash = models.BooleanField(default=False)
    otp = models.CharField(max_length=5, default="12345")
    date_created = models.DateTimeField(auto_now_add=True)
    date_delivered = models.DateTimeField(auto_now=True)
    order_number = models.CharField(max_length=50)

    def __str__(self):
        return f"delivery: {self.otp} for {self.client.get_name()}"
    
    class Meta:
        ordering = ("-date_created",)
        verbose_name_plural = "PlantationDeliveries"
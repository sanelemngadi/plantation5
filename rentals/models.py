from django.db import models
from products.models import PlantationProduct
# from django.contrib.auth.models import User
from user.models import PlantationUser

# Create your models here.

class PlantationRentalModel(models.Model):
    STATUS_CHOICES = (
        ("pending", "pending"),
        ("overdue", "overdue"),
        ("returned", "returned"),
        ("rejected", "rejected"),
        ("collected", "collected"),
    )
    # when we delete a rental we don't need to delete a product not even by a mistake
    product = models.ForeignKey(PlantationProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(PlantationUser, on_delete=models.CASCADE, related_name="rentals")
    date_request = models.DateTimeField(auto_now_add=True)
    date_from = models.DateField()
    date_to = models.DateField()
    returned = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    reason = models.CharField(max_length=255)
    collected = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    pending = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)
    id_image = models.ImageField(upload_to='images/',  blank=True, null=True)
    proof_of_residence = models.ImageField(upload_to='images/', blank=True, null=True)
    qr_tag = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} rented {self.product.name}"
    
    def count_days(self):
        return (self.date_to - self.date_from).days
    
    class Meta:
        ordering = ("-date_request", )

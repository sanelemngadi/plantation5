from django.db import models
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from user.models import PlantationUser

# Create your models here.

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

class PlantationAppointmentsModel(models.Model):
    APPOINTMENT_TYPE = (("indoor", "Indoor"), ( "outdoor", "Outdoor"))
    # title = models.CharField(max_length=255)
    appointment_service_type = models.CharField(max_length=50, choices=APPOINTMENT_TYPE)
    date = models.DateField()
    # description = models.TextField()
    fumigation_area = models.FloatField() #in square meters
    price_per_sqm = models.FloatField()

    user = models.ForeignKey(PlantationUser, on_delete=models.CASCADE)
    fumigator = models.ForeignKey(PlantationUser, on_delete=models.CASCADE, 
                                  related_name="appointments", blank=True, null=True)
    # accepted = models.BooleanField(default=False)
    # reviewed = models.BooleanField(default=False)
    # confirmed = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    location = models.CharField(max_length=255, default="Cape town offices")
    appointment_service_completed = models.BooleanField(default=False) # is service provided
    paid = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)

    def clean(self):
        # Check if the assigned fumigator is a staff member
        if self.fumigator and not self.fumigator.is_staff:
            raise ValidationError("Fumigator must be a staff member.")
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate the model
        super().save(*args, **kwargs)

    def get_total_price(self):
        return self.fumigation_area * self.price_per_sqm
    
    def get_day(self):
        return self.date.day
    
    def get_month(self):
        return MONTHS[self.date.month - 1]
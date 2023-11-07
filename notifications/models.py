from django.db import models
from user.models import PlantationUser
from events.models import PlantationEventModel

# Create your models here.
# class PlantationNotificationsModel(models.Model):
#     user = models.ForeignKey(PlantationUser, on_delete=models.CASCADE, related_name="notifications")
#     event = models.ForeignKey(PlantationEventModel, on_delete=models.PROTECT)
#     viewed = models.BooleanField(default=False)
#     rsvped = models.BooleanField(default=False)
#     attended = models.BooleanField(default=False)
#     bought_vip = models.BooleanField(default=True)

#     qr_image = models.ImageField(upload_to="images/", max_length=800, null=True, blank=True)

#     def __str__(self):
#         return f"notification for: {self.user.get_name()}"


class PlantationNotificationStatus(models.Model):
    notification_from = models.ForeignKey(PlantationUser, on_delete=models.CASCADE, related_name="sent_notifications")
    # recipients = models.ManyToManyField(PlantationNotificationStatus)
    message = models.TextField()
    subject = models.CharField(max_length=50, default="Appointment")
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_time",)
    
    def __str__(self):
        return f"Message from {self.notification_from.get_name}"

class PlantationNotification(models.Model):
    user = models.ForeignKey(PlantationUser, on_delete=models.CASCADE, related_name="notifications")
    read = models.BooleanField(default=False)
    notification = models.ForeignKey(PlantationNotificationStatus, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_time",)
from django.contrib import admin
from notifications.models import PlantationNotificationStatus, PlantationNotification

# Register your models here.

# admin.site.register(PlantationNotificationsModel)
admin.site.register(PlantationNotificationStatus)
admin.site.register(PlantationNotification)

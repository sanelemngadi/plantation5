from django.contrib import admin
from orders.models import PlantationOrderModel, PlantationAddress, PlantationOrderItemModel

# Register your models here.

admin.site.register(PlantationOrderModel)
admin.site.register(PlantationAddress)
admin.site.register(PlantationOrderItemModel)
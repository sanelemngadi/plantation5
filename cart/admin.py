from django.contrib import admin
from cart.models import PlantationCartModel, PlantationProductDetails

# Register your models here.


admin.site.register(PlantationCartModel)
admin.site.register(PlantationProductDetails)
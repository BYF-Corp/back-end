from django.contrib import admin
from .models import *

admin.site.register(FriedItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Flavor)
admin.site.register(Size)
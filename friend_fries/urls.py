from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from menu.views import *

router = DefaultRouter()
router.register(r'fried', FriedItemViewSet)
router.register(r'order', OrderViewSet)
router.register(r'order-item', OrderItemViewSet)
router.register(r'size', SizeViewSet)
router.register(r'flavor', FlavorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('menu.urls')),
    path('api/dashboard/summary/', dashboard_summary, name='dashboard-summary'),
]
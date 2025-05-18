from django.urls import path
from .views import delete_order

urlpatterns = [
    path('delete-order/<int:pk>/', delete_order, name='delete_order'),
]

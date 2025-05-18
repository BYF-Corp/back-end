from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FriedItem, Order, OrderItem, Size, Flavor
from .serializers import *
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count
from django.utils.timezone import now, timedelta

class FriedItemViewSet(viewsets.ModelViewSet):
    queryset = FriedItem.objects.all()
    serializer_class = FriedItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class FlavorViewSet(viewsets.ModelViewSet):
    queryset = Flavor.objects.all()
    serializer_class = FlavorSerializer

@csrf_exempt
def delete_order(request, pk):
    if request.method == 'DELETE':
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return JsonResponse({'message': 'Deleted successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
    else:
        return HttpResponseNotAllowed(['DELETE'])

@api_view(['GET'])
def dashboard_summary(request):
    today = now().date()
    week_ago = today - timedelta(days=6)

    today_orders = Order.objects.filter(date_ordered__date=today)
    today_revenue = sum(o.get_total_price() for o in today_orders)

    month_orders = Order.objects.filter(date_ordered__month=today.month, date_ordered__year=today.year)
    month_revenue = sum(o.get_total_price() for o in month_orders)

    total_orders = Order.objects.count()

    best_sellers = (
        OrderItem.objects
        .values('fried__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:5]
    )

    popular_flavors = (
        Flavor.objects
        .annotate(times_used=Count('orderitem'))
        .order_by('-times_used')[:5]
    )

    popular_sizes = (
        Size.objects
        .annotate(total_sold=Sum('orderitem__quantity'))
        .order_by('-total_sold')[:5]
    )

    daily_sales = []
    for i in range(7):
        day = today - timedelta(days=i)
        orders = Order.objects.filter(date_ordered__date=day)
        revenue = sum(o.get_total_price() for o in orders)
        daily_sales.append({
            'date': day.strftime('%Y-%m-%d'),
            'revenue': revenue
        })

    daily_sales.reverse()

    return Response({
        'today_revenue': round(today_revenue, 2),
        'month_revenue': round(month_revenue, 2),
        'total_orders': total_orders,
        'best_sellers': list(best_sellers),
        'popular_flavors': [
            {'flavor': f.flavor_name, 'times_used': f.times_used}
            for f in popular_flavors
        ],
        'popular_sizes': [
            {'size': s.size_name, 'total_sold': s.total_sold}
            for s in popular_sizes
        ],
        'daily_sales': daily_sales
    })
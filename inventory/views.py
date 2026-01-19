from django.shortcuts import render
from django.db.models import Count, Sum, F
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, StockMovement
from .serializers import ProductSerializer, StockMovementSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class StockMovementViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer


class DashboardStatsView(APIView):
    def get(self, request):
        total_products = Product.objects.count()
        low_stock_count = Product.objects.filter(quantity__lte=F('low_stock_threshold')).count()    # __lte = less than equal too.
        inventory_value_result = Product.objects.aggregate(total_value=Sum(F('price') * F('quantity')))
        total_inventory_value = inventory_value_result['total_value'] or 0

        data = {
            "total_products": total_products,
            "low_stock_products": low_stock_count,
            "total_inventory_value": total_inventory_value
        }

        return Response(data)
    
def dashboard_ui(request):
    return render(request, 'inventory/dashboard.html')
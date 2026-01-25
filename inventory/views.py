import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class DashboardStatsView(APIView):
    def get(self, request):
        total_products = Product.objects.count()
        low_stock_count = Product.objects.filter(quantity__lte=F('low_stock_threshold')).count()    # __lte = less than equal too.
        inventory_value_result = Product.objects.aggregate(total_value=Sum(F('price') * F('quantity')))
        total_inventory_value = inventory_value_result['total_value'] or 0

        data = {
            "total_products": total_products,
            "low_stock_count": low_stock_count,
            "total_inventory_value": total_inventory_value
        }

        return Response(data)
@login_required
def dashboard_ui(request):
    return render(request, 'inventory/dashboard.html')

class StockMovementExportView(APIView):
    def get(self, request):
        # 1. Get dates from URL parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # 2. Filter the QuerySet
        queryset = StockMovement.objects.all().select_related('product')

        if start_date:
            queryset = queryset.filter(date__date__gte=start_date)  # gte = greater than or equal
        if end_date:
            queryset = queryset.filter(date__date__lte=end_date)

        # 3. Create the Response Object (The "file")
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        # Add BOM for Excel to recognize UTF-8
        response.write('\ufeff')
        response['Content-Disposition'] = 'attachment; filename="stock_report.csv"'

        # 4. Create the CSV Writer
        writer = csv.writer(response)
        writer.writerow(['Date', 'Product', 'Type', 'Quantity', 'User', 'User Note'])   # Header Row

        # 5. Write Data
        for movement in queryset:
            user_email = movement.user.email if movement.user else "Unknown"
            writer.writerow([
                movement.date.strftime("%m/%d/%Y %H:%M"),
                movement.product.name,
                movement.movement_type,
                movement.quantity,
                user_email,
                movement.note
            ])
        return response
    
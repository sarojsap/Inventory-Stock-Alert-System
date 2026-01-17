from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, StockMovementViewSet, DashboardStatsView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'stocks', StockMovementViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/dashboard/', DashboardStatsView.as_view()),
]

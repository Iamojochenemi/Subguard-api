from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChargeViewSet, DashboardView, SubscriptionViewSet, AlertViewSet

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'charges', ChargeViewSet, basename='charge')
router.register(r'alerts', AlertViewSet, basename='alert')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
]

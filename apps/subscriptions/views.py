from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.db.models import Sum

from .models import Subscription, Charge, Alert
from .serializers import (
    SubscriptionSerializer,
    ChargeSerializer,
    AlertSerializer
)
from .services import assess_charge_risk

# 👇 IMPORT YOUR WRAPPER
from .utils import api_response


# ---------------- SUBSCRIPTIONS ---------------- #

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return api_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------------- CHARGES ---------------- #

class ChargeViewSet(viewsets.ModelViewSet):
    serializer_class = ChargeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Charge.objects.filter(subscription__user=self.request.user)

    def perform_create(self, serializer):
        subscription = serializer.validated_data["subscription"]

        if subscription.user != self.request.user:
            raise ValidationError("Invalid subscription ownership")

        charge = serializer.save(source="manual")

        risk_level, reason = assess_charge_risk(subscription, charge)

        Alert.objects.create(
            subscription=subscription,
            message=reason,
            severity=risk_level.lower()
        )


# ---------------- DASHBOARD ---------------- #

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        subscriptions = Subscription.objects.filter(user=user)

        results = []
        risk_counts = {"low": 0, "medium": 0, "high": 0}

        total_spend = Charge.objects.filter(
            subscription__user=user
        ).aggregate(total=Sum("amount"))["total"] or 0

        for sub in subscriptions:

            charges = Charge.objects.filter(
                subscription=sub
            ).order_by("-charge_date")

            alerts = Alert.objects.filter(subscription=sub)

            latest_charge = charges.first()

            if latest_charge:
                risk_level, risk_reason = assess_charge_risk(sub, latest_charge)
            else:
                risk_level, risk_reason = "LOW", "No charges yet"

            risk_counts[risk_level.lower()] += 1

            results.append({
                "subscription": {
                    "id": sub.id,
                    "name": sub.name,
                    "amount": str(sub.amount),
                    "currency": sub.currency,
                    "billing_cycle": sub.billing_cycle,
                    "next_billing_date": sub.next_billing_date,
                    "is_active": sub.is_active,
                },

                "latest_charge": {
                    "amount": str(latest_charge.amount) if latest_charge else None,
                    "date": latest_charge.charge_date if latest_charge else None,
                },

                "risk": {
                    "level": risk_level,
                    "reason": risk_reason,
                },

                "alerts_count": alerts.count(),
            })

        subscription_count = subscriptions.count()

        return api_response({
            "summary": {
                "total_subscriptions": subscription_count,
                "total_spend": str(total_spend),
                "active_subscriptions": subscriptions.filter(is_active=True).count(),
            },

            "insights": {
                "risk_distribution": risk_counts,
                "avg_spend_per_subscription": str(
                    total_spend / subscription_count
                    if subscription_count > 0 else 0
                ),
            },

            "subscriptions": results
        })


# ---------------- ALERTS ---------------- #

class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Alert.objects.filter(
            subscription__user=self.request.user
        ).order_by("-created_at")
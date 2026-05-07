from rest_framework import serializers
from .models import Subscription, Charge, Alert


class SubscriptionSerializer(serializers.ModelSerializer):
    is_due = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = [
            'id',
            'name',
            'amount',
            'currency',
            'billing_cycle',
            'next_billing_date',
            'is_due',
        ]

    def get_is_due(self, obj):
        from django.utils import timezone
        return obj.next_billing_date <= timezone.now().date()


class ChargeSerializer(serializers.ModelSerializer):
    subscription = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.none())

    class Meta:
        model = Charge
        fields = [
            'id',
            'subscription',
            'amount',
            'currency',
            'charge_date',
            'source',
        ]
        read_only_fields = ['source']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')

        if request and request.user.is_authenticated:
            self.fields['subscription'].queryset = Subscription.objects.filter(
                user=request.user
            )

    def validate_subscription(self, value):
        request = self.context.get('request')

        if not request or value.user != request.user:
            raise serializers.ValidationError("Invalid subscription")

        return value
    
from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    subscription_name = serializers.CharField(
        source="subscription.name",
        read_only=True
    )

    class Meta:
        model = Alert
        fields = [
            "id",
            "subscription",
            "subscription_name",
            "message",
            "severity",
            "created_at",
        ]
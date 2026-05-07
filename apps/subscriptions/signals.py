from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Charge, Alert
from .services import assess_charge_risk


@receiver(post_save, sender=Charge)
def analyze_charge(sender, instance, created, **kwargs):
    if not created:
        return

    subscription = instance.subscription

    risk_level, reason = assess_charge_risk(subscription, instance)

    Alert.objects.create(
        subscription=subscription,
        message=reason,
        severity=risk_level.lower()
    )
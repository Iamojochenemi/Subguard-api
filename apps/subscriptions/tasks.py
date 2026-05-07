from django.utils import timezone
from celery import shared_task
from datetime import timedelta

from .models import Subscription, Charge, Alert
from .services import assess_charge_risk, send_alert_email


@shared_task
def daily_subscription_check():
    subscriptions = Subscription.objects.filter(is_active=True)

    now_date = timezone.now().date()

    for sub in subscriptions:
        print("🔥 TASK IS RUNNING FOR:", sub.name)

        next_billing_date = sub.next_billing_date

        if not next_billing_date:
            continue

        is_due = next_billing_date <= now_date

        print(
            "DEBUG:",
            sub.name,
            "next_billing_date:", next_billing_date,
            "today:", now_date,
            "is_due:", is_due
        )

        # SKIP if not due
        if not is_due:
            continue

        # 🔒 Prevent duplicate charge for SAME billing date cycle
        already_charged_this_cycle = Charge.objects.filter(
            subscription=sub,
            charge_date=now_date,
            source="system"
        ).exists()

        if already_charged_this_cycle:
            continue

        # 💰 CREATE CHARGE
        Charge.objects.create(
            subscription=sub,
            amount=sub.amount,
            currency=sub.currency,
            charge_date=now_date,
            source="system"
        )

        # 🔁 ADVANCE BILLING DATE
        cycle = sub.billing_cycle.lower()

        if cycle == "daily":
            sub.next_billing_date = next_billing_date + timedelta(days=1)

        elif cycle == "weekly":
            sub.next_billing_date = next_billing_date + timedelta(days=7)

        elif cycle == "monthly":
            sub.next_billing_date = next_billing_date + timedelta(days=30)

        elif cycle == "yearly":
            sub.next_billing_date = next_billing_date + timedelta(days=365)

        sub.save()

        # 📊 RISK ANALYSIS
        latest_charge = Charge.objects.filter(
            subscription=sub
        ).order_by("-charge_date").first()

        risk_level, reason = assess_charge_risk(sub, latest_charge)

        # 🚨 ALERT + EMAIL (always triggered when charge happens)
        alert = Alert.objects.create(
            subscription=sub,
            message=reason,
            severity=risk_level.lower()
        )

        send_alert_email(sub, reason, risk_level)
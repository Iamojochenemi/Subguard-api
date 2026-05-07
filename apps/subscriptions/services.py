from decimal import Decimal
from django.db.models import Avg
from .models import Charge
from django.core.mail import send_mail
from django.conf import settings


def assess_charge_risk(subscription, charge):
    """
    Returns: (risk_level, reason)
    """

    expected = subscription.amount
    actual = charge.amount

    # prevent division issues
    if expected == 0:
        return "LOW", "Invalid expected amount"

    deviation = abs(actual - expected) / expected

    risk_level = "LOW"
    reason = "Normal charge"

    if deviation >= Decimal("1.0"):
        risk_level = "HIGH"
        reason = "Severe amount spike detected"

    elif deviation >= Decimal("0.5"):
        risk_level = "MEDIUM"
        reason = "Significant deviation from expected amount"

    elif deviation >= Decimal("0.2"):
        risk_level = "LOW"
        reason = "Minor variation detected"

    return risk_level, reason


def get_subscription_risk(subscription):
    """
    Centralized risk function (USED by Celery + Dashboard)
    """

    charges = Charge.objects.filter(subscription=subscription)

    latest_charge = charges.order_by("-charge_date").first()

    if not latest_charge:
        return "LOW", "No charges yet"

    return assess_charge_risk(subscription, latest_charge)


def get_subscription_risk_summary(subscription):
    """
    Aggregated historical risk based on average spending
    """

    charges = subscription.charges.all()

    if not charges.exists():
        return "LOW", "No charges yet"

    expected = subscription.amount
    avg_actual = charges.aggregate(avg=Avg("amount"))["avg"]

    if expected == 0:
        return "LOW", "Invalid expected amount"

    deviation = abs(avg_actual - expected) / expected

    risk_level = "LOW"
    reason = "Stable spending pattern"

    if deviation >= Decimal("1.0"):
        risk_level = "HIGH"
        reason = "Highly unstable spending pattern"

    elif deviation >= Decimal("0.5"):
        risk_level = "MEDIUM"
        reason = "Moderate spending variation"

    return risk_level, reason


def send_alert_email(subscription, message, severity):
    user = subscription.user

    subject = f"[SubGuard Alert] {subscription.name} - {severity.upper()} Risk"

    body = f"""
Hello {user.username},

We detected a {severity.upper()} risk on your subscription: {subscription.name}

Details:
{message}

SubGuard System
"""

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )




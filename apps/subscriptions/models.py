from django.db import models
from django.conf import settings


class Subscription(models.Model):
    BILLING_CYCLES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="NGN")
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CYCLES)
    next_billing_date = models.DateField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"


class Charge(models.Model):
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="charges"
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="NGN")
    charge_date = models.DateField()

    source = models.CharField(
        max_length=20,
        choices=[
            ("manual", "Manual Entry"),
            ("system", "System Generated"),
        ],
        default="manual"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subscription", "amount", "charge_date"],
                name="unique_charge_per_subscription_day"
            )
        ]
        ordering = ["-charge_date"]

    def __str__(self):
        return f"{self.subscription.name} - {self.amount}"


class Alert(models.Model):
    SEVERITY_LEVELS = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="alerts"
    )

    message = models.TextField()
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_LEVELS,
        default="medium"
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subscription.name} - {self.severity}"
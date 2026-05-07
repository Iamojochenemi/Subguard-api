class Alert(models.Model):
    SEVERITY_LEVELS = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, default="medium")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscription.name} - {self.severity}"
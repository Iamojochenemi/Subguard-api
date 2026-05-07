from django.contrib import admin
from .models import Subscription, Charge, Alert

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'amount', 'currency', 'billing_cycle', 'next_billing_date', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('billing_cycle', 'currency')

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'currency', 'charge_date', 'source', 'created_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subscription":
            kwargs["queryset"] = Subscription.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'severity', 'message', 'created_at')
    list_filter = ('severity',)
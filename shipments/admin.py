from django.contrib import admin

from .models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "world")
    readonly_fields = ("owner", "world", "name")
    search_fields = ("owner__username", "name", "world__postfix")

from django.contrib import admin

from .models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "world")
    readonly_fields = ("world", "name", "overviews")
    search_fields = ("owner__username", "name", "world__postfix")

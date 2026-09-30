# Copyright: (c) 2020-2026, Rafał Safin <rafal.safin@rafsaf.pl>
# GNU Affero General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/agpl-3.0.txt)

from django.urls import path

from shipments import views

app_name = "shipments"

urlpatterns = [
    path("my", views.my_shipments, name="my_shipments"),
    path("<int:pk>", views.shipment_send, name="shipment"),
    path("add", views.add_edit_shipment, name="add_shipment"),
    path("<int:pk>/edit", views.add_edit_shipment, name="edit_shipment"),
    path("<int:pk>/hide", views.shipment_hide, name="shipment_hide"),
    path("<int:pk>/delete", views.shipment_delete, name="shipment_delete"),
]

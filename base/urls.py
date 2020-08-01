from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    path("", views.base_view, name="base"),
    path("planer/", views.OutlineList.as_view(), name="planer"),
    path("planer/show-all", views.OutlineListShowAll.as_view(), name="planer_all"),
    path("planer/update", views.database_update, name="planer_update"),
    path("planer/create/", views.new_outline_create, name="planer_create"),
    path("planer/<int:_id>/status", views.inactive_outline, name="planer_status"),
    path(
        "planer/<int:_id>/results",
        views.outline_detail_results,
        name="planer_detail_results",
    ),
    path("planer/<int:_id>", views.outline_detail_1, name="planer_detail"),
    path(
        "planer/<int:_id>/initial-period-form",
        views.outline_detail_initial_period_form,
        name="planer_initial_form",
    ),
    path(
        "planer/<int:_id>/initial-period-outline",
        views.outline_detail_initial_period_outline,
        name="planer_initial",
    ),
    path(
        "planer/<int:_id>/initial-period-outline/<str:coord>",
        views.outline_detail_initial_period_outline_detail,
        name="planer_initial_detail",
    ),
    path(
        "planer/<int:_id>/get-deff",
        views.outline_detail_2_deff,
        name="planer_detail_get_deff",
    ),
    path(
        "planer/<int:_id>/create/select-tribe",
        views.new_outline_create_select,
        name="planer_create_select",
    ),
    path(
        "planer/<int:_id>/delete/ally-tags",
        views.outline_delete_ally_tags,
        name="planer_delete_ally_tags",
    ),
    path(
        "planer/<int:_id>/delete/enemy-tags",
        views.outline_delete_enemy_tags,
        name="planer_delete_enemy_tags",
    ),
    path(
        "planer/<int:_id>/disable_editable",
        views.outline_disable_editable,
        name="planer_disable_editable",
    ),
    path("planer/<int:pk>/delete", views.OutlineDelete.as_view(), name="planer_delete"),
    path("documentation", views.base_documentation, name="documentation"),
]

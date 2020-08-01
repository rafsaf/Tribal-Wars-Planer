from django.shortcuts import render, redirect
from django.http import Http404
from markdownx.utils import markdownify
from trbial_wars.database_update import cron_schedule_data_update
from base import models

def database_update(request):
    # ZMIENIC
    """ to update database manually, superuser required """
    if request.user.is_superuser:
        cron_schedule_data_update()
        return redirect("base:base")
    else:
        return Http404()


def base_view(request):
    """ base view """
    return render(request, "base/base.html")


def base_documentation(request):
    """ base documentation view"""
    doc = models.Documentation.objects.get(title="Doc").main_page
    doc = markdownify(doc)

    context = {"doc": doc}
    return render(request, "base/documentation.html", context)

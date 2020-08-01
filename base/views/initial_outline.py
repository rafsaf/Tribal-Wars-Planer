from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import trbial_wars.outline_initial as initial
from base import models, forms


@login_required
def outline_detail_initial_period_outline(request, _id):
    """ view with form for initial period outline """

    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)

    # User have to fill data or get redirected to outline_detail view
    # if instance.deff_troops == "":
    #    request.session["error"] = "Zbiórka Obrona pusta !"
    #    return redirect("base:planer_detail", _id)

    if instance.off_troops == "":
        request.session["error"] = "Zbiórka Wojsko pusta !"
        return redirect("base:planer_detail", _id)

    if "form1" in request.POST:
        request.session["pass-to-form"] = "True"
        return redirect("base:planer_initial_form", _id)

    target_query = models.TargetVertex.objects.all().filter(outline=instance)
    query = [
        models.WeightModel.objects.all().filter(target=target)
        for target in target_query
    ]

    query = zip(target_query, query)
    context = {"instance": instance, "query": query}
    return render(request, "base/new_outline/new_outline_initial_period2.html", context)


@login_required
def outline_detail_initial_period_form(request, _id):
    """ view with table with created outline, returned after valid filled form earlier """

    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)
    # User have to fill data or get redirected to outline_detail view
    # if instance.deff_troops == "":
    #    request.session["error"] = "Zbiórka Obrona pusta !"
    #    return redirect("base:planer_detail", _id)

    if instance.off_troops == "":
        request.session["error"] = "Zbiórka Wojsko pusta !"
        return redirect("base:planer_detail", _id)
    try:
        var = request.session["pass-to-form"]
        allowed_form = True
    except KeyError:
        allowed_form = False

    # always go to the next view after form confirmation OR if user want to
    if allowed_form == False and instance.initial_outline_targets != "":
        return redirect("base:planer_initial", _id)

    form1 = forms.InitialOutlineForm(request.POST or None, world=instance.world)
    # form2 = forms.InitialOutlinePlayerForm(request.POST or None)

    # form2.fields["player"].choices = [("banned", "--------")] + [
    #    ("{}".format(i.name), "{}".format(i.name))
    #    for i in models.Player.objects.all()
    #    .exclude(name__in=instance.initial_outline_players.split("\r\n"))
    #    .filter(world=instance.world)
    #    .filter(
    #        tribe_id__in=[
    #            tribe.tribe_id
    #            for tribe in models.Tribe.objects.all().filter(
    #                tag__in=instance.ally_tribe_tag.split(", ")
    #            )
    #        ]
    #    )
    # ]

    form1.fields["target"].initial = instance.initial_outline_targets

    if "form1" in request.POST:
        if form1.is_valid():
            player = request.POST.get("players")
            target = request.POST.get("target")
            max_distance = request.POST.get("max_distance")
            instance.initial_outline_players = player
            instance.initial_outline_targets = target
            instance.initial_outline_max_distance = max_distance
            instance.save()
            # make outline
            graph = initial.make_outline(instance)
            try:
                del request.session["pass-to-form"]
            except KeyError:
                pass
            return redirect("base:planer_initial", _id)

    # if "form2" in request.POST:
    #    if form2.is_valid():
    #        player = request.POST.get("player")
    #        # banned means "-------"
    #        if player == "banned":
    #            pass
    #        elif instance.initial_outline_players == "":
    #            instance.initial_outline_players = player
    #        else:
    #            instance.initial_outline_players += "\r\n{}".format(player)
    #        instance.save()
    #        return redirect("base:planer_initial_form", _id)

    context = {"instance": instance, "form1": form1}
    return render(request, "base/new_outline/new_outline_initial_period1.html", context)


@login_required
def outline_detail_initial_period_outline_detail(request, _id, coord):
    """ view with form for initial period outline detail """
    coordinates = coord[0:3] + "|" + str(coord[3:6])

    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)
    target_model = get_object_or_404(
        models.TargetVertex, outline=instance, target=coordinates
    )

    # User have to fill data or get redirected to outline_detail view
    # if instance.deff_troops == "":
    #    request.session["error"] = "Zbiórka Obrona pusta !"
    #    return redirect("base:planer_detail", _id)

    if instance.off_troops == "":
        request.session["error"] = "Zbiórka Wojsko pusta !"
        return redirect("base:planer_detail", _id)

    graph = initial.get_branch_graph(instance, target_model)
    target: initial.Vertex_Represent_Target_Village = graph.get_target_vertex(
        target_model.target
    )

    nonused_vertices = [
        i for i in target.connected_to_vertex_army if i not in target.result_lst
    ]

    # sort
    sort = request.GET.get("sort")
    if sort is None or sort == "distance":
        sort = "distance"
        sorting = "distance"
        rev = False
    elif sort == "distance-r":
        sorting = "distance"
        rev = True
    else:
        sorting = sort
        rev = True

    nonused_vertices.sort(key=lambda weight: getattr(weight, sorting), reverse=rev)
    # paginator
    paginator = Paginator(nonused_vertices, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    result_lst = models.WeightModel.objects.all().filter(target=target_model)
    # url
    url = (
        reverse("base:planer_initial_detail", args=[_id, coord])
        + f"?page={page_obj.number}&sort={sort}#table"
    )
    # form modal - update / duplicate
    form = forms.WeightForm(request.POST or None)
    if request.method == "POST":
        if "save" in request.POST:
            if form.is_valid():
                start = request.POST.get("start")
                off = request.POST.get("off")
                nobleman = request.POST.get("nobleman")
                order = request.POST.get("order")

                weight = models.WeightModel.objects.get(
                    target=target_model, start=start, order=order
                )

                state = weight.state

                other_off = state.off_state - weight.off
                other_snob = state.snob_state - weight.nobleman

                state.off_state = int(off) + other_off
                state.snob_state = int(nobleman) + other_snob
                state.save()

                weight.off = off
                weight.nobleman = nobleman
                weight.save()
                return redirect(url)

        # raczej zmienic caly ten syf nizej
        for weight in result_lst:
            # duplikowanie
            if f"{weight.start}-duplicate-{weight.order}" in request.POST:
                target.duplicate(order=weight.order)
                target.renew(target_model)

                return redirect(url)

            # usuwanie
            if f"{weight.start}-delete-{weight.order}" in request.POST:
                target.delete_element(
                    coord=weight.start, target_model=target_model, order=weight.order
                )
                target.renew(target_model)

                return redirect(url)

            # up
            if f"{weight.start}-up-{weight.order}" in request.POST:
                target.swap_up(weight.order)
                target.renew(target_model)

                return redirect(url)
            # down
            if f"{weight.start}-down-{weight.order}" in request.POST:
                target.swap_down(weight.order)
                target.renew(target_model)

                return redirect(url)

        for i in nonused_vertices:
            # add first
            if f"{i.start.coord}-add-first" in request.POST:
                target.add_first(coord=i.start.coord, target_model=target_model)
                target.renew(target_model)

                return redirect(url)
            # add last
            if f"{i.start.coord}-add-last" in request.POST:
                target.add_last(coord=i.start.coord, target_model=target_model)
                target.renew(target_model)

                return redirect(url)

    context = {
        "instance": instance,
        "target": target,
        "nonused": nonused_vertices,
        "result_lst": result_lst,
        "form": form,
        "page_obj": page_obj,
        "sort": sort,
    }
    return render(request, "base/new_outline/new_outline_initial_period3.html", context)

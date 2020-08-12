from itertools import zip_longest

from django.shortcuts import render, redirect
from django.db.models import Max, Min
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

import trbial_wars.outline_initial as initial
import trbial_wars.basic as basic
from base import models, forms


@login_required
def initial_planer(request, _id):
    """ view with form for initial period outline """
    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)
    if instance.written == 'inactive':
        return Http404()
    if request.method == 'POST':
        if "form1" in request.POST:
            instance.written = 'inactive'
            instance.save()
            return redirect("base:planer_initial_form", _id)
    instance.date = str(instance.date)

    target_query = models.TargetVertex.objects.select_related('outline_time').filter(outline=instance).order_by('id')
    target_context = {}
    for target in target_query:
        target_context[target] = list()

    for weight in (
        models.WeightModel.objects.select_related("target")
        .filter(target__in=target_query)
        .order_by("order")
    ):
        weight.distance = round(
            basic.Village(weight.start, validate=False).distance(
                basic.Village(weight.target.target, validate=False)
            ),
            1,
        )
        weight.off = f"{round(weight.off / 1000,1)}k"
        target_context[weight.target].append(weight)

    target_context = list(target_context.items())
    paginator = Paginator(target_context, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    mode = request.GET.get('mode')
    if mode is None or mode not in {'menu', 'time'}:
        mode = 'menu'

    context = {"instance": instance, "query": page_obj, 'mode': mode}




    
    if mode == 'time':
        outline_time_query = models.OutlineTime.objects.filter(outline=instance).order_by('id')
        time_period_context = {}
        for outline_time in outline_time_query:
            time_period_context[outline_time] = list()

        for time in models.PeriodModel.objects.select_related('outline_time').filter(outline_time__in=outline_time_query).order_by( 'from_time', '-unit'):
            time.from_time = str(time.from_time)
            time.to_time = str(time.to_time)
            time_period_context[time.outline_time].append(time)

        time_period_id_context = {}
        for i in time_period_context:
            time_period_id_context[i.id] = i

        choose_forms = formset_factory(form=forms.ChooseOutlineTimeForm, extra=12, max_num=12)
        choices = [(f'{time.id}', f'{i + 1}') for (i, time) in enumerate(time_period_context)]


        my_forms = formset_factory(form=forms.PeriodForm, formset=forms.BasePeriodFormSet, extra=6, min_num=2, max_num=6)

        if request.method == 'POST':
            if 'formset' in request.POST:
                my_forms = my_forms(request.POST)
                choose_forms = choose_forms()
                if my_forms.is_valid():
                    new_time = models.OutlineTime.objects.create(outline=instance)
                    create_list = []
                    for obj_dict in my_forms.cleaned_data:
                        if obj_dict == {}:
                            continue
                        obj_dict['outline_time'] = new_time
                        create_list.append(models.PeriodModel(**obj_dict))
                    models.PeriodModel.objects.bulk_create(create_list)
                    return redirect(reverse("base:planer_initial", args=[_id])+f'?page={page_obj.number}&mode={mode}')
            if 'choice-formset' in request.POST:
                choose_forms = choose_forms(request.POST)
                for form in choose_forms.forms:
                    form.fields['choice'].choices = choices
                my_forms = my_forms()
                if choose_forms.is_valid():
                    update_list = []
                    for data, tup in zip(choose_forms.cleaned_data, page_obj):
                        try:
                            index = int(data['choice'])
                        except KeyError:
                            continue
                        else:
                            outline_time = time_period_id_context[index]


                        if tup[0].outline_time != outline_time:
                            tup[0].outline_time = outline_time
                            update_list.append(tup[0])
                    models.TargetVertex.objects.bulk_update(update_list,['outline_time'])
                            
                
        else:
            my_forms = my_forms()
            choose_forms = choose_forms()

        
        for form in choose_forms.forms:
            form.fields['choice'].choices = choices

        choice_form_list = [form for form in choose_forms.forms]

        for target, _ in page_obj:
            for p_key, number in choices:
                try:
                    statement = bool(target.outline_time.id == int(p_key))
                except AttributeError:
                    continue
                else:
                    if statement:
                        target.value = number

        query2 = zip(page_obj, choice_form_list)
        try:
            error = request.session['outline_error']
        except KeyError:
            error = None
        else:
            del request.session['outline_error']
        finally:
            context['error'] = error

        context['outline_time'] = time_period_context
        context['formset'] = my_forms
        context['choice_formset'] = choose_forms
        context['query2'] = query2
    
    return render(request, "base/new_outline/new_outline_initial_period2.html", context)


@login_required
def initial_form(request, _id):
    """ view with table with created outline, returned after valid filled form earlier """
    instance = get_object_or_404(models.Outline, id=_id, owner=request.user)
    if instance.written == 'active':
        return redirect("base:planer_initial", _id)

    form1 = forms.InitialOutlineForm(request.POST or None, world=instance.world)
    form1.fields["target"].initial = instance.initial_outline_targets

    if "form1" in request.POST:
        if form1.is_valid():
            target = request.POST.get("target")
            instance.initial_outline_targets = target
            instance.save()
            # make outline
            try:
                initial.make_outline(instance)
            except KeyError:
                request.session[
                    "error"
                ] = "Wygląda na to, że Twoja Zbiórka Wojska nie jest już aktualna! Aby skorzystać z planera: skopiuj dane z podglądu i popraw błędy lub wklej aktualne dane o wojsku \n"
                return redirect("base:planer_detail", _id)
            instance.written = 'active'
            instance.save()
            return redirect("base:planer_initial", _id)

    context = {"instance": instance, "form1": form1}
    return render(request, "base/new_outline/new_outline_initial_period1.html", context)


@login_required
def initial_target(request, id1, id2):
    """ view with form for initial period outline detail """
    instance = get_object_or_404(models.Outline, id=id1, owner=request.user)
    if instance.written == 'inactive':
        return Http404()

    target = get_object_or_404(models.TargetVertex, pk=id2)
    nonused_vertices = models.WeightMaximum.objects.filter(outline=instance).exclude(off_left=0, nobleman_left=0)
    result_lst = models.WeightModel.objects.filter(target=target).order_by("order")
    for weight in result_lst:
        weight.distance = round(weight.distance, 1)
    ## sort
    sort = request.GET.get("sort")
    if sort is None:
        sort = "-off_left"
    if sort == "distance":
        nonused_vertices = list(nonused_vertices)
        for weight in nonused_vertices:
            weight.distance = round(basic.dist(weight.start, target.target), 1)
        nonused_vertices.sort(key=lambda weight: weight.distance)
        paginator = Paginator(nonused_vertices, 16)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    elif sort == "-distance":
        nonused_vertices = list(nonused_vertices)
        for weight in nonused_vertices:
            weight.distance = round(basic.dist(weight.start, target.target), 1)
        nonused_vertices.sort(key=lambda weight: weight.distance, reverse=True)
        paginator = Paginator(nonused_vertices, 16)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        if sort in {"-off_left", "-nobleman_left"}:
            nonused_vertices = nonused_vertices.order_by(sort)
        else:
            nonused_vertices = nonused_vertices.order_by("-off_left")
        paginator = Paginator(nonused_vertices, 16)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        for weight in page_obj:
            weight.distance = round(basic.dist(weight.start, target.target), 1)

    ## forms
    if request.method == "POST":
        if "form" in request.POST:
            form = forms.WeightForm(request.POST)
            if form.is_valid():
                weight_id = request.POST.get("weight_id")
                off = int(request.POST.get("off"))
                nobleman = int(request.POST.get("nobleman"))

                weight = models.WeightModel.objects.select_related("state").filter(
                    id=weight_id
                )[0]
                state = weight.state

                if off > weight.off:
                    state.off_max += off - weight.off

                if nobleman > weight.nobleman:
                    state.nobleman_max += nobleman - weight.nobleman

                state.off_state = state.off_state - weight.off + off
                state.nobleman_state = state.nobleman_state - weight.nobleman + nobleman

                state.off_left = state.off_max - state.off_state
                state.nobleman_left = state.nobleman_max - state.nobleman_state

                weight.off = off
                weight.nobleman = nobleman

                weight.save()
                state.save()
                return redirect(
                    reverse("base:planer_initial_detail", args=[id1, id2])
                    + f"?page={page_number}&sort={sort}"
                )
        else:
            form = forms.WeightForm(None)

    else:
        form = forms.WeightForm(None)

    try:
        paint = int(request.session['weight'])
        del[request.session['weight']]
    except KeyError:
        paint = None

    context = {
        "instance": instance,
        "target": target,
        "result_lst": result_lst,
        "form": form,
        "page_obj": page_obj,
        "sort": sort,
        'paint': paint,
    }
    return render(request, "base/new_outline/new_outline_initial_period3.html", context)


@login_required
def initial_add_first(request, id1, id2, id3):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        target = get_object_or_404(models.TargetVertex, pk=id2)
        weight = get_object_or_404(models.WeightMaximum, pk=id3)
        if not models.WeightModel.objects.filter(target=target).exists():
            order = 0
        else:
            order = (
                models.WeightModel.objects.filter(target=target).aggregate(
                    Min("order")
                )["order__min"]
                - 1
            )
        models.WeightModel.objects.create(
            target=target,
            player=weight.player,
            start=weight.start,
            state=weight,
            off=weight.off_left,
            nobleman=weight.nobleman_left,
            order=order,
            distance=round(
                basic.Village(target.target).distance(basic.Village(weight.start)), 1
            ),
        )
        weight.off_state += weight.off_left
        weight.off_left = 0
        weight.nobleman_state += weight.nobleman_left
        weight.nobleman_left = 0
        weight.save()
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


class InitialDeleteTime(LoginRequiredMixin, DeleteView):
    model = models.OutlineTime
    def get_success_url(self):
        outline = self.object.outline
        mode = self.request.GET.get('mode')
        page = self.request.GET.get('page')
        return reverse('base:planer_initial', args=[outline.id])+f'?page={page}&mode={mode}'


@login_required
def initial_add_last(request, id1, id2, id3):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        target = get_object_or_404(models.TargetVertex, pk=id2)
        weight = get_object_or_404(models.WeightMaximum, pk=id3)
        if not models.WeightModel.objects.filter(target=target).exists():
            order = 0
        else:
            order = (
                models.WeightModel.objects.filter(target=target).aggregate(
                    Max("order")
                )["order__max"]
                + 1
            )
        models.WeightModel.objects.create(
            target=target,
            player=weight.player,
            start=weight.start,
            state=weight,
            off=weight.off_left,
            nobleman=weight.nobleman_left,
            order=order,
            distance=round(
                basic.Village(target.target).distance(basic.Village(weight.start)), 1
            ),
        )
        weight.off_state += weight.off_left
        weight.off_left = 0
        weight.nobleman_state += weight.nobleman_left
        weight.nobleman_left = 0
        weight.save()
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()

@login_required
def initial_move_down(request, id1, id2, id4):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight_model = models.WeightModel.objects.get(pk=id4)
        target = get_object_or_404(models.TargetVertex, pk=id2)
        order1 = weight_model.order

        next_weight = (
            models.WeightModel.objects.filter(order__gt=order1)
            .filter(target=target)
            .order_by("order")
            .first()
        )
        
        if next_weight is not None:
            weight_model.order = next_weight.order
            weight_model.save()
            next_weight.order = order1
            next_weight.save()
        request.session['weight'] = weight_model.id
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()

@login_required
def initial_move_up(request, id1, id2, id4):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight_model = models.WeightModel.objects.get(pk=id4)
        target = get_object_or_404(models.TargetVertex, pk=id2)
        order1 = weight_model.order

        next_weight = (
            models.WeightModel.objects.filter(order__lt=order1)
            .filter(target=target)
            .order_by("-order")
            .first()
        )
        
        if next_weight is not None:
            weight_model.order = next_weight.order
            weight_model.save()
            next_weight.order = order1
            next_weight.save()
        request.session['weight'] = weight_model.id
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()

@login_required
def initial_weight_delete(request, id1, id2, id4):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight_model = models.WeightModel.objects.select_related("state").filter(
            pk=id4
        )[0]
        weight_model.state.off_left += weight_model.off
        weight_model.state.off_state -= weight_model.off
        weight_model.state.nobleman_left += weight_model.nobleman
        weight_model.state.nobleman_state -= weight_model.nobleman
        weight_model.state.save()
        weight_model.delete()

        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


@login_required
def initial_divide(request, id1, id2, id4, n):
    if request.method == "POST":
        outline = models.Outline.objects.get(id=id1)
        if not request.user == outline.owner:
            return Http404()
        sort = request.GET.get("sort")
        page = request.GET.get("page")
        weight = models.WeightModel.objects.select_related("state").filter(
            pk=id4
        )[0]
        n_list = [i + 1 for i in range(n -1)]
        nob_list = [i for i in range(max(weight.nobleman - 1,0))]
        if n > weight.nobleman:
            zipped_list = zip_longest(n_list, nob_list)
            nob_number = max(weight.nobleman - 1, 0)
        else:
            zipped_list = zip(n_list, nob_list)
            nob_number = n - 1


        off = weight.off // n
        rest = weight.off - off * n
        update_list = []
        create_list = []
        for number, nob in zipped_list:
            if nob is None:
                nob = 0
            else:
                nob = 1

            create_list.append(models.WeightModel(
                target=weight.target,
                player=weight.player,
                start=weight.start,
                state=weight.state,
                off=off,
                nobleman=nob,
                order=weight.order + number,
                distance=weight.distance
            ))
        weight.off = off + rest
        weight.nobleman = weight.nobleman - nob_number
        weight.save()

        for next_weight in models.WeightModel.objects.filter(target=weight.target, order__gt=weight.order):
            next_weight.order = next_weight.order + n
            update_list.append(next_weight)
        
        models.WeightModel.objects.bulk_create(create_list)
        models.WeightModel.objects.bulk_update(update_list, ['order'])

        
        
        return redirect(
            reverse("base:planer_initial_detail", args=[id1, id2])
            + f"?page={page}&sort={sort}"
        )
    return Http404()


@login_required
def create_final_outline(request, id1):
    instance = get_object_or_404(models.Outline, id=id1, owner=request.user)
    target_with_no_time = models.TargetVertex.objects.filter(outline=instance).filter(outline_time=None).exists()
    if target_with_no_time:
        request.session['outline_error'] = "Wszystkie cele muszą mieć ustawiony Czas."
        return redirect(reverse('base:planer_initial', args=[id1])+'?page=1&mode=time')
    initial.make_final_outline(instance)
    return redirect('base:planer_detail_results', id1)
    


    #do stuff
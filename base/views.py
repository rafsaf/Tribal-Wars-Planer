
""" views.py """



from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.http import require_POST

from markdownx.utils import markdownify
from plemiona_pliki.cron import cron_schedule_data_update
from plemiona_pliki.get_deff import get_deff
from . import models, forms



class OutlineList(LoginRequiredMixin, ListView):
    """ login required view /planer """
    template_name = 'base/base_planer.html'

    def get_queryset(self):
        return User.objects.get(
            username=self.request.user.username).new_outline_set.all().filter(
                status='active')


class OutlineListShowAll(LoginRequiredMixin, ListView):
    """ login required view which shows hidden instances /planer/show_all """
    template_name = 'base/base_planer.html'


    def get_queryset(self):
        return User.objects.get(
            username=self.request.user.username).new_outline_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_all'] = True
        return context


@login_required
@require_POST
def inactive_outline(request, _id):
    """ class based view makeing outline with id=id inavtive/active, post and login required """

    outline = get_object_or_404(models.New_Outline, id=_id, owner=request.user)
    if outline.status == 'active':
        outline.status = 'inactive'
        outline.save()
        return redirect('base:planer')
    else:
        outline.status = 'active'
        outline.save()
        return redirect('base:planer_all')


class OutlineDelete(LoginRequiredMixin, DeleteView):
    """ class based view to delete outline login required"""
    def get_queryset(self):
        return User.objects.get(
            username=self.request.user.username).new_outline_set.all()

    def get_success_url(self):
        return reverse('base:planer')


class WorldList(ListView):
    """ class based view to show all worlds """
    model = models.World
    template_name = 'base/world/world.html'


def base_view(request):
    """ base view """
    return render(request, 'base/base.html')


def base_documentation(request):
    """ base documentation view"""
    doc = models.Documentation.objects.get(title="Doc").main_page
    doc = markdownify(doc)
    print(doc)
    context = {"doc": doc}
    return render(request, 'base/documentation.html', context)


@login_required
def new_outline_create_select(request, _id):
    """ select user's ally and enemy tribe after creating outline, login required """

    instance = get_object_or_404(models.New_Outline,
                                 pk=_id,
                                 owner=request.user)

    form1 = forms.Moje_plemie_skrot_Form(request.POST or None)
    form1.fields['plemie1'].choices = [("banned","--------")]+[
        ("{}".format(i.tag), "{}".format(i.tag))
        for i in models.Tribe.objects.all().filter(
            world=instance.swiat).exclude(
                tag__in=instance.moje_plemie_skrot.split(', ')).exclude(
                    tag__in=instance.przeciwne_plemie_skrot.split(', '))
    ]

    form2 = forms.Przeciwne_plemie_skrot_Form(request.POST or None)
    form2.fields['plemie2'].choices = [("banned","--------")]+[
        ("{}".format(i.tag), "{}".format(i.tag))
        for i in models.Tribe.objects.all().filter(
            world=instance.swiat).exclude(
                tag__in=instance.przeciwne_plemie_skrot.split(', ')).exclude(
                    tag__in=instance.moje_plemie_skrot.split(', '))
    ]

    if 'form-1' in request.POST:

        if form1.is_valid():
            plemie = request.POST.get('plemie1')
            if instance.moje_plemie_skrot == '':
                instance.moje_plemie_skrot = plemie
            else:
                instance.moje_plemie_skrot += str(', ' + plemie)
            instance.save()
            return redirect('base:planer_create_select', _id)
    if 'form-2' in request.POST:
        if form2.is_valid():
            plemie = request.POST.get('plemie2')
            if instance.przeciwne_plemie_skrot == '':
                instance.przeciwne_plemie_skrot = plemie
            else:
                instance.przeciwne_plemie_skrot += str(', ' + plemie)
            instance.save()
            return redirect('base:planer_create_select', _id)

    context = {
        'form1': form1,
        'form2': form2,
    }
    return render(request, 'base/new_outline/new_outline_create_select.html',
                  context)


@login_required
def new_outline_create(request):
    """ creates new user's outline login required """
    form1 = forms.New_Outline_Form(request.POST or None)
    form1.fields['swiat'].choices = [("{}".format(i.world),
                                      "{}".format(i.world))
                                     for i in models.World.objects.all()]

    if form1.is_valid():
        user_ = get_object_or_404(User, username=request.user.username)

        new_instance = models.New_Outline(
            owner=user_,
            data_akcji=request.POST['data_akcji'],
            nazwa=request.POST['nazwa'],
            swiat=request.POST['swiat'],
        )

        new_instance.save()
        results = models.Results(outline=new_instance)
        results.save()
        return render(request, 'base/new_outline/new_outline_create.html', {
            'created': True,
            'id': new_instance.id
        })

    context = {"form1": form1}

    return render(request, 'base/new_outline/new_outline_create.html', context)


def database_update(request):
    # ZMIENIC
    """ to update database manually, superuser required """
    if request.user.is_superuser:
        cron_schedule_data_update()
        return redirect('base:base')
    else:
        return Http404()


@login_required
def outline_detail_1(request, _id):
    """details user's outline , login required"""
    

    instance = get_object_or_404(models.New_Outline, id=_id, owner=request.user)

    form1 = forms.Wojsko_Outline_Form(request.POST or None)
    form2 = forms.Obrona_Outline_Form(request.POST or None)

    if 'form-1' in request.POST:
        if form1.is_valid():
            instance.zbiorka_wojsko = request.POST.get('zbiorka_wojsko')
            instance.save()

            return redirect('base:planer_detail', _id)

    if 'form-2' in request.POST:
        if form2.is_valid():
            instance.zbiorka_obrona = request.POST.get('zbiorka_obrona')
            instance.save()
            
            return redirect('base:planer_detail', _id)
    context = {'instance': instance, 'form1': form1, 'form2': form2}

    error = request.session.get('error')
    if not error is None:
        context['error'] = error
        del request.session['error']
    return render(request, 'base/new_outline/new_outline.html', context)

@login_required
def outline_detail_2_deff(request, _id):
    """ details user outline, get deff page """
    instance = get_object_or_404(models.New_Outline, id=_id, owner=request.user)
    results = get_object_or_404(models.Results, pk=instance)

    # only correct zbiorka_obrona allowed
    if instance.zbiorka_obrona == "":
        request.session['error'] = "Zbiórka Obrona pusta !"
        return redirect('base:planer_detail', _id)

    form = forms.Get_Deff_Form(request.POST or None, world=instance.swiat)
    print([form.errors])
    if 'form' in request.POST:
        if form.is_valid():
            radius = request.POST.get('radius')
            excluded = request.POST.get('excluded')

            results.results_get_deff = get_deff(instance,int(radius),excluded)
            results.save()

            return redirect('base:planer_detail_get_deff', _id)

            
    

    context = {'instance': instance, 'form':form}

    return render(request, 'base/new_outline/new_outline_get_deff.html', context)



def outline_detail_results(request, _id):
    """ view for results """

    instance = get_object_or_404(models.New_Outline, id=_id, owner=request.user)
    context = {'instance': instance}

    return render(request, 'base/new_outline/new_outline_results.html', context)


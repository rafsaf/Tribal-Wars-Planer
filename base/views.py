from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse
from . import models, forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from plemiona_pliki.cron import cron_schedule_data_update
from django.http import Http404
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

class OutlineList(LoginRequiredMixin, ListView):
    template_name = 'base/base_planer.html'

    def get_queryset(self):
        return User.objects.get(username=self.request.user.username).new_outline_set.all().filter(status='active')

class OutlineListShowAll(LoginRequiredMixin, ListView):
    template_name = 'base/base_planer.html'

    def get_queryset(self):
        return User.objects.get(username=self.request.user.username).new_outline_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_all'] = True
        return context

@login_required
@require_POST
def inactive_outline(request, id):

    outline = get_object_or_404(models.New_Outline, id=id, owner=request.user)
    if outline.status == 'active':
        outline.status = 'inactive'
        outline.save()
        return redirect('base:planer')
    else:
        outline.status = 'active'
        outline.save()
        return redirect('base:planer_all')



class OutlineDelete(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        return User.objects.get(username=self.request.user.username).new_outline_set.all()

    def get_success_url(self):
        return reverse('base:planer')


class WorldList(ListView):
    model = models.World
    template_name = 'base/world/world.html'


def base_view(request):
    return render(request, 'base/base.html')

def base_documentation(request):
    return render(request, 'base/documentation.html')


@login_required
def new_outline_create_select(request, id):

    instance = get_object_or_404(models.New_Outline, pk=id, owner=request.user)

    form1 = forms.Moje_plemie_skrot_Form(request.POST or None)
    form1.fields['plemie'].choices = [
        ("{}".format(i.tag), "{}".format(i.tag)) for i in models.Tribe.objects.all().filter(world=instance.swiat).exclude(tag__in=instance.moje_plemie_skrot.split(', ')).exclude(tag__in=instance.przeciwne_plemie_skrot.split(', '))
    ]


    form2 = forms.Przeciwne_plemie_skrot_Form(request.POST or None)
    form2.fields['plemie'].choices = [
        ("{}".format(i.tag), "{}".format(i.tag)) for i in models.Tribe.objects.all().filter(world=instance.swiat).exclude(tag__in=instance.przeciwne_plemie_skrot.split(', ')).exclude(tag__in=instance.moje_plemie_skrot.split(', '))
    ]


    if 'form-1' in request.POST:

        if form1.is_valid():
            plemie = request.POST.get('plemie')
            if instance.moje_plemie_skrot == '':
                instance.moje_plemie_skrot = plemie
            else:
                instance.moje_plemie_skrot += str(', ' + plemie)
            instance.save()
            return redirect('base:planer_create_select', id)
    if 'form-2' in request.POST:
        if form2.is_valid():
            plemie = request.POST.get('plemie')
            if instance.przeciwne_plemie_skrot == '':
                instance.przeciwne_plemie_skrot = plemie
            else:
                instance.przeciwne_plemie_skrot += str(', ' + plemie)
            instance.save()
            return redirect('base:planer_create_select', id)

    context = {
        'form1': form1,
        'form2': form2,
    }
    return render(request, 'base/new_outline/new_outline_create_select.html', context)

@login_required
def new_outline_create(request):
    form1 = forms.New_Outline_Form(request.POST or None)
    form1.fields['swiat'].choices = [("{}".format(i.world), "{}".format(i.world)) for i in models.World.objects.all()]

    if form1.is_valid():
        user_ = get_object_or_404(User, username=request.user.username)


        new_instance = models.New_Outline(
            owner=user_,
            data_akcji=request.POST['data_akcji'],
            nazwa=request.POST['nazwa'],
            swiat=request.POST['swiat'],
        )

        new_instance.save()


        return render(request, 'base/new_outline/new_outline_create.html', {'created': True, 'id': new_instance.id})

    context = {"form1": form1}

    return render(request,  'base/new_outline/new_outline_create.html', context)



def database_update(request):
    if request.user.is_superuser:
        cron_schedule_data_update()
        return redirect('base:base')
    else:
        return Http404()






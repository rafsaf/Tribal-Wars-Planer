""" Database models """
import datetime
from math import sqrt
from typing import Dict, List, Optional, Union

import django
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count, F, Q, Sum
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy
from markdownx.models import MarkdownxField

from .message import Message
from .outline import Outline, building_default_list
from .player import Player
from .profile import Profile
from .server import Server
from .stats import Stats
from .tribe import Tribe
from .village_model import VillageModel
from .world import World


class Result(models.Model):
    """Presents Outline and Deff results"""

    outline = models.OneToOneField(Outline, on_delete=models.CASCADE, primary_key=True)
    results_get_deff = models.TextField(default="")
    results_outline = models.TextField(default="")
    results_players = models.TextField(default="")
    results_sum_up = models.TextField(default="")
    results_export = models.TextField(default="")

    def __str__(self):
        return self.outline.name + " results"


class Documentation(models.Model):
    """Docs page"""

    title = models.CharField(max_length=30)
    main_page = MarkdownxField()
    language = models.CharField(max_length=2, default="pl")

    def __str__(self):
        return f"{self.title}_{self.language}"

    class Meta:
        ordering = (
            "-language",
            "title",
        )


class WeightMaximum(models.Model):
    """Control state smaller than maximum"""

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE, db_index=True)
    start = models.CharField(max_length=7, db_index=True)
    x_coord = models.IntegerField(default=0)
    y_coord = models.IntegerField(default=0)
    player = models.CharField(max_length=30)

    off_max = models.IntegerField()
    off_state = models.IntegerField(default=0)
    off_left = models.IntegerField()

    nobleman_max = models.IntegerField()
    nobleman_state = models.IntegerField(default=0)
    nobleman_left = models.IntegerField()

    catapult_max = models.IntegerField(default=0)
    catapult_state = models.IntegerField(default=0)
    catapult_left = models.IntegerField(default=0)

    hidden = models.BooleanField(default=False)
    first_line = models.BooleanField(default=False)
    too_far_away = models.BooleanField(default=False)
    fake_limit = models.IntegerField(
        default=4, validators=[MinValueValidator(0), MaxValueValidator(20)]
    )

    def __str__(self):
        return self.start

    def coord_tuple(self):
        return (int(self.start[0:3]), int(self.start[4:7]))


class OutlineTime(models.Model):
    """Handle Time for Target"""

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)


class PeriodModel(models.Model):
    """Handle one period of time in outline specification"""

    STATUS = [
        ("all", gettext_lazy("All")),
        ("random", gettext_lazy("Random")),
        ("exact", gettext_lazy("Exact")),
    ]
    UNITS = [
        ("noble", gettext_lazy("Noble")),
        ("ram", gettext_lazy("Ram")),
    ]
    outline_time = models.ForeignKey(OutlineTime, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS)
    unit = models.CharField(max_length=15, choices=UNITS)
    from_number = models.IntegerField(null=True, default=None, blank=True)
    to_number = models.IntegerField(null=True, default=None, blank=True)
    from_time = models.TimeField(default=datetime.time(hour=7))
    to_time = models.TimeField(default=datetime.time(hour=7))


class TargetVertex(models.Model):
    """Target Village"""

    MODE_OFF = [
        ("closest", gettext_lazy("Closest Front")),
        ("close", gettext_lazy("Close Back")),
        ("random", gettext_lazy("Random Back")),
        ("far", gettext_lazy("Far Back")),
    ]

    MODE_NOBLE = [
        ("closest", gettext_lazy("Closest Front")),
        ("close", gettext_lazy("Close Back")),
        ("random", gettext_lazy("Random Back")),
        ("far", gettext_lazy("Far Back")),
    ]

    MODE_DIVISION = [
        ("divide", gettext_lazy("Divide off with nobles")),
        ("not_divide", gettext_lazy("Dont't divide off")),
        ("separatly", gettext_lazy("Off and nobles separatly")),
    ]

    NOBLE_GUIDELINES = [
        ("one", gettext_lazy("Try send all nobles to one target")),
        ("many", gettext_lazy("Nobles to one or many targets")),
        ("single", gettext_lazy("Try single nobles from many villages")),
    ]

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE, db_index=True)
    outline_time = models.ForeignKey(
        OutlineTime, on_delete=models.SET_NULL, null=True, default=None
    )
    target = models.CharField(max_length=7, db_index=True)
    player = models.CharField(max_length=30)
    fake = models.BooleanField(default=False)
    ruin = models.BooleanField(default=False)

    required_off = models.IntegerField(default=0)
    required_noble = models.IntegerField(default=0)

    exact_off = ArrayField(models.IntegerField(), default=list, size=4)
    exact_noble = ArrayField(models.IntegerField(), default=list, size=4)

    mode_off = models.CharField(max_length=15, choices=MODE_OFF, default="random")
    mode_noble = models.CharField(max_length=15, choices=MODE_NOBLE, default="closest")
    mode_division = models.CharField(
        max_length=15, choices=MODE_DIVISION, default="not_divide"
    )
    mode_guide = models.CharField(
        max_length=15, choices=NOBLE_GUIDELINES, default="one"
    )
    night_bonus = models.BooleanField(default=False)
    enter_t1 = models.IntegerField(default=7)
    enter_t2 = models.IntegerField(default=12)

    def __str__(self):
        return self.target

    def get_absolute_url(self):
        return reverse("base:planer_initial_detail", args=[self.outline.pk, self.pk])

    def coord_tuple(self):
        return (int(self.target[0:3]), int(self.target[4:7]))


class WeightModel(models.Model):
    """Command between start and target"""

    BUILDINGS = [
        ("headquarters", gettext_lazy("Headquarters")),
        ("barracks", gettext_lazy("Barracks")),
        ("stable", gettext_lazy("Stable")),
        ("workshop", gettext_lazy("Workshop")),
        ("academy", gettext_lazy("Academy")),
        ("smithy", gettext_lazy("Smithy")),
        ("rally_point", gettext_lazy("Rally point")),
        ("statue", gettext_lazy("Statue")),
        ("market", gettext_lazy("Market")),
        ("timber_camp", gettext_lazy("Timber camp")),
        ("clay_pit", gettext_lazy("Clay pit")),
        ("iron_mine", gettext_lazy("Iron mine")),
        ("farm", gettext_lazy("Farm")),
        ("warehouse", gettext_lazy("Warehouse")),
        ("wall", gettext_lazy("wall")),
    ]

    target = models.ForeignKey(TargetVertex, on_delete=models.CASCADE, db_index=True)
    state = models.ForeignKey(WeightMaximum, on_delete=models.CASCADE)
    start = models.CharField(max_length=7)
    off = models.IntegerField()
    distance = models.FloatField()
    nobleman = models.IntegerField()
    catapult = models.IntegerField(default=0)
    ruin = models.BooleanField(default=False)
    building = models.CharField(
        default=None, max_length=50, choices=BUILDINGS, null=True, blank=True
    )
    order = models.IntegerField()
    player = models.CharField(max_length=40)
    first_line = models.BooleanField(default=False)
    t1 = models.TimeField(null=True, blank=True, default=None)
    t2 = models.TimeField(null=True, blank=True, default=None)

    def __str__(self):
        return self.start

    def distance_to_village(self, coord: str) -> float:
        return sqrt(
            (int(self.start[0:3]) - int(coord[0:3])) ** 2
            + (int(self.start[4:7]) - int(coord[4:7])) ** 2
        )


class OutlineOverview(models.Model):
    outline = models.ForeignKey(
        Outline, on_delete=models.SET_NULL, null=True, blank=True
    )
    weights_json = models.TextField(default="", blank=True)
    targets_json = models.TextField(default="", blank=True)


class Overview(models.Model):
    """Present results for tribe members using unique urls"""

    outline_overview = models.ForeignKey(OutlineOverview, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, primary_key=True, db_index=True)
    outline = models.ForeignKey(
        Outline, on_delete=models.SET_NULL, null=True, blank=True
    )
    player = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    table = models.TextField()
    string = models.TextField()
    extended = models.TextField(default="")
    deputy = models.TextField(default="")
    show_hidden = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def get_absolute_url(self):
        return reverse("base:overview", args=[self.token])

    def extend_with_encodeURIComponent(
        self, instance: Outline, request: HttpRequest
    ) -> None:
        from utils.basic import encode_component

        setattr(self, "to", encode_component(self.player))

        message: str = f"[b]{self.player}[/b]\n\n"
        f2 = f"[url]{request.scheme}://{request.get_host()}{self.get_absolute_url()}[/url]\n\n"

        if instance.sending_option == "string":
            message += instance.text_message + self.string
        elif instance.sending_option == "extended":
            message += instance.text_message + self.extended
        elif instance.sending_option == "deputy":
            message += instance.text_message + self.deputy
        else:
            message += f2 + instance.text_message

        setattr(
            self,
            "message",
            encode_component(message.replace("[size=12]", "").replace("[/size]", "")),
        )


class TargetVertexOverview(models.Model):
    """Copied Target Village"""

    outline_overview = models.ForeignKey(OutlineOverview, on_delete=models.CASCADE)
    target = models.CharField(max_length=7)
    player = models.CharField(max_length=30)
    fake = models.BooleanField(default=False)
    target_vertex = models.ForeignKey(
        TargetVertex, on_delete=models.SET_NULL, null=True, default=None, blank=True
    )

    def __str__(self):
        return self.target


class WeightModelOverview(models.Model):
    """Copied Command between start and target"""

    target = models.ForeignKey(TargetVertexOverview, on_delete=models.CASCADE)
    start = models.CharField(max_length=7)
    off = models.IntegerField()
    distance = models.FloatField()
    nobleman = models.IntegerField()
    order = models.IntegerField()
    player = models.CharField(max_length=40)
    t1 = models.TimeField(default=datetime.time(hour=0, minute=0, second=0))
    t2 = models.TimeField(default=datetime.time(hour=0, minute=0, second=0))

    def __str__(self):
        return self.start


class Payment(models.Model):
    """Represents real payment, only superuser access"""

    STATUS = [
        ("finished", gettext_lazy("Finished")),
        ("returned", gettext_lazy("Returned")),
    ]
    status = models.CharField(max_length=30, choices=STATUS, default="finished")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    send_mail = models.BooleanField(default=True)
    amount = models.FloatField()
    event_id = models.CharField(max_length=300, null=True, default=None, blank=True)
    from_stripe = models.BooleanField(default=False)
    payment_date = models.DateField()
    months = models.IntegerField(default=1)
    comment = models.CharField(max_length=150, default="", blank=True)
    new_date = models.DateField(default=None, null=True, blank=True)

    def value(self) -> str:
        return f"{self.amount} PLN"


@receiver(post_save, sender=Payment)
def handle_payment(sender, instance: Payment, created: bool, **kwargs) -> None:
    if created:
        user: User = instance.user
        user_profile: Profile = Profile.objects.get(user=user)

        current_date: datetime.date = timezone.localdate()
        relative_months: relativedelta = relativedelta(months=instance.months)
        day: relativedelta = relativedelta(days=1)
        if user_profile.validity_date is None:
            user_profile.validity_date = current_date + relative_months + day
        elif user_profile.validity_date <= current_date:
            user_profile.validity_date = current_date + relative_months + day
        else:
            user_profile.validity_date = (
                user_profile.validity_date + relative_months + day
            )

        if instance.send_mail:
            msg_html = render_to_string(
                "email_payment.html",
                {
                    "amount": instance.amount,
                    "payment_date": instance.payment_date,
                    "new_date": instance.new_date,
                    "user": instance.user,
                },
            )
            send_mail(
                "plemiona-planer.pl",
                "",
                "plemionaplaner.pl@gmail.com",
                recipient_list=[user.email],
                html_message=msg_html,
            )

        instance.new_date = user_profile.validity_date
        user_profile.save()
        instance.save()

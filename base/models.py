""" Database models """
import datetime
from math import sqrt
from typing import Dict, List, Optional
from dateutil.relativedelta import relativedelta

import django
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models.query import QuerySet
from django.db.models import F, Q, Count
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

from markdownx.models import MarkdownxField


class Server(models.Model):
    dns = models.CharField(max_length=50, primary_key=True)
    prefix = models.CharField(max_length=2)

    def __str__(self):
        return self.dns


class Message(models.Model):
    date = models.DateField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=20, default="bug fix")
    text = models.TextField(default="")


@receiver(post_save, sender=Message)
def created_message(sender, instance, created, **kwargs):
    if created:
        Profile.objects.all().update(messages=F("messages") + 1)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    server = models.ForeignKey(
        Server, on_delete=models.SET_NULL, null=True, default=None
    )
    validity_date = models.DateField(
        default=datetime.date(year=2021, month=2, day=25), blank=True, null=True
    )
    messages = models.IntegerField(default=0)

    def is_premium(self) -> bool:
        if self.validity_date is None:
            return False
        today = timezone.localdate()
        if today > self.validity_date:
            return False
        return True

    def latest_messages(self) -> "QuerySet[Message]":
        return Message.objects.order_by("-created")[:6]


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        default_server = Server.objects.get_or_create(dns="plemiona.pl", prefix="pl")[0]
        Profile.objects.create(user=instance, server=default_server)
    else:
        instance.profile.save()


class World(models.Model):
    """World in the game"""

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    postfix = models.CharField(max_length=10)
    last_update = models.DateTimeField(auto_now_add=True)

    connection_errors = models.IntegerField(default=0)
    speed_world = models.FloatField(null=True, blank=True, default=1)
    speed_units = models.FloatField(null=True, blank=True, default=1)
    paladin = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    archer = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    militia = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    max_noble_distance = models.IntegerField(default=50)

    def __str__(self):
        return self.server.prefix + self.postfix

    def human(self, prefix=False):
        if prefix:
            last = " " + self.server.prefix.upper()
        else:
            last = ""
        return gettext_lazy("World ") + self.postfix + last

    def link_to_game(self, addition=""):
        return f"https://{str(self)}." f"{self.server.dns}" f"{addition}"

    def tw_stats_link_to_village(self, village_id):
        return (
            f"https://{self.server.prefix}.twstats.com/{str(self)}/index.php?"
            f"page=village&id={village_id}"
        )


class Tribe(models.Model):
    """Tribe in game"""

    tribe_id = models.IntegerField()
    tag = models.TextField(db_index=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.tag


class Player(models.Model):
    """Player in the game"""

    player_id = models.IntegerField()
    name = models.TextField(db_index=True)
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE, null=True, blank=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class VillageModel(models.Model):
    """Village in the game"""

    village_id = models.IntegerField()
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    coord = models.CharField(max_length=7, db_index=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    def __str__(self):
        return self.coord


def create_test_world(server: Server):
    test_world = World.objects.create(server=server, postfix="Test")
    tribe1 = Tribe.objects.create(tribe_id=0, tag="ALLY", world=test_world)
    tribe2 = Tribe.objects.create(tribe_id=1, tag="ENEMY", world=test_world)
    ally_villages = []
    ally_players = []
    enemy_players = []
    enemy_villages = []
    for i in range(5):
        ally_players.append(
            Player(tribe=tribe1, world=test_world, player_id=i, name=f"AllyPlayer{i}")
        )
        enemy_players.append(
            Player(
                tribe=tribe2, world=test_world, player_id=i + 5, name=f"EnemyPlayer{i}"
            )
        )
    Player.objects.bulk_create(enemy_players)
    Player.objects.bulk_create(ally_players)
    ally_players = list(Player.objects.filter(world=test_world, player_id__lte=4))
    enemy_players = list(Player.objects.filter(world=test_world, player_id__gte=5))
    for i in range(50):
        ids = i // 10
        ally_villages.append(
            VillageModel(
                world=test_world,
                x_coord=100 + i,
                y_coord=100 + i,
                coord=f"{100+i}|{100+i}",
                village_id=i,
                player=ally_players[ids],
            )
        )
        enemy_villages.append(
            VillageModel(
                world=test_world,
                x_coord=200 + i,
                y_coord=200 + i,
                coord=f"{200+i}|{200+i}",
                village_id=i + 50,
                player=enemy_players[ids],
            )
        )

    VillageModel.objects.bulk_create(enemy_villages)
    VillageModel.objects.bulk_create(ally_villages)


@receiver(post_save, sender=Server)
def new_server_create_test_world(sender, instance, created, **kwargs):
    if created:
        create_test_world(server=instance)


def building_default_list() -> List[str]:
    return [
        "farm",
        "headquarters",
        "smithy",
    ]


class Outline(models.Model):
    """Outline with all informations about it"""

    VALID_SORT_CHOICES = [
        ("distance", "distance"),
        ("random_distance", "random_distance"),
        ("-distance", "-distance"),
        ("-off_left", "-off_left"),
        ("-nobleman_left", "-nobleman_left"),
        ("closest_offs", "closest_offs"),
        ("random_offs", "random_offs"),
        ("farthest_offs", "farthest_offs"),
        ("closest_noblemans", "closest_noblemans"),
        ("random_noblemans", "random_noblemans"),
        ("farthest_noblemans", "farthest_noblemans"),
        ("closest_noble_offs", "closest_noble_offs"),
        ("random_noble_offs", "random_noble_offs"),
        ("farthest_noble_offs", "farthest_noble_offs"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

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

    MODE_SPLIT = [
        ("together", gettext_lazy("Nobles from one village as one command")),
        ("split", gettext_lazy("Nobles from one village as many commands")),
    ]

    NOBLE_GUIDELINES = [
        ("one", gettext_lazy("Try send all nobles to one target")),
        ("many", gettext_lazy("Nobles to one or many targets")),
        ("single", gettext_lazy("Try single nobles from many villages")),
    ]

    HIDE_CHOICES = [
        ("all", gettext_lazy("All")),
        ("front", gettext_lazy("Front")),
        ("back", gettext_lazy("Back")),
        ("hidden", gettext_lazy("Hidden")),
    ]

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

    RUINED_VILLAGES_POINTS = [
        ("big", gettext_lazy("Average greater than 8k")),
        ("medium", gettext_lazy("Average 5-8k")),
    ]

    CATAPULTS_NUMBER = [(50, 50), (75, 75), (100, 100), (150, 150), (200, 200)]

    FAKE_MIN_OFF_CHOICES = [
        ("off", gettext_lazy("Fakes only from off villages")),
        ("all", gettext_lazy("Fakes from all villages")),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=django.utils.timezone.now)  # type: ignore
    name = models.TextField()
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    written = models.CharField(choices=STATUS_CHOICES, max_length=8, default="inactive")
    editable = models.CharField(choices=STATUS_CHOICES, max_length=8, default="active")
    ally_tribe_tag = ArrayField(models.CharField(max_length=6), default=list)
    enemy_tribe_tag = ArrayField(models.CharField(max_length=6), default=list)

    choice_sort = models.CharField(
        max_length=50, choices=VALID_SORT_CHOICES, default="distance"
    )
    initial_outline_targets = models.TextField(blank=True, default="")
    initial_outline_fakes = models.TextField(blank=True, default="")
    initial_outline_ruins = models.TextField(blank=True, default="")

    initial_outline_catapult_default = models.IntegerField(
        default=150, choices=CATAPULTS_NUMBER
    )
    initial_outline_off_left_catapult = models.IntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(400)]
    )
    initial_outline_average_ruining_points = models.CharField(
        max_length=150, choices=RUINED_VILLAGES_POINTS, default="big"
    )
    initial_outline_buildings = ArrayField(
        models.CharField(max_length=100, choices=BUILDINGS),
        default=building_default_list,
    )
    initial_outline_min_off = models.IntegerField(
        default=19000,
        validators=[MinValueValidator(1), MaxValueValidator(28000)],
    )
    initial_outline_front_dist = models.IntegerField(
        default=10, validators=[MinValueValidator(0), MaxValueValidator(45)]
    )
    initial_outline_target_dist = models.IntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(150)]
    )
    initial_outline_excluded_coords = models.TextField(default="", blank=True)
    initial_outline_fake_limit = models.IntegerField(
        default=4, validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    initial_outline_fake_mode = models.CharField(
        max_length=60, choices=FAKE_MIN_OFF_CHOICES, default="off"
    )
    off_troops = models.TextField(
        blank=True,
        default="",
    )
    deff_troops = models.TextField(
        blank=True,
        default="",
    )

    avaiable_offs = ArrayField(models.IntegerField(), default=list, blank=True)
    avaiable_nobles = ArrayField(models.IntegerField(), default=list, blank=True)
    avaiable_offs_near = ArrayField(models.IntegerField(), default=list, blank=True)
    avaiable_nobles_near = ArrayField(models.IntegerField(), default=list, blank=True)
    avaiable_ruins = models.IntegerField(default=None, null=True, blank=True)

    mode_off = models.CharField(max_length=15, choices=MODE_OFF, default="random")
    mode_noble = models.CharField(max_length=15, choices=MODE_NOBLE, default="closest")
    mode_division = models.CharField(
        max_length=15, choices=MODE_DIVISION, default="not_divide"
    )
    mode_guide = models.CharField(
        max_length=15, choices=NOBLE_GUIDELINES, default="one"
    )
    mode_split = models.CharField(max_length=15, choices=MODE_SPLIT, default="split")

    filter_weights_min = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(30000)]
    )
    filter_weights_max = models.IntegerField(
        default=30000,
        validators=[MinValueValidator(0), MaxValueValidator(30000)],
    )
    filter_card_number = models.IntegerField(
        default=12,
        validators=[MinValueValidator(1), MaxValueValidator(40)],
    )
    filter_targets_number = models.IntegerField(
        default=12,
        validators=[MinValueValidator(1), MaxValueValidator(40)],
    )
    filter_hide_front = models.CharField(
        max_length=20, choices=HIDE_CHOICES, default="all"
    )

    filter_targets_number = models.IntegerField(
        default=12,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
    )
    simple_textures = models.BooleanField(default=False)
    default_show_hidden = models.BooleanField(default=False)
    title_message = models.CharField(
        max_length=50, default=gettext_lazy("Outline Targets")
    )
    text_message = models.CharField(max_length=500, default="", blank=True)
    night_bonus = models.BooleanField(default=False)
    enter_t1 = models.IntegerField(default=7)
    enter_t2 = models.IntegerField(default=12)
    default_off_time_id = models.IntegerField(default=None, null=True, blank=True)
    default_fake_time_id = models.IntegerField(default=None, null=True, blank=True)
    default_ruin_time_id = models.IntegerField(default=None, null=True, blank=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "ID:" + str(self.pk) + ", Nazwa: " + str(self.name)

    def remove_user_outline(self):
        self.written = "inactive"
        self.avaiable_offs = []
        self.avaiable_offs_near = []
        self.avaiable_nobles = []
        self.avaiable_nobles_near = []
        self.avaiable_ruins = None
        self.filter_weights_min = 0
        self.filter_weights_max = 30000
        self.filter_card_number = 12
        self.filter_targets_number = 12
        self.filter_hide_front = "all"
        self.choice_sort = "distance"
        self.default_off_time_id = None
        self.default_fake_time_id = None
        self.default_ruin_time_id = None

        WeightMaximum.objects.filter(outline=self).delete()
        OutlineTime.objects.filter(outline=self).delete()
        TargetVertex.objects.filter(outline=self).delete()
        Overview.objects.filter(outline=self, removed=False).update(removed=True)
        result: Result = Result.objects.get(outline=self)
        result.results_outline = ""
        result.results_players = ""
        result.results_sum_up = ""
        result.save()
        self.save()

    def count_targets(self) -> int:
        targets: "QuerySet[TargetVertex]" = TargetVertex.objects.filter(outline=self)
        return targets.filter(fake=False, ruin=False).count()

    def count_fake(self) -> int:
        targets: "QuerySet[TargetVertex]" = TargetVertex.objects.filter(outline=self)
        return targets.filter(fake=True, ruin=False).count()

    def count_ruin(self) -> int:
        targets: "QuerySet[TargetVertex]" = TargetVertex.objects.filter(outline=self)
        return targets.filter(fake=False, ruin=True).count()

    def count_off(self) -> int:
        weights: "QuerySet[WeightMaximum]" = WeightMaximum.objects.filter(outline=self)
        return weights.filter(off_left__gte=self.initial_outline_min_off).count()

    def count_noble(self) -> int:
        weights: "QuerySet[WeightMaximum]" = WeightMaximum.objects.filter(outline=self)
        return weights.aggregate(sum=Sum("nobleman_left"))["sum"] or 0

    def pagin_targets(
        self,
        page: Optional[str],
        fake: bool = False,
        ruin: bool = False,
        every: bool = False,
        filtr: str = "",
        not_empty_only: bool = False,
        related: bool = False,
    ):
        all_targets: "QuerySet[TargetVertex]" = TargetVertex.objects.filter(
            outline=self
        ).order_by("pk")

        if not every:
            targets = all_targets.filter(fake=fake, ruin=ruin)
        else:
            targets = all_targets

        if not_empty_only:
            targets = targets.annotate(num_of_weights=Count("weightmodel")).filter(
                num_of_weights__gt=0
            )

        if related:
            targets = targets.select_related("outline_time")

        if filtr != "":
            if "|" in filtr:
                targets = targets.filter(target__icontains=filtr)
            elif filtr.isnumeric() and len(filtr) <= 3:
                targets = targets.filter(
                    Q(target__icontains=filtr) | Q(player__icontains=filtr)
                )
            elif (
                filtr.startswith("command")
                and filtr[7] in [">", "<", "="]
                and filtr[8:].isnumeric()
            ):
                if not not_empty_only:
                    targets = targets.annotate(num_of_weights=Count("weightmodel"))
                if filtr[7] == ">":
                    targets = targets.filter(num_of_weights__gt=int(filtr[8:]))
                elif filtr[7] == "=":
                    targets = targets.filter(num_of_weights=int(filtr[8:]))
                else:
                    targets = targets.filter(num_of_weights__lt=int(filtr[8:]))

            else:
                targets = targets.filter(player__icontains=filtr)

        pagin = Paginator(targets, self.filter_targets_number)
        return pagin.get_page(page)

    def targets_query(self, target_lst):
        result: Dict[TargetVertex, List[WeightModel]] = {}
        for target in target_lst:
            result[target] = list()
        weights: "QuerySet[WeightModel]" = (
            WeightModel.objects.select_related("target")
            .filter(target__in=target_lst)
            .order_by("order")
        )
        weight: WeightModel
        for weight in weights:
            weight.distance = round(weight.distance_to_village(weight.target.target), 1)
            weight.off = f"{round(weight.off / 1000, 1)}k"
            result[weight.target].append(weight)
        return result.items()

    def create_target(self, target_type: Optional[str], coord: Optional[str]) -> None:
        if target_type == "real":
            fake = False
            ruin = False
        elif target_type == "fake":
            fake = True
            ruin = False
        else:
            fake = False
            ruin = True
        village: VillageModel = VillageModel.objects.select_related().get(
            coord=coord, world=self.world
        )
        TargetVertex.objects.create(
            outline=self,
            player=village.player.name,
            target=coord,
            fake=fake,
            ruin=ruin,
        )

    def is_target_with_no_time(self) -> bool:
        return (
            TargetVertex.objects.filter(outline=self)
            .filter(outline_time=None)
            .annotate(num_of_weights=Count("weightmodel"))
            .filter(num_of_weights__gt=0)
            .exists()
        )

    def get_outline_times(self, with_periods: bool):
        outline_time_lst = OutlineTime.objects.filter(outline=self).order_by("order")
        if not with_periods:
            return outline_time_lst

        period_model_lst = (
            PeriodModel.objects.select_related("outline_time")
            .filter(outline_time__in=outline_time_lst)
            .order_by("from_time", "-unit")
        )

        result: Dict[OutlineTime, List[PeriodModel]] = {}
        period: PeriodModel
        for period in period_model_lst:
            if period.outline_time in result:
                result[period.outline_time].append(period)
            else:
                result[period.outline_time] = [period]
        return result


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
    amount = models.IntegerField()
    payment_date = models.DateField()
    months = models.IntegerField(default=1)
    comment = models.CharField(max_length=150, default="", blank=True)
    new_date = models.DateField(default=None, null=True, blank=True)


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

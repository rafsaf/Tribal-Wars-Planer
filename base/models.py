""" Database models """
import datetime
from dateutil.relativedelta import relativedelta

import django
from django.utils.translation import gettext_lazy, gettext
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from markdownx.models import MarkdownxField


class Server(models.Model):
    dns = models.CharField(max_length=50, primary_key=True)
    prefix = models.CharField(max_length=2)

    def __str__(self):
        return self.dns

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    server = models.ForeignKey(Server, on_delete=models.SET_NULL, null=True, default=None)
    validity_date = models.DateField(default=None, blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        default_server = Server.objects.get_or_create(dns="plemiona.pl", prefix="pl")[0]
        Profile.objects.create(user=instance, server=default_server)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class World(models.Model):
    """ World in the game """
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
    paladin = models.CharField(
        choices=STATUS_CHOICES, max_length=8, default="active"
    )
    archer = models.CharField(
        choices=STATUS_CHOICES, max_length=8, default="active"
    )
    militia = models.CharField(
        choices=STATUS_CHOICES, max_length=8, default="active"
    )
    max_noble_distance = models.IntegerField(default=50)

    def __str__(self):
        return self.server.prefix + self.postfix

    def human(self, prefix=False):
        if prefix:
            last = " " + self.server.prefix.upper()
        else:
            last = ""
        return  gettext_lazy("World ") + self.postfix + last

    def link_to_game(self, addition=""):
        return (
            f"https://{str(self)}."
            f"{self.server.dns}"
            f"{addition}"
        )

    def tw_stats_link_to_village(self, village_id):
        return (
            f"https://{self.server.prefix}.twstats.com/{str(self)}/index.php?"
            f"page=village&id={village_id}"
        )



class Tribe(models.Model):
    """ Tribe in game """

    tribe_id = models.IntegerField()
    tag = models.TextField(db_index=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return self.tag


class Player(models.Model):
    """ Player in the game """

    player_id = models.IntegerField()
    name = models.TextField(db_index=True)
    tribe = models.ForeignKey(Tribe, on_delete=models.CASCADE, null=True, blank=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class VillageModel(models.Model):
    """ Village in the game """

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
    tribe1 = Tribe.objects.create(tribe_id=0, tag='ALLY', world=test_world)
    tribe2 = Tribe.objects.create(tribe_id=1, tag='ENEMY', world=test_world)
    ally_villages = []
    ally_players = []
    enemy_players = []
    enemy_villages = []
    for i in range(5):
        ally_players.append(Player(tribe=tribe1, world=test_world, player_id=i, name=f'AllyPlayer{i}'))
        enemy_players.append(Player(tribe=tribe2, world=test_world, player_id=i+5, name=f'EnemyPlayer{i}'))
    Player.objects.bulk_create(enemy_players)
    Player.objects.bulk_create(ally_players)
    ally_players = list(Player.objects.filter(world=test_world, player_id__lte=4))
    enemy_players = list(Player.objects.filter(world=test_world, player_id__gte=5))
    for i in range(50):
        ids = i // 10
        ally_villages.append(
            VillageModel(world=test_world, x_coord=100+i, y_coord=100+i, coord=f"{100+i}|{100+i}", village_id=i, player=ally_players[ids])
        )
        enemy_villages.append(
            VillageModel(world=test_world, x_coord=200+i, y_coord=200+i, coord=f"{200+i}|{200+i}", village_id=i+50, player=enemy_players[ids])
        )

    VillageModel.objects.bulk_create(enemy_villages)
    VillageModel.objects.bulk_create(ally_villages)

@receiver(post_save, sender=Server)
def new_server_create_test_world(sender, instance, created, **kwargs):
    if created:
        create_test_world(server=instance)

class Outline(models.Model):
    """ Outline with all informations about it"""

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
        ("hidden", gettext_lazy("Hidden"))
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=django.utils.timezone.now)
    name = models.TextField()
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=8, default="active"
    )
    written = models.CharField(
        choices=STATUS_CHOICES, max_length=8, default="inactive"
    )
    editable = models.CharField(
        choices=STATUS_CHOICES, max_length=8, default="active"
    )
    ally_tribe_tag = ArrayField(models.CharField(max_length=6), default=list)
    enemy_tribe_tag = ArrayField(models.CharField(max_length=6), default=list)

    initial_outline_targets = models.TextField(blank=True, default="")
    initial_outline_fakes = models.TextField(blank=True, default="")
    initial_outline_ruins = models.TextField(blank=True, default="")

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
    initial_outline_excluded_coords = models.TextField(default="")
    initial_outline_fake_limit = models.IntegerField(
        default=4, validators=[MinValueValidator(0), MaxValueValidator(20)]
    )

    off_troops = models.TextField(blank=True, default="",)
    deff_troops = models.TextField(blank=True, default="",)

    avaiable_offs = ArrayField(models.IntegerField(), default=list)
    avaiable_nobles = ArrayField(models.IntegerField(), default=list)
    avaiable_offs_near = ArrayField(models.IntegerField(), default=list)
    avaiable_nobles_near = ArrayField(models.IntegerField(), default=list)

    mode_off = models.CharField(
        max_length=15, choices=MODE_OFF, default="random"
    )
    mode_noble = models.CharField(
        max_length=15, choices=MODE_NOBLE, default="closest"
    )
    mode_division = models.CharField(
        max_length=15, choices=MODE_DIVISION, default="not_divide"
    )
    mode_guide = models.CharField(
        max_length=15, choices=NOBLE_GUIDELINES, default="one"
    )
    mode_split = models.CharField(
        max_length=15, choices=MODE_SPLIT, default="split"
    )

    filter_weights_min = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(30000)]
    )
    filter_weights_max = models.IntegerField(
        default=30000,
        validators=[MinValueValidator(0), MaxValueValidator(30000)],
    )
    filter_card_number = models.IntegerField(
        default=12, validators=[MinValueValidator(1), MaxValueValidator(40)],
    )
    filter_targets_number = models.IntegerField(
        default=12, validators=[MinValueValidator(1), MaxValueValidator(40)],
    )
    filter_hide_front = models.CharField(
        max_length=20, choices=HIDE_CHOICES, default="all"
    )

    filter_targets_number = models.IntegerField(
        default=12, validators=[MinValueValidator(1), MaxValueValidator(50)],
    )

    default_show_hidden = models.BooleanField(default=False)
    title_message = models.CharField(max_length=50, default=gettext_lazy("Outline Targets"))
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
        return "ID:" + str(self.id) + ", Nazwa: " + str(self.name)

    def remove_user_outline(self):
        self.written = "inactive"
        self.avaiable_offs = []
        self.avaiable_offs_near = []
        self.avaiable_nobles = []
        self.avaiable_nobles_near = []
        self.filter_weights_min = 0
        self.filter_weights_max = 30000
        self.filter_card_number = 12
        self.filter_targets_number = 12
        self.filter_hide_front = "all"
        self.default_off_time_id = None
        self.default_fake_time_id = None
        self.default_ruin_time_id = None
 
        WeightMaximum.objects.filter(outline=self).delete()
        OutlineTime.objects.filter(outline=self).delete()
        TargetVertex.objects.filter(outline=self).delete()
        Overview.objects.filter(outline=self, removed=False).update(removed=True)
        result = self.result
        result.results_outline = ""
        result.results_players = ""
        result.results_sum_up = ""
        result.save()

        self.save()


class Result(models.Model):
    """ Presents Outline and Deff results """

    outline = models.OneToOneField(
        Outline, on_delete=models.CASCADE, primary_key=True
    )
    results_get_deff = models.TextField(default="")
    results_outline = models.TextField(default="")
    results_players = models.TextField(default="")
    results_sum_up = models.TextField(default="")
    results_export = models.TextField(default="")

    def __str__(self):
        return self.outline.name + " results"


class Documentation(models.Model):
    """ Docs page """

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
    """ Control state smaller than maximum """

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE, db_index=True)
    start = models.CharField(max_length=7, db_index=True)
    x_coord = models.IntegerField(default=0)
    y_coord = models.IntegerField(default=0)
    player = models.CharField(max_length=30)
    off_max = models.IntegerField()
    off_state = models.IntegerField(default=0)
    off_left = models.IntegerField()
    off_in_village = models.IntegerField(null=True, blank=True, default=None)
    nobleman_max = models.IntegerField()
    nobleman_state = models.IntegerField(default=0)
    nobleman_left = models.IntegerField()
    nobleman_in_village = models.IntegerField(
        null=True, blank=True, default=None
    )
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
    """ Handle Time for Target """

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)


class PeriodModel(models.Model):
    """ Handle one period of time in outline specification """

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
    """ Target Village """

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

    mode_off = models.CharField(
        max_length=15, choices=MODE_OFF, default="random"
    )
    mode_noble = models.CharField(
        max_length=15, choices=MODE_NOBLE, default="closest"
    )
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
        return reverse(
            "base:planer_initial_detail", args=[self.outline_id, self.id]
        )

    def coord_tuple(self):
        return (int(self.target[0:3]), int(self.target[4:7]))


class WeightModel(models.Model):
    """ Command between start and target """

    target = models.ForeignKey(TargetVertex, on_delete=models.CASCADE, db_index=True)
    state = models.ForeignKey(WeightMaximum, on_delete=models.CASCADE)
    start = models.CharField(max_length=7)
    off = models.IntegerField()
    distance = models.FloatField()
    nobleman = models.IntegerField()
    order = models.IntegerField()
    player = models.CharField(max_length=40)
    first_line = models.BooleanField(default=False)
    t1 = models.TimeField(default=datetime.time(hour=0, minute=0, second=0))
    t2 = models.TimeField(default=datetime.time(hour=0, minute=0, second=0))

    def __str__(self):
        return self.start

class OutlineOverview(models.Model):
    outline = models.ForeignKey(Outline, on_delete=models.SET_NULL, null=True, blank=True)
    weights_json = models.TextField(default="", blank=True)
    targets_json = models.TextField(default="", blank=True)

class Overview(models.Model):
    """ Present results for tribe members using unique urls """
    outline_overview = models.ForeignKey(OutlineOverview, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, primary_key=True, db_index=True)
    outline = models.ForeignKey(Outline, on_delete=models.SET_NULL, null=True, blank=True)
    player = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    table = models.TextField()
    string = models.TextField()
    deputy = models.TextField(default="")
    targets = models.TextField(default="")
    show_hidden = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("base:overview", args=[self.token])


class TargetVertexOverview(models.Model):
    """ Copied Target Village """

    outline_overview = models.ForeignKey(OutlineOverview, on_delete=models.CASCADE)
    target = models.CharField(max_length=7)
    player = models.CharField(max_length=30)
    fake = models.BooleanField(default=False)
    target_vertex = models.ForeignKey(TargetVertex, on_delete=models.SET_NULL, null=True, default=None, blank=True)

    def __str__(self):
        return self.target


class WeightModelOverview(models.Model):
    """ Copied Command between start and target """

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
    """ Represents real payment, only superuser access """
    STATUS = [
        ("finished", gettext_lazy("Finished")),
        ("returned", gettext_lazy("Returned")),
    ]
    status = models.CharField(max_length=30, choices=STATUS, default="finished")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.IntegerField()
    payment_date = models.DateField()
    months = models.IntegerField(default=1)
    comment = models.CharField(max_length=150, default="", blank=True)
    new_date = models.DateField(default=None, null=True, blank=True)

@receiver(post_save, sender=Payment)
def create_user_profile(sender, instance: Payment, created, **kwargs):
    if created:
        user_profile: Profile = instance.user.profile
        current_date = instance.payment_date
        relative_months = relativedelta(months=instance.months)
        day = relativedelta(days=1)
        if user_profile.validity_date is None:
            user_profile.validity_date = current_date + relative_months + day
        elif user_profile.validity_date <= current_date:
            user_profile.validity_date = current_date + relative_months + day
        else:
            user_profile.validity_date = user_profile.validity_date + relative_months + day
        
        instance.new_date = user_profile.validity_date
        user_profile.save()
        instance.save()


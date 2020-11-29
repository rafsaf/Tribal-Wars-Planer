""" Database models """
import datetime

from django.utils.translation import gettext_lazy
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from markdownx.models import MarkdownxField


class World(models.Model):
    """ World in the game """

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    title = models.TextField(verbose_name="Tytuł")
    world = models.IntegerField(verbose_name="Numer świata")
    classic = models.BooleanField(default=False)
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

    def __str__(self):
        return str(self.title)

    def tw_stats_link_to_village(self, village_id):
        if self.classic:
            short = f"plc{self.world}"
        else:
            short = f"pl{self.world}"

        return (
            f"https://pl.twstats.com/{short}/index.php?"
            f"page=village&id={village_id}"
        )

    class Meta:
        ordering = ("-world",)


class TribeHasUnallowedPatternInTag(Exception):
    """ Tribe Exception """


class Tribe(models.Model):
    """ Tribe in game """

    id = models.CharField(primary_key=True, max_length=11)
    tribe_id = models.IntegerField()
    tag = models.TextField()
    world = models.IntegerField()

    def __str__(self):
        return self.tag


class Player(models.Model):
    """ Player in the game """

    id = models.CharField(primary_key=True, max_length=30)
    player_id = models.IntegerField()
    name = models.TextField()
    tribe_id = models.IntegerField()
    world = models.IntegerField()

    def __str__(self):
        return self.name


class VillageModel(models.Model):
    """ Village in the game """

    id = models.CharField(primary_key=True, max_length=9)
    village_id = models.IntegerField()
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()
    player_id = models.IntegerField()
    world = models.IntegerField(db_index=True)

    def __str__(self):
        return str(self.village_id)


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

    NOBLE_GUIDELINES = [
        ("one", gettext_lazy("Try send all nobles to one target")),
        ("many", gettext_lazy("Nobles to one or many targets")),
        ("single", gettext_lazy("Try single nobles from many villages")),
    ]

    HIDE_CHOICES = [
        ("all", gettext_lazy("All")),
        ("front", gettext_lazy("Front")),
        ("back", gettext_lazy("Back")),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    name = models.TextField()
    world = models.IntegerField(null=True, blank=True)
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

    initial_outline_players = models.TextField(blank=True, default="")
    initial_outline_targets = models.TextField(blank=True, default="---")
    initial_outline_min_off = models.IntegerField(
        default=19000,
        validators=[MinValueValidator(1), MaxValueValidator(28000)],
    )
    initial_outline_front_dist = models.IntegerField(
        default=12, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    initial_outline_target_dist = models.IntegerField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(150)]
    )
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
    filter_hide_front = models.CharField(
        max_length=20, choices=HIDE_CHOICES, default="all"
    )
    default_show_hidden = models.BooleanField(default=False)
    title_message = models.CharField(max_length=50, default="Cele Akcja")
    text_message = models.CharField(max_length=300, default="", blank=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return "ID:" + str(self.id) + ", Nazwa: " + str(self.name)

    def remove_user_outline(self):
        self.written = "inactive"
        WeightMaximum.objects.filter(outline=self).delete()
        OutlineTime.objects.filter(outline=self).delete()
        TargetVertex.objects.filter(outline=self).delete()
        Overview.objects.filter(outline=self).delete()
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
    results_get_off = models.TextField(default="")
    results_outline = models.TextField(default="")
    results_players = models.TextField(default="")
    results_sum_up = models.TextField(default="")

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

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE)
    start = models.CharField(max_length=7)
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

    outline = models.ForeignKey(Outline, on_delete=models.CASCADE)
    outline_time = models.ForeignKey(
        OutlineTime, on_delete=models.SET_NULL, null=True, default=None
    )
    target = models.CharField(max_length=7)
    player = models.CharField(max_length=30)
    fake = models.BooleanField(default=False)

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

    target = models.ForeignKey(TargetVertex, on_delete=models.CASCADE)
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


class Overview(models.Model):
    """ Present results for tribe members using unique urls """

    token = models.CharField(max_length=100, primary_key=True, db_index=True)
    outline = models.ForeignKey(Outline, on_delete=models.CASCADE)
    player = models.CharField(max_length=40)
    created = models.DateField(auto_now=True)
    table = models.TextField()
    string = models.TextField()
    show_hidden = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("base:overview", args=[self.token])
